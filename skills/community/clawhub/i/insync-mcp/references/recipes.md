# insync-fpx recipes

All verified live 2026-10-28. `I=~/.claude/skills/insync-fpx/scripts/insync`.

## At a glance

```sh
$I counts | jq '{UnreadMessage, Medications, PendingPatientFormCount, PendingPatientSurveyFormCount, Problems}'
$I balance | jq '{owed: (if .NetDue > 0 then .NetDue else 0 end), credit: .CreditBalance}'
```

## Appointments

```sh
# next appointment
$I appointments | jq '.appointments[0] | "\(.VisitDate) \(.StartTime) with \(.Provider) — \(.VisitType)"'
# last 5 visits with status + copay
$I appointments past 5 | jq -r '.appointments[] | [.VisitDate, .StartTime, .Provider, .VisitStatus, .ExpectedCopay] | @tsv'
```

Record fields: `VisitID VisitDate StartTime EndTime Provider FacilityName VisitType VisitStatus ExpectedCopay`.
`VisitDate` is `M/D/YYYY`. `VisitStatus` values seen on past visits: `Check In`, `Check Out`, `No Show`.

## Medications

```sh
$I medications | jq -r '.medications[] | [.DrugName, .Dispense, "refills:\(.Refills)", .PrescriptionDate, .PhysicianName] | @tsv'
# refills left per drug, lowest first
$I medications | jq '[.medications[] | {DrugName, Refills: (.Refills|tonumber? // .Refills)}] | sort_by(.Refills)'
```

`PrescriptionDate` is `MM/DD/YYYY hh:mm AM`. `Rxcui` is the RxNorm id.

## Messages

```sh
# unread triage: sender, date, subject (does NOT mark read)
$I messages unread 50 | jq -r '.messages[] | [.date, .from, .subject] | @tsv'
# my sent messages
$I messages sent 10 | jq -r '.messages[] | [.date, .to, .subject] | @tsv'
# read one ALREADY-READ message, body as plain text
row=$($I messages read 1 | jq -c '.messages[0]')
$I message "$(jq -r .childId <<<"$row")" "$(jq -r .masterId <<<"$row")" |
  jq -r '.bodyHtml' | sed -e 's/<[^>]*>//g' -e 's/&nbsp;/ /g' | sed '/^[[:space:]]*$/d'
```

`date` is `MM/DD/YYYY hh:mm AM`. Many unread items are `System Alert` notices
(new forms or assessments available). Filter those with
`select(.from != "System Alert")`.

## Forms

```sh
$I forms | jq -r '.[] | [.SentOn, .FormName] | @tsv'          # what's outstanding
$I forms all | jq 'group_by(.Status) | map({status: .[0].Status, n: length})'
```

`Status`: `Sent` = waiting on the patient, `Received` = submitted.

## Surveys

```sh
$I surveys | jq -r '.[] | [.received, .name] | @tsv'     # received = MM/DD/YYYY
```

## Anything else

```sh
$I raw GET  '/PatientScheduler/GetVisitDetails?...'   # GETs: query-string params
$I raw POST /Dashboard/GetDashboardDetails '{}'       # POSTs: JSON body
```

See `endpoints.md` for the catalog and the paging conventions.
