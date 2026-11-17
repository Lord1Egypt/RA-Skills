# PickUp Patrol API reference

Every shape here was read off the shipped SPA's own request DTO classes or
observed on a live signed-in session (2026-08-16). No credential, cookie or
token value is recorded.

- Base: `https://app.pickuppatrol.net/api/json/reply/<DtoName>`
- GET args on the query string; POST/PUT/PATCH args in a JSON body
- Auth: session cookies from `Authenticate` (`ss-id`, `ss-pid`, `ss-opt`). This
  deployment returns `BearerToken: null`; send `Authorization: Bearer …` too if
  one ever appears
- Errors: ServiceStack `{"ResponseStatus":{"ErrorCode","Message","Errors":[…]}}`;
  an unauthenticated call to any authorised DTO is a bare `401`

Assumes the `pup` / `pup_login` shell functions from `SKILL.md`.

## Authentication

```bash
curl -sS -c jar -X POST "$PUP/Authenticate" -H 'Content-Type: application/json' \
  -d '{"provider":"credentials","UserName":"…","Password":"…","RememberMe":true}'
```

Response: `{UserId, SessionId, UserName, DisplayName, BearerToken, RefreshToken,
Roles, Permissions, ResponseStatus}` — `BearerToken` and `RefreshToken` come
back null here; the session is the cookies.

Two-factor accounts (`User.OtpTypeId` set) need `POST /CreateOtp {OtpTypeId}`
then `PUT /VerifyOtp {Otp, RememberMe}`. Token refresh is
`POST /GetAccessToken {refreshToken}` or `GET /RequestNewtoken?OldToken=…`.

## Read DTOs

| DTO | Args |
|---|---|
| `GetSession` | — |
| `GetSessionInfo` | — |
| `GetChildren` | — |
| `GetStudent` | `StudentId`, `MergeTimeWithNote?` |
| `GetDefaultPlansReviewNeeded` | — |
| `GetParentPlans` | `StartDate`, `EndDate` |
| `GetPlanEdit` | `PlanDate`, `StudentId` |
| `GetBoldedDates` | `StartDate`, `EndDate` (dates differing from the default) |
| `GetInvalidPlanDates` | `SchoolId` (non-school days) |
| `GetTransportations` | `SchoolId` |
| `GetCarNumbers` | `SchoolId` |
| `GetSchool` | `SchoolId` |
| `GetSchoolNotifyTimes` | `SchoolId` |
| `GetSchoolSettings` | `SchoolId` |
| `GetMiddayPlan` | `StudentId`, `PlanDate`, `TypeId?` |
| `GetParentHealthScreenAudits` | `ScreenDate` |
| `GetTermsOfUse` | — |

### Student

```
StudentId SchoolId SchoolName FirstName LastName IsActive SASId TeacherId
AllowPlans CreateDate CreatedBy ModifiedDate ModifiedBy DefaultsModifiedDate
DefaultPlanModifiedBy DefaultsReviewedDate DefaultsReviewedBy DefaultPlans
SafetyFlag DefaultCarNumber LimitedIds
```

`DefaultPlans[]`:

```json
{"StudentId":1050046,"DayId":2,"TransportationId":41246,"Note":"Chris Hall",
 "TransportationName":"PickUp","WeekDayName":"Monday","EarlyDismissalTime":null,
 "CarNumber":null,"UseCarNumbers":false}
```

`DayId` is 1-based with **Sunday = 1** — verified from a live record where
`DayId: 2` carried `WeekDayName: "Monday"`.

### Transportation

```
TransportationId SchoolId Name NoteHint IsNoteRequired UseCarNumbers
IsNotePrivate IsActive Sequence IsEarlyDismissal IsLimited CutoffTime
CutoffTime{Sunday…Saturday} AllowParentCheck
```

### GetPlanEdit

```
PlanDate StudentId FirstName LastName SchoolId TransportationId Note IsLocked
TransportationName SchoolName BusRouteUrl ValidationErrors EarlyDismissalTime
CarNumber LimitedIds IsNotePrivate
```

