# MyAtriumHealth endpoints — verified recipes

Every recipe below was run against a live signed-in session. `source mah.sh` first and
cache the token once per shell:

    source references/mah.sh
    mah_signed_in || echo "sign in to MyAtriumHealth in Chrome first"
    export MAH_TOKEN="$(mah_token)"       # 172 chars; avoids re-fetching a 137KB page per call

Response envelopes are large (test results 33KB, medications 30KB) — always project
with `jq` rather than printing whole responses.

---

## Allergies

    mah_api allergies/LoadAllergies | jq '[.dataList[].allergyItem
      | {name, severe: .isSevere, reactions: [.reactionList[]?.name]}]'

`dataList[].allergyItem` → `{id, name, reactionList[], classification, isSevere, priority, displayType}`.
`localItem` repeats the same shape for this organization; `externalItems`/`externalOrgs`
carry the same allergy as recorded at linked outside organizations.

## Health issues (problem list)

    mah_api HealthIssues/LoadHealthIssuesData | jq '[.dataList[].healthIssueItem
      | {name, noted: .formattedDateNoted}]'

`healthIssueItem` → `{name, id, formattedDateNoted, action, isReadOnly}`.

## Immunizations

    mah_api immunizations/LoadImmunizations | jq '[.organizationImmunizationList[]
      | {org: .organization.OrganizationName?} + {shots: [.orgImmunizations[] | {name, dates: .formattedAdministeredDates}]}]'

Grouped per organization: `organizationImmunizationList[].orgImmunizations[]`
→ `{id, name, formattedAdministeredDates}`.

## Medications

    mah_api medications/LoadMedicationsPage | jq '[.communityMembers[]
      | .prescriptionList.prescriptions[]?
      | {name, friendly: .patientFriendlyName, sig, provider: .authorizingProvider}]'

`communityMembers[]` is one entry per organization; each has
`prescriptionList.prescriptions[]` → `{name, patientFriendlyName, sig,
prescriptionNumber, authorizingProvider, orderingProvider, dateToDisplay,
isPatientReported, …}`. `sig` is the dosing instruction text.

## Test results

    # index of result groups (visits), newest first
    mah_api test-results/GetList | jq '[.newResultGroups[]
      | {date: .formattedDate, type: .contactType, count: (.resultList | length)}]'

    # the results themselves — newResults is a MAP keyed by an opaque handle
    mah_api test-results/GetList | jq '[.newResults[]
      | {name, abnormal: .isAbnormal,
         when: .orderMetadata.prioritizedInstantDisplay,
         provider: .orderMetadata.orderProviderName,
         comments: [.providerComments[]?.content]}]'

`newResultGroups[].resultList` is an array of **strings** — handles into `newResults`.
`resultComponents` is empty in the list view (individual values load on the detail page).
`orderMetadata` → `{orderProviderName, authorizingProviderName, prioritizedInstantISO,
prioritizedInstantDisplay, resultType, read}`.

## Goals

    mah_api goals/LoadPatientGoals | jq '[.patientGoals[] | {goalId, goalType, lastUpdatedDate}]'

## Health summary / menu / folders

    mah_api health-summary/FetchHealthSummary | jq '{patientFirstName, actionPlans}'
    mah_api conversations/GetFoldersList     | jq '.folders'      # [{tag, badgeCount, totalCount}]
    mah_api search/LoadMenuInfo              | jq '[.submenus[] | {menu: .name, items: [.menuItems[].name]}]'

`search/LoadMenuInfo` currently answers 302 to `Home/FiveHundred` (a server error), so
expect that call to fail until its real parameters are captured.

Folder tags seen: `1` Conversations/inbox, `2` Archive, `3`, `6`, `7`
(Bookmarked / Appointments / Automated — exact mapping unconfirmed).

## Insurance

    mah_legacy_form Insurance/Coverages/GetCoverages 'isStandAlone=true' | jq '.ActiveCoverages'

Needs the form body `isStandAlone=true`; an empty body returns the "Oops!" page.
Coverages arrive in five buckets — `ActiveCoverages`, `CoveragesPendingSubmission`,
`CoveragesPendingDeletion`, `CoveragesInReview`, `CoveragesInVerification` — so check
all of them, not just the first. Each item has `CoverageName`, `PlanName`, `PayorName`,
`MemberId`, `GroupNumber`, `Status`, `CoverageType`, `FormattedEffectiveDate`,
`FormattedEndDate`, `SubscriberName`, `PatientIsSubscriber`, `Termed` and more.

## Care team

    mah_legacy Clinical/CareTeam/Load "hfrId=&sources=&actions=&isPrimaryStandalone=true&ComponentNumber=2" \
      | jq '[.ProvidersList[] | {name: .Name, specialty: .Specialty, relation: .Relation}]'

`LoadExternal` (same query minus `isPrimaryStandalone`) returns providers at linked
outside organizations. The page shows the union of both — de-duplicate on `.ID`.

Billing is server-rendered with **no data endpoint**; the MCP's
`mah_list_billing_accounts` parses it. Documents renders no list on its landing page and
has not been captured.

## Visits (legacy form-encoded endpoints — use `mah_legacy`)

    mah_legacy Visits/VisitsList/LoadUpcoming "timeZone=America%2FNew_York&ComponentNumber=5" \
      | jq '{next: .NextNDaysVisits, later: .LaterVisitsList, inProgress: .InProgressVisits}'

    NOW=$(date -u +%Y-%m-%dT%H:%M:%S.000Z)
    mah_legacy Visits/VisitsList/LoadPast "loadpast=1&searchString=&oldestRenderedDate=$NOW&ComponentNumber=7" \
      | jq '[.List[] | .Organization.OrganizationName as $o
             | .List[] | {org: $o, date: .PrimaryDate, bucket: .PastVisitBucket, csn: .Csn}]'

Past visits are grouped by an opaque organization handle under `.List`.

---

## Messages

    mah_messages       | jq '[.conversations[] | {subject, preview: .previewText,
                              date: .messages[0].deliveryInstantISO,
                              unread: ([.messages[].isUnread] | any)}]'
    mah_messages 2     | jq '.conversations | length'    # 2 = Archive

`POST api/conversations/GetConversationList` needs a five-key body, and every part
matters — this is the one endpoint here that cannot be called with `{}`:

    {"tag":1,
     "localLoadParams":{"loadStartInstantISO":"","loadEndInstantISO":"","pagingInfo":1},
     "externalLoadParams":{"<external org handle>":{"communicationCenter":{…same three…}}},
     "searchQuery":"",
     "PageNonce":"<32-hex CSP nonce from an /app/* page>"}

**`externalLoadParams` takes the NON-local organizations only.** Get them from
`api/conversations/GetOrganizations` (which does take `{}`) and filter on the explicit
`isLocal` flag. Passing the local organization — or the handles from the visits
response, which include it — returns HTTP 500.

Response: `{conversations[], users, viewers, localSummary, externalSummaries,
legacyXUnreadCount}`. Each conversation has `subject`, `previewText`, `messageType`,
`hasAttachments`, `hasUrgentMsgs`, `organizationId` and `messages[]`
→ `{author, body, deliveryInstantISO, isUnread, attachments, tasks}`.

Do not try to satisfy the nonce by generating values — it is an anti-CSRF control;
read the one the server sent (`mah_nonce`).

`api/item-feed/FetchItemFeed` still needs parameters that have not been captured.
