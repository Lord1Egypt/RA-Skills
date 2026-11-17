# InSync portal endpoint catalog

Extracted 2026-10-28 from the portal's JS bundles and page scripts
(`pfbhintouch.insynchcs.com`). Paths are `/<Controller>/<Action>`, relative to
`INSYNC_PORTAL`. **Bold = verified live** (shape noted). Everything else is
unverified: read the call site and capture a real request before relying on it.
Names ending in a write verb are marked ✎. None of those are wired in the
skill, and each needs a live capture plus user confirmation first.

## Conventions

- Send `X-Requested-With: XMLHttpRequest` + `Accept: application/json` (the helper does).
- jQuery `ServerCall(url, method, data)` GETs put params in the query string.
  Angular `$http.post` sends JSON bodies. Both are accepted for the verified POSTs.
- DataTables grids (`serverSide: true`) need `draw=1&start=<offset>&length=<n>`
  and optionally `order[0][column]=<i>&order[0][dir]=asc|desc`.
- Some POSTs that change state include `__RequestVerificationToken` (from the
  hidden input of the same name on the page). The reads above do not need it.
- A signed-out session returns the login page (`<title>Portal :: Login`) with
  HTTP 200, or JSON `{"isTimeout":true,"redirectUrl":…}`.
- Mixed spellings are the server's: `FutureAppiontmentDetails`,
  `GetPateintBalance`, `GetDashBoradCount`, `todoMasaterId`.

## Account

- `Account/ClockInBind`
- `Account/ClockInConfig`
- `Account/HeaderBind`
- `Account/LogOut`

## AllergyMedicationClinical

- `AllergyMedicationClinical/Allergy`
- `AllergyMedicationClinical/ClinicalSummary`
- **`AllergyMedicationClinical/GetAllergiesGridData`**: GET DataTables params + `objAllergie={}` → `{data[],recordsTotal}`
- `AllergyMedicationClinical/GetClinicalGridData`
- `AllergyMedicationClinical/GetClinicalSummaryActionLogGridData`
- **`AllergyMedicationClinical/GetMedicationGridData`**: GET DataTables params + `objMedicationsSummary={"Type":"82"}` (82 current / 68 discontinued / 78 cancelled) → `{data[],recordsTotal}`; missing Type = HTTP 500
- `AllergyMedicationClinical/GetPatientEncounterTypes`
- `AllergyMedicationClinical/GeteMARMedicationGridData`
- `AllergyMedicationClinical/Medications`

## Appointment

- `Appointment/CancelAppointmentRequest` ✎

## AssessmentTools

- `AssessmentTools/GetCommonInstructionMessage`
- **`AssessmentTools/GetReceivedAssessmentTools`**: GET → HTML fragment (empty here)
- `AssessmentTools/GetSubmittedAssessmentTools`

## ClinicalSummary

- `ClinicalSummary/DownloadCDA`
- `ClinicalSummary/GetAntiForgeryToken`
- `ClinicalSummary/GetDirectEmailSentDraftGridData`
- `ClinicalSummary/IOSDownloadCDA`
- `ClinicalSummary/TransmitCDA` ✎
- `ClinicalSummary/ViewCDA`
- `ClinicalSummary/ViewSOAP`

## CloverPayment

- `CloverPayment/Index`

## CommonFunctions

- `CommonFunctions/DownloadRawFile`
- `CommonFunctions/GetConsentInformation`

## CommonViews

- `CommonViews/GetCaptureImagePopupBody`
- `CommonViews/PatientStatement`

## Dashboard

- `Dashboard/BindBillingEntity`
- `Dashboard/CheckTelemedicineCoapyCollection`
- `Dashboard/ConsentMaxAmount`
- `Dashboard/GetCaseWorkerPatientList`
- `Dashboard/GetClinicalSummaryByEncounterType`
- **`Dashboard/GetDashBoradCount`**: POST `{}` → `.Dashboard[0]` badge counts
- `Dashboard/GetDashboardAllowedPages`
- `Dashboard/GetDashboardAppointmentDetails`
- **`Dashboard/GetDashboardDetails`**: POST `{}` → `.Dashboard`
- `Dashboard/GetDateTimeBaseonTimezone`
- `Dashboard/GetEasyPayACHURL`
- `Dashboard/GetEasyPayConsentURL`
- `Dashboard/GetEasyPayURL`
- `Dashboard/GetEncounterType`
- `Dashboard/GetImage`
- `Dashboard/GetMostRecentServices`
- **`Dashboard/GetPateintBalance`**: POST `{}` → `.Dashboard.PaymentSummaryModel[0]` {NetDue, CreditBalance}
- `Dashboard/GetPatientDueAmountWithVendor`
- `Dashboard/GetPatientsFamilyMembers`
- **`Dashboard/GetPracticeSubscriptionDetails`**: GET → array
- `Dashboard/GetSurChargeDetails`
- `Dashboard/GetTelemedicineMail`
- `Dashboard/GetTelemedicineMeetingDetails`
- `Dashboard/GetTopQuickAccessBar`
- `Dashboard/GetUnreadMessage`
- `Dashboard/GetUserPreferenceWidget`
- `Dashboard/InsertUpdateWidgetPreference` ✎
- `Dashboard/PayNowDashboard` ✎
- `Dashboard/RemovePatientImage` ✎
- `Dashboard/ReturnToDashboardwithFamilyID` ✎
- `Dashboard/ReturnToDashboardwithPatientID` ✎
- `Dashboard/SavePatientImage` ✎
- `Dashboard/SetDefaultConsnet` ✎
- `Dashboard/UpdatePatientTelemedicineMeetingDetails` ✎
- `Dashboard/ValidateDuplicateCopayCollection`
- `Dashboard/ValidateRestrictionforCheckInStartingEncounterBasedOnForm`