Returns the date's **override**, not the effective plan: a date with no specific
plan reads back `TransportationId: null` even when the student has a weekly
default for that weekday. Merge with `GetStudent(...).DefaultPlans` yourself to
know what actually happens on a date.

## Write DTOs

| DTO | Verb | Body |
|---|---|---|
| `UpdatePlans` | PUT | `{Plans:[…]}` |
| `Student` | PUT | the whole student record |
| `SetDefaultsReviewed` | PUT | `{StudentId, Reviewed}` |
| `UpdateMiddayPlanCheck` | PUT | `{StudentId, PlanDate, TypeId, Action}` |
| `MiddayPlan` | PUT | full midday-plan record |
| `UpdateSendPlanConfirmationEmail` | PUT | `{Send}` |
| `UpdateUserLanguage` | PATCH | `{Language}` |
| `AcceptTerms` | PUT | — |
| `ChangePassword` | PUT | `{CurrentPassword, NewPassword, ConfirmPassword}` |

### UpdatePlans element

```json
{"StudentId":1050046,"SchoolId":1703,"PlanDate":"2026-08-17",
 "TransportationId":41246,"TransportationName":"PickUp","Note":"Chris Hall",
 "EarlyDismissalTime":"13:00:00","CarNumber":"12"}
```

Omit `EarlyDismissalTime` unless the option has `IsEarlyDismissal`, and
`CarNumber` unless it has `UseCarNumbers` — the web app leaves both keys off
otherwise.

Build several dates at once:

```bash
jq -nc --argjson dates '["2026-08-17","2026-08-18"]' '
  {Plans: ($dates | map({
    StudentId:1050046, SchoolId:1703, PlanDate:.,
    TransportationId:41246, TransportationName:"PickUp", Note:"Chris Hall"}))}' \
| xargs -0 -I{} sh -c 'pup PUT UpdatePlans -d "$1"' _ {}
```

### Weekly defaults: read-modify-write the whole student

There is no default-plans endpoint. Read the student, replace only
`DefaultPlans`, PUT the whole record to the `Student` DTO.

```bash
STUDENT=1050046
pup GET "GetStudent?StudentId=$STUDENT" > /tmp/pup_student.json

# Set Monday (DayId 2) and Tuesday (3) to Bus (41245).
jq '.DefaultPlans = (
      (.DefaultPlans // []) as $p
      | [2,3] as $days
      | ($p | map(select(.DayId as $d | $days | index($d) | not)))
        + ($days | map({DayId:., TransportationId:41245, TransportationName:"Bus", Note:null}))
      | sort_by(.DayId))' /tmp/pup_student.json > /tmp/pup_student_new.json

pup PUT Student -d @/tmp/pup_student_new.json

# Verify: compare TransportationId per DayId, never DefaultsModifiedDate.
pup GET "GetStudent?StudentId=$STUDENT" \
  | jq '.DefaultPlans | sort_by(.DayId) | map({DayId, TransportationId})'
```

Clear every default with `jq '.DefaultPlans = []'`.

Send every other field back verbatim — the whole record round-trips, so a
dropped field is a field cleared.

## Gates

- `GetSchoolSettings(...).General.AllowDefaultPlans` — school allows default plans
- `Student.AllowPlans` — this student's plans may be changed
- `GetSchoolNotifyTimes` — a weekday with no `NotifyTime<Day>` is not a school day
- `GetPlanEdit(...).IsLocked` — the cutoff for that date has passed

## Verifying a write

Re-read and compare the fields that prove the change — the transportation id
**and the note**. Every option seen so far is `IsNoteRequired`, so a note-only
edit is an ordinary change and an id-only comparison would pass without ever
observing it.

- one-off plan → `GetPlanEdit(PlanDate, StudentId)` → `.TransportationId`, `.Note`
- weekly defaults → `GetStudent(StudentId).DefaultPlans[]` → `.TransportationId`, `.Note`

After *clearing* a date, expect `TransportationId: null` — not the weekday
default, which `GetPlanEdit` does not merge in.

Exclude `ModifiedDate` and `DefaultsModifiedDate`: they advance on their own, so
including them makes every write look successful.