## EncPatientRestrictAccess

- `EncPatientRestrictAccess/CheckPatientRestriction`
- `EncPatientRestrictAccess/PRAUpdateReasonSave` ✎

## EncounterType

- `EncounterType/BindCPT`

## HealthMaintenance

- `HealthMaintenance/HMaintenance`

## History

- `History/DisplayHistoryTab`

## Immunization

- `Immunization/Immunization`

## LabResults

- `LabResults/Index`

## Messages

- `Messages/ComposeEmail` ✎
- `Messages/DeleteMessageDetail` ✎
- `Messages/GetComposeDetailForReply`
- `Messages/GetComposeMessageDetail`
- `Messages/GetFormDetailByID`
- `Messages/GetMessage`
- **`Messages/GetMessageDetail`**: GET `toDoChildId todoMasaterId` (sic) `type=inbox` → `{MessageDetail, MessageAttachments[], PracticeName}`; likely marks an unread message read
- `Messages/GetMessageInstructionMessage`
- **`Messages/GetMessages`**: GET `messageType` (1 unread / 2 read / 4 sent) `searchStr hasAttachment IsArchived` + DataTables `draw start length` → `{data[],recordsTotal,UnreadMessagesCount}`; side-effect free
- `Messages/GetToDoAttachments`
- **`Messages/GetUnreadMessages`**: GET `pageSize sortBy searchStr hasAttachment` → counts + `ViewHtmlResult` (HTML); prefer GetMessages?messageType=1
- `Messages/LoadComposeMessageDetail`
- `Messages/ReplySendEmail` ✎
- `Messages/UploadFiles` ✎

## OnlinePaymentLog

- `OnlinePaymentLog/DeleteConsentData` ✎
- `OnlinePaymentLog/GetEasyPayPaymentReceiptForEmail`
- `OnlinePaymentLog/GetPatientConsent`
- `OnlinePaymentLog/GetPatientConsentForm`
- `OnlinePaymentLog/GetPatientConsents`
- `OnlinePaymentLog/Index`
- `OnlinePaymentLog/IsConsentExists`
- `OnlinePaymentLog/OpenPDFFileInPDFViewer`
- `OnlinePaymentLog/SavePatientConsent` ✎
- `OnlinePaymentLog/SendReciept` ✎
- `OnlinePaymentLog/UpdateToPreventDelegateAccessCard` ✎

## PatientAppointment

- `PatientAppointment/CancelBookAppoinment` ✎
- `PatientAppointment/ConfirmBookAppoinment`
- `PatientAppointment/GetCheckInConfirmationFromPatientPortal`
- `PatientAppointment/GetCheckInVisitCopayValidationData`
- `PatientAppointment/GetCheckInVisitPatientSignature`
- `PatientAppointment/GetPatientVisitDetailsForCheckIn`
- `PatientAppointment/GetPatientWaitlistPendingDetail`
- `PatientAppointment/GetTokenAndVerify`
- `PatientAppointment/GetWaitListPatientDetail`
- `PatientAppointment/GetWaitListPatientInfo`
- `PatientAppointment/PatientWaitListAppoinmentInfo`
- `PatientAppointment/SaveAppointmentCheckinStatusUpdatePayer` ✎
- `PatientAppointment/UpdateVisitStatusCheckIn` ✎

## PatientDocument

- `PatientDocument/DeletePDFFile` ✎
- **`PatientDocument/GetAllNodes`**: POST `{}` → `.TreeData[]`
- **`PatientDocument/GetAllPatientDocs`**: POST `{}` → `.Files[]`
- `PatientDocument/GetCommonInstructionMessage`
- `PatientDocument/GetFile`
- `PatientDocument/GetFileSource`
- `PatientDocument/GetHealthFormFileList`
- **`PatientDocument/GetPatientFromList`**: POST `{}` → `.PatientFormcollection[]` (Status Sent = pending); records carry a password hash + template HTML, so project
- **`PatientDocument/GetSurveyFromList`**: POST `{}` → `.SurveyFormcollection[]` (empty here; surveys live in SurveyForms/GetReceivedSurveyForms)
- `PatientDocument/SaveDocumentRequest` ✎

## PatientFinancial

- `PatientFinancial/Ledger`

## PatientProfile

- `PatientProfile/DeletePatientAdditionalEmployerDetails` ✎
- `PatientProfile/EditPatientAdditionalEmployerDetails` ✎
- `PatientProfile/FileUploadPhoto` ✎
- `PatientProfile/FileUploadPhotoPath` ✎
- `PatientProfile/GetAdditionalContactDetails`
- `PatientProfile/GetAddressDetails`
- `PatientProfile/GetEmergencyContactDetails`
- `PatientProfile/GetGrantInformationData`
- `PatientProfile/GetGuarantorContactDetails`
- `PatientProfile/GetInsurance`
- `PatientProfile/GetPatientAdditionalEmployerDetails`
- `PatientProfile/GetPatientCareTeamData`
- `PatientProfile/GetPatientContactDetailsHistory`
- `PatientProfile/GetPatientDetailHistoryLogs`
- **`PatientProfile/GetPatientDetails`**: POST `{}` → `.PatientDetail` (~540 KB: picklists + photo; project scalars)
- `PatientProfile/GetPatientPreferences`
- `PatientProfile/GetPatientSignature`
- `PatientProfile/GetPortalContactDetails`
- `PatientProfile/GetPrimaryContactId`
- `PatientProfile/InsuranceCardRemoveYes` ✎
- `PatientProfile/InsuranceInti`
- `PatientProfile/SaveFiles` ✎
- `PatientProfile/SaveInsrurance` ✎
- `PatientProfile/SaveInsuranceCardImages` ✎
- `PatientProfile/SavePDAdditionalDetails` ✎
- `PatientProfile/SavePatientAdditionalEmployerDetails` ✎
- `PatientProfile/SavePatientSignature` ✎
- `PatientProfile/TransferPatientAdditionalEmployerDetails`
- `PatientProfile/UpdateInsrurance` ✎
- `PatientProfile/UpdatePatientDetails` ✎
- `PatientProfile/UpdatePatientPreferences` ✎
- `PatientProfile/UpdatePatientTimeZone` ✎
- `PatientProfile/UpdateSessionTimeOut` ✎

## PatientScheduler

- `PatientScheduler/BindFacilities`
- `PatientScheduler/BindGenderList`
- `PatientScheduler/BindLanguageProficiency`
- `PatientScheduler/BindProvider`
- `PatientScheduler/BindProviders`
- `PatientScheduler/BindSchedulerSlots`
- `PatientScheduler/BindServiceOffered`
- `PatientScheduler/CancelRequestAppointment` ✎
- `PatientScheduler/CheckOutStandingPatientBalanceBookingAppointments` ✎
- **`PatientScheduler/FutureAppiontmentDetails`**: POST `{"pageOptions":{"PageSize":20,"CurrentPage":1},"sortOptions":{"Field":"VISITDATETIME","Direction":"ASC"}}` → `.currentAppointment.{Appointment[],TotalRows}`
- `PatientScheduler/GetAppointmentRequestDetails`
- `PatientScheduler/GetNextAppointmentAvailability`
- `PatientScheduler/GetReasonAsListAndProviderSearchBy`
- `PatientScheduler/GetSchedulerVisitTypeSlots`
- `PatientScheduler/GetVisitDetails`
- `PatientScheduler/GetWeeklyAppointments`
- `PatientScheduler/MonthlyAppointments`
- **`PatientScheduler/PastAppiontmentDetails`**: POST, same body as Future (Direction DESC)
- `PatientScheduler/SaveAppointmentDetails` ✎
- `PatientScheduler/SaveAppointmentReq` ✎

## PatientSearch

- `PatientSearch/Index`

## PatientStatementsReport

- `PatientStatementsReport/Index`

## PaymentReceipt

- `PaymentReceipt/PaymentReceipt`

## RefillPrescription

- `RefillPrescription/RefillPrescription`

## Registration

- `Registration/GetCountyList`
- `Registration/GetPayerList`
- `Registration/GetRaceList`
- `Registration/GetZipCodeList`

## SessionTimeout

- `SessionTimeout/SessionTimeOut`

## SurveyForms

- `SurveyForms/AddFamilyProgramSurvey` ✎
- `SurveyForms/AddPatientSatisfactionSurvey` ✎
- `SurveyForms/AddPostTreatment` ✎
- `SurveyForms/AddTransferDischargeSurvey` ✎
- `SurveyForms/GetOldSurveyFormsById`
- `SurveyForms/GetOldSurveyFormsDetailsById`
- **`SurveyForms/GetReceivedSurveyForms`**: GET → HTML `<tr>` rows (name, ReceivedDate); onclick holds a sign-in token
- `SurveyForms/GetSubmittedSurveyForms`
- `SurveyForms/InsertPatientSelfReport` ✎

## TreatmentPlan

- `TreatmentPlan/ValidateModifierCode`

## TreatmentPlanConfig

- `TreatmentPlanConfig/BindModifier`

## User

- `User/UserDetails`

