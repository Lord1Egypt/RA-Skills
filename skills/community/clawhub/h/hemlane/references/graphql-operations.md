# Hemlane GraphQL operations from HAR files

## BulkGetVendorProfiles
- Seen: 4 time(s)
- HAR files: tenant-reply_hemlane.com.har
- Sample variables:
```json
{
  "userIds": [
    "b0d233d3-d71e-4d8b-967d-2c17781340ae",
    "3cb297be-8425-42fe-afbf-80b1eb6fc324",
    "b0d233d3-d71e-4d8b-967d-2c17781340ae",
    "689e8aa9-0640-461c-bdb4-1cc6d1d86986",
    "b0d233d3-d71e-4d8b-967d-2c17781340ae",
    "689e8aa9-0640-461c-bdb4-1cc6d1d86986",
    "321ad27c-2d09-49cf-a27b-6fd124a23241",
    "b0d233d3-d71e-4d8b-967d-2c17781340ae",
    "3cb297be-8425-42fe-afbf-80b1eb6fc324",
    "3cb297be-8425-42fe-afbf-80b1eb6fc324"
  ]
}
```
- Sample query excerpt:
```graphql
query BulkGetVendorProfiles($userIds: [ID!]!) {
  bulkGetVendorProfiles(userIds: $userIds) {
    id
    profileImageUrl
    userId
    __typename
  }
}

```

## FinancialsScheduledActionPanelStats
- Seen: 2 time(s)
- HAR files: requests_hemlane.com.har, transactions_hemlane.com.har
- Sample variables:
```json
{
  "paymentCategoryId": null,
  "paymentSubcategoryId": null,
  "propertyId": null,
  "propertyUnitId": null,
  "portfolioId": null,
  "ownerUserId": null,
  "sourceTenantGroupId": null,
  "sourceUserId": null,
  "destinationUserId": null,
  "dueDateBegin": null,
  "dueDateEnd": null,
  "status": "all-active"
}
```
- Sample query excerpt:
```graphql
query FinancialsScheduledActionPanelStats($propertyId: ID, $propertyUnitId: ID, $portfolioId: ID, $ownerUserId: ID, $sourceUserId: ID, $sourceTenantGroupId: ID, $paymentCategoryId: ID, $paymentSubcategoryId: ID, $sourceType: TransactionSourceType, $destinationUserId: ID, $dueDateBegin: ISO8601DateTime, $dueDateEnd: ISO8601DateTime, $status: String) {
  ownerTransactionSummary(propertyId: $propertyId, propertyUnitId: $propertyUnitId, portfolioId: $portfolioId, ownerUserId: $ownerUserId, sourceUserId: $sourceUserId, sourceTenantGroupId: $sourceTenantGroupId, paymentCategoryId: $paymentCategoryId, paymentSubcategoryId: $paymentSubcategoryId, sourceType: $sourceType, destinationUserId: $destinationUserId, dueDateBegin: $dueDateBegin, dueDateEnd: $dueDateEnd, status: $status) {
    balanceDue
    __typename
  }
}

```

## GetPlaidSyncItems
- Seen: 1 time(s)
- HAR files: transactions_hemlane.com.har
- Sample variables:
```json
{}
```
- Sample query excerpt:
```graphql
query GetPlaidSyncItems {
  plaidItems {
    id
    externalItemId
    institutionName
    transactionSyncEnabled
    authRequired
    expiresAt
    user {
      id
      email
      __typename
    }
    plaidAccounts {
      id
      externalAccountId
      niceName
      name
      mask
      accountType
      subtype
      transactionSyncEnabled
      historicalSyncStartAt
      properties {
        id
        nickname
        __typename
      }
      propertyUnits {
        id
        nicknameWithUnit
        __typename
      }
      __typename
    }
    __typename
  }
}

```

## HubspotFormSubmit
- Seen: 1 time(s)
- HAR files: refer_hemlane.com.har
- Sample variables:
```json
{
  "input": {
    "fields": [
      {
        "name": "firstname",
        "value": "Mike"
      },
      {
        "name": "lastname",
        "value": "Hugs"
      },
      {
        "name": "phone",
        "value": "8018824174"
      },
      {
        "name": "email",
        "value": "michael@michaelahuggins.com"
      },
      {
        "name": "referrername",
        "value": "Earl Co (ECO Systems)"
      },
      {
        "name": "referreremail",
        "value": "ecosystemspm@gmail.com"
      }
    ],
    "formId": "5e905969-3188-4c3a-ba74-519d43a39761",
    "context": {
      "pageUri": "https://www.hemlane.com/dashboards/owner/"
    }
  }
}
```
- Sample query excerpt:
```graphql
mutation HubspotFormSubmit($input: HubspotFormSubmitInput!) {
  hubspotFormSubmit(input: $input) {
    hubspotFormSubmission {
      id
      __typename
    }
    errors {
      base
      __typename
    }
    __typename
  }
}

```

## LogView
- Seen: 2 time(s)
- HAR files: tenant-reply_hemlane.com.har
- Sample variables:
```json
{
  "viewloggableId": "1b45d37c-144a-4106-b16e-5f0cec4f57cd",
  "viewloggableType": "TenantGroup"
}
```
- Sample query excerpt:
```graphql
mutation LogView($viewloggableType: String!, $viewloggableId: ID!) {
  logView(input: {viewloggableType: $viewloggableType, viewloggableId: $viewloggableId}) {
    success
    __typename
  }
}

```

## LogViewOnMount
- Seen: 1 time(s)
- HAR files: work-order_hemlane.com.har
- Sample variables:
```json
{
  "input": {
    "viewloggableId": "d05b854e-eee7-46e1-9e48-e280f16477ed",
    "viewloggableType": "MaintenanceWorkOrder"
  }
}
```
- Sample query excerpt:
```graphql
mutation LogViewOnMount($input: LogViewCreateInput!) {
  logView(input: $input) {
    clientMutationId
    success
    __typename
  }
}

```

## MCDashboardMaintenanceWorkOrderSchedulingContacts
- Seen: 2 time(s)
- HAR files: work-order_hemlane.com.har
- Sample variables:
```json
{
  "id": "d05b854e-eee7-46e1-9e48-e280f16477ed"
}
```
- Sample query excerpt:
```graphql
query MCDashboardMaintenanceWorkOrderSchedulingContacts($id: ID!) {
  maintenanceWorkOrder(id: $id) {
    id
    maintenanceRequest {
      id
      maintenanceRequestDefaultSchedulingContacts {
        edges {
          node {
            id
            fullName
            formattedPhoneNumber
            user {
              id
              fullName
              formattedPhoneNumber
              __typename
            }
            tenant {
              id
              invitationName
              formattedPhoneNumber
              user {
                id
                fullName
                formattedPhoneNumber
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
      property {
        id
        acceptedPropertyMembers {
          edges {
            node {
              id
              user {
                id
                fullName
                formattedPhoneNumber
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
      activeTenants {
        edges {
          node {
            id
            user {
              id
              fullName
              formattedPhoneNumber
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
  
```

## MaintenanceGetCurrentUser
- Seen: 2 time(s)
- HAR files: work-order_hemlane.com.har
- Sample variables:
```json
{}
```
- Sample query excerpt:
```graphql
query MaintenanceGetCurrentUser {
  currentUser {
    id
    userType
    paymentCredential {
      id
      paymentAccountsV2 {
        id
        accountName
        accountLast4
        depositEnabled
        __typename
      }
      __typename
    }
    hasAdminRole(roles: [["maintenance"]])
    __typename
  }
  serviceRequestCategories(nonDeprecated: true) {
    value
    label
    __typename
  }
  maintenanceServiceRequestCategories(nonDeprecated: true) {
    value
    label
    __typename
  }
  imgixDomain
}

```

## MyAppNotificationStats
- Seen: 6 time(s)
- HAR files: maintenance_update_hemlane.com.har, refer_hemlane.com.har, requests_hemlane.com.har, tenant-reply_hemlane.com.har, work-order_hemlane.com.har
- Sample variables:
```json
{}
```
- Sample query excerpt:
```graphql
query MyAppNotificationStats($propertyId: ID) {
  myAppNotificationStats(propertyId: $propertyId) {
    unreadCount
    totalCount
    __typename
  }
  currentUser {
    id
    __typename
  }
}

```

## ODDashboardConsolidatedQuery
- Seen: 1 time(s)
- HAR files: refer_hemlane.com.har
- Sample variables:
```json
{}
```
- Sample query excerpt:
```graphql
query ODDashboardConsolidatedQuery($status: TaskStatus, $isActive: Boolean, $first: Int) {
  tenantsDashboardStats {
    expiringIn30
    expiringIn60
    expiringIn90
    occupiedUnitCount
    totalUnitCount
    __typename
  }
  prospectiveTenantInfo {
    id
    inquiryLeadsCount
    qualificationTenantGroupsCount
    moveInTenantGroupsCount
    __typename
  }
  adminUser {
    id
    __typename
  }
  currentUser {
    id
    trialEndDate
    isStripeSubscriptionStatusDelinquent
    isOnStarterPlan
    freePlanModalAcknowledged
    metaActiveBillToUnitCount
    metaAgentBillToUnitCount
    stripeSubscriptionInvoiceStatusStr
    stripeSubscriptionStatus
    shouldTakeCareOfSubscriptionPayments
    myProperties(isDeleted: false, isBillTo: true) {
      data {
        id
        addressLat
        addressLng
        packageType
        billToUser {
          id
          isOnStarterPlan
          __typename
        }
        __typename
      }
      __typename
    }
    currentUserInfo {
      id
      viewAsUsers {
        id
        fullName
        email
        __typename
      }
      __typename
    }
    __typename
  }
  maintenanceServiceRequestCategories(nonDeprecated: true) {
    value
    label
    __typename
  }
  paginatedMaintenanceRequests(isOpen: true, pagination: {page: 1, limit: 2}, updatedAtOrder: Descending) {
    data {
      id
      property {
        id
        nickname
        __typename
      }
      category
      title
      createdAt
      updatedAt
```

## ODFinancialsSummaryOwnerFinancialsSummary
- Seen: 2 time(s)
- HAR files: refer_hemlane.com.har
- Sample variables:
```json
{
  "viewAsUserId": "3cb297be-8425-42fe-afbf-80b1eb6fc324",
  "type": "MoneyIn"
}
```
- Sample query excerpt:
```graphql
query ODFinancialsSummaryOwnerFinancialsSummary($type: OwnerFinancialsSummaryType!, $viewAsUserId: ID!) {
  currentUser {
    id
    currentUserInfo {
      id
      ownerFinancialsSummary(type: $type, viewAsUserId: $viewAsUserId) {
        id
        dueDateYearMonth
        successAmount
        pendingAmount
        pastDueAmount
        futureDueAmount
        uncollectedAmount
        __typename
      }
      __typename
    }
    __typename
  }
}

```

## ODGetContextValues
- Seen: 7 time(s)
- HAR files: maintenance_update_hemlane.com.har, refer_hemlane.com.har, requests_hemlane.com.har, tenant-reply_hemlane.com.har, work-order_hemlane.com.har
- Sample variables:
```json
{}
```
- Sample query excerpt:
```graphql
query ODGetContextValues {
  paymentCategories {
    id
    label
    purpose
    isRent
    sortIndex
    paymentSubcategories {
      id
      label
      shortLabel
      purpose
      isGlobal
      sortIndex
      __typename
    }
    __typename
  }
  currentUser {
    id
    evictionGuardEnabled
    metaAssociatedUnitCount
    metaBasicAllBillToUnitCount
    metaEssentialAllBillToUnitCount
    metaCompleteAllBillToUnitCount
    email
    firstName
    lastName
    fullName
    vendorProfile {
      id
      profileImageUrl
      __typename
    }
    isStripeSubscriptionStatusDelinquent
    stripeSubscriptionStatus
    stripeSubscriptionId
    activeBillToUnitCount: metaActiveBillToUnitCount
    isOnStarterPlan
    agentBillToUnitCount: metaAgentBillToUnitCount
    metaAssociatedUnitCount
    metaAssociatedAgentUnitCount
    metaBasicAllBillToUnitCount
    metaCompleteAllBillToUnitCount
    metaEssentialAllBillToUnitCount
    evictionGuardEnabled
    ownerAccountType
    extraFeatures
    authyVerified
    trialEndDate
    trialStartDate
    createdAt
    rbpOwnerEnrolled
    onboardingConfig {
      unitSelectionComplete
      __typename
    }
    onboardingSteps {
      financials
      marketing
      prospectiveTenants
      tenantsAndLeases
      __typename
    }
    manageablePropertiesCache {
      id
      hasCanManageProperty
      hasCanManageTenancy
      hasCanManageServiceProviders
      hasCanManageRequests
      hasCanManageFinancials
      hasCanManageSer
```

## ODMaintenanceRequests
- Seen: 1 time(s)
- HAR files: tenant-reply_hemlane.com.har
- Sample variables:
```json
{
  "isOpen": false,
  "status": "Open",
  "propertyId": null,
  "propertyUnitId": null,
  "portfolioId": null,
  "ownerUserId": null,
  "page": 1
}
```
- Sample query excerpt:
```graphql
query ODMaintenanceRequests($status: MaintenanceRequestStatus, $isOpen: Boolean!, $propertyId: ID, $propertyUnitId: ID, $portfolioId: ID, $ownerUserId: ID, $page: Int) {
  maintenanceServiceRequestCategories(nonDeprecated: true) {
    value
    label
    __typename
  }
  paginatedMaintenanceRequests(status: $status, isOpen: $isOpen, propertyId: $propertyId, propertyUnitId: $propertyUnitId, portfolioId: $portfolioId, ownerUserId: $ownerUserId, pagination: {page: $page, limit: 12}) {
    data {
      workOrders {
        edges {
          node {
            assigneeUser {
              fullName
              id
              __typename
            }
            assigneeServiceProvider {
              fullName
              id
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
      lastOwnerVisibleComment {
        body
        createdBy {
          id
          userType
          fullName
          isAdmin
          vendorProfile {
            profileImageUrl
            __typename
          }
          __typename
        }
        createdAt
        __typename
      }
      coordinatedBy {
        id
        __typename
      }
      id
      title
      description
      category
      status
      token
      referenceNumber
      isHemlaneCoordinated
      maintenanceRequestComments(first: 1) {
        edges {
          node {
            body
            createdAt
            createdBy {
      
```

## ODProspectiveTenantGroupMessageCreate
- Seen: 1 time(s)
- HAR files: tenant-reply_hemlane.com.har
- Sample variables:
```json
{
  "input": {
    "tenantGroupId": "53cf1ff2-56d7-41e5-a0bd-9d3cc2a99aab",
    "body": "Good morning Tiffany, as discussed, it seems your $890 December payment bounced and was reversed by Hemlane. You may see a new request for it to be reprocessed in your Financials tab. Thanks!",
    "notifyImmediately": true,
    "isOwnerPrivate": false,
    "attachmentUrl": null
  }
}
```
- Sample query excerpt:
```graphql
mutation ODProspectiveTenantGroupMessageCreate($input: TenantGroupMessageAdd2Input!) {
  tenantGroupMessageAdd: tenantGroupMessageAdd2(input: $input) {
    tenantGroupMessage {
      id
      body
      createdAt
      createdByInfo {
        id
        name
        email
        type
        __typename
      }
      __typename
    }
    errors {
      base
      body
      createdByInfo
      tenantGroup
      __typename
    }
    __typename
  }
}

```

## ODTenantsAndLeasesBucketCounts
- Seen: 2 time(s)
- HAR files: tenant-reply_hemlane.com.har
- Sample variables:
```json
{
  "propertyId": null,
  "propertyUnitId": null,
  "portfolioId": null,
  "ownerUserId": null,
  "tenantGroupStatus": [
    "Active"
  ]
}
```
- Sample query excerpt:
```graphql
query ODTenantsAndLeasesBucketCounts($propertyId: ID, $propertyUnitId: ID, $portfolioId: ID, $ownerUserId: ID, $tenantGroupStatus: [TenantGroupStatus!], $tenantSearch: String, $hasUnreadMessages: Boolean, $hasOutstandingBalance: Boolean, $hasRegisteredTenant: Boolean, $hasRecurringRent: Boolean, $hasBankAccount: Boolean, $missingLeaseDocuments: Boolean) {
  tenantsAndLeasesBucketCounts(propertyId: $propertyId, propertyUnitId: $propertyUnitId, portfolioId: $portfolioId, ownerUserId: $ownerUserId, tenantGroupStatus: $tenantGroupStatus, tenantSearch: $tenantSearch, hasUnreadMessages: $hasUnreadMessages, hasOutstandingBalance: $hasOutstandingBalance, hasRegisteredTenant: $hasRegisteredTenant, hasRecurringRent: $hasRecurringRent, hasBankAccount: $hasBankAccount, missingLeaseDocuments: $missingLeaseDocuments) {
    allLeases
    newMoveIns
    endingSoon
    moveOuts
    __typename
  }
}

```

## ODTenantsAndLeasesGetTenantMessagesStatsLog
- Seen: 2 time(s)
- HAR files: tenant-reply_hemlane.com.har
- Sample variables:
```json
{}
```
- Sample query excerpt:
```graphql
query ODTenantsAndLeasesGetTenantMessagesStatsLog($statsLogId: ID) {
  tenantMessagesStatsLog(statsLogId: $statsLogId) {
    id
    tag
    logStr
    __typename
  }
}

```

## ODTenantsAndLeasesTenantGroups
- Seen: 2 time(s)
- HAR files: tenant-reply_hemlane.com.har
- Sample variables:
```json
{
  "propertyId": null,
  "propertyUnitId": null,
  "portfolioId": null,
  "ownerUserId": null,
  "tenantGroupStatus": [
    "Active"
  ],
  "pagination": {
    "page": 1,
    "limit": 25
  },
  "leaseFilter": "all",
  "sortBy": "endDate"
}
```
- Sample query excerpt:
```graphql
query ODTenantsAndLeasesTenantGroups($propertyId: ID, $propertyUnitId: ID, $portfolioId: ID, $ownerUserId: ID, $tenantGroupStatus: [TenantGroupStatus!], $pagination: PagedPaginationInput, $leaseFilter: String, $sortBy: String, $tenantSearch: String, $hasUnreadMessages: Boolean, $hasOutstandingBalance: Boolean, $hasRegisteredTenant: Boolean, $hasRecurringRent: Boolean, $hasBankAccount: Boolean, $missingLeaseDocuments: Boolean) {
  tenantsAndLeasesTenantGroups(propertyId: $propertyId, propertyUnitId: $propertyUnitId, portfolioId: $portfolioId, ownerUserId: $ownerUserId, tenantGroupStatus: $tenantGroupStatus, pagination: $pagination, leaseFilter: $leaseFilter, sortBy: $sortBy, tenantSearch: $tenantSearch, hasUnreadMessages: $hasUnreadMessages, hasOutstandingBalance: $hasOutstandingBalance, hasRegisteredTenant: $hasRegisteredTenant, hasRecurringRent: $hasRecurringRent, hasBankAccount: $hasBankAccount, missingLeaseDocuments: $missingLeaseDocuments) {
    pageInfo {
      page
      totalCount
      totalPages
      __typename
    }
    data {
      id
      status
      evictionStatus
      terminationDate
      lastMessageCreated
      unreadMessagesCount
      tenantLedgerBalanceInCents
      hasRegisteredTenant
      hasRecurringRent
      hasBankAccount
      propertyDocuments {
        id
        docType
        __typename
      }
      lease {
        id
        status
        monthlyRentInCents
        endDate
        endDateAction
        leaseRenewal {
          id
      
```

## ODTenantsIndexNewPermissions
- Seen: 2 time(s)
- HAR files: tenant-reply_hemlane.com.har
- Sample variables:
```json
{
  "propertyId": null,
  "portfolioId": null
}
```
- Sample query excerpt:
```graphql
query ODTenantsIndexNewPermissions($propertyId: ID, $portfolioId: ID) {
  currentUser {
    id
    canManageTenancyPropertiesCount(propertyId: $propertyId, portfolioId: $portfolioId, includeArchived: false)
    canManageProspectiveTenancyPropertiesCount(propertyId: $propertyId, portfolioId: $portfolioId, includeArchived: false)
    __typename
  }
}

```

## OwnerDashboardMaintenanceMaintenanceRequest
- Seen: 4 time(s)
- HAR files: maintenance_update_hemlane.com.har, work-order_hemlane.com.har
- Sample variables:
```json
{
  "id": "8609a66f-8403-483c-aaef-fecfa199c9bd"
}
```
- Sample query excerpt:
```graphql
query OwnerDashboardMaintenanceMaintenanceRequest($id: ID!) {
  currentUser {
    id
    userType
    email
    fullName
    formattedPhoneNumber
    __typename
  }
  maintenanceCoordinator {
    id
    vendorProfile {
      id
      profileImageUrl
      __typename
    }
    __typename
  }
  serviceRequestCategories(nonDeprecated: true) {
    value
    label
    __typename
  }
  maintenanceServiceRequestCategories(nonDeprecated: true) {
    value
    label
    __typename
  }
  maintenanceRequest(id: $id) {
    id
    troubleshooting
    title
    description
    status
    category
    referenceNumber
    token
    packageType
    isHemlaneCoordinated
    photos {
      totalCount
      __typename
    }
    openWorkOrders {
      edges {
        node {
          id
          photos {
            totalCount
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    managedBy {
      id
      fullName
      formattedPhoneNumber
      userType
      __typename
    }
    coordinatedBy {
      id
      fullName
      formattedPhoneNumber
      __typename
    }
    turnoverManagedBy {
      id
      fullName
      formattedPhoneNumber
      __typename
    }
    property {
      id
      addressStreet
      addressCity
      addressState
      addressZip
      maintenanceThreshold
      emergencyMaintenanceThreshold
      description
      timeZone
      maintenanceBillingStatus
      billToUser {
        id
        fullN
```

## OwnerDashboardMaintenanceMaintenanceRequestCommentCreate
- Seen: 2 time(s)
- HAR files: maintenance_update_hemlane.com.har, work-order_hemlane.com.har
- Sample variables:
```json
{
  "input": {
    "maintenanceRequestId": "8609a66f-8403-483c-aaef-fecfa199c9bd",
    "body": "This task can be closed. Everything is fixed.",
    "isHiddenFromTenants": true,
    "isHiddenFromOwners": false
  }
}
```
- Sample query excerpt:
```graphql
mutation OwnerDashboardMaintenanceMaintenanceRequestCommentCreate($input: MaintenanceRequestCommentCreateInput!) {
  maintenanceRequestCommentCreate(input: $input) {
    maintenanceRequestComment {
      id
      body
      isHiddenFromTenants
      createdAt
      createdBy {
        id
        fullName
        isAdmin
        vendorProfile {
          id
          profileImageUrl
          __typename
        }
        __typename
      }
      __typename
    }
    errors {
      base
      body
      maintenanceRequestId
      isHiddenFromTenants
      __typename
    }
    __typename
  }
}

```

## OwnerDashboardMaintenanceMaintenanceRequestComments
- Seen: 4 time(s)
- HAR files: maintenance_update_hemlane.com.har, work-order_hemlane.com.har
- Sample variables:
```json
{
  "maintenanceRequestId": "8609a66f-8403-483c-aaef-fecfa199c9bd"
}
```
- Sample query excerpt:
```graphql
query OwnerDashboardMaintenanceMaintenanceRequestComments($maintenanceRequestId: ID!) {
  maintenanceRequestComments(maintenanceRequestId: $maintenanceRequestId) {
    edges {
      cursor
      node {
        id
        body
        isHiddenFromTenants
        createdAt
        createdBy {
          id
          fullName
          isAdmin
          vendorProfile {
            id
            profileImageUrl
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    pageInfo {
      startCursor
      endCursor
      hasPreviousPage
      hasNextPage
      __typename
    }
    __typename
  }
}

```

## OwnerDashboardMaintenanceMaintenanceRequestPhotos
- Seen: 1 time(s)
- HAR files: work-order_hemlane.com.har
- Sample variables:
```json
{
  "id": "8609a66f-8403-483c-aaef-fecfa199c9bd"
}
```
- Sample query excerpt:
```graphql
query OwnerDashboardMaintenanceMaintenanceRequestPhotos($id: ID!) {
  maintenanceRequest(id: $id) {
    id
    openWorkOrders {
      edges {
        node {
          id
          assigneeUser {
            id
            fullName
            __typename
          }
          assigneeServiceProvider {
            id
            contactName
            companyName
            __typename
          }
          photos {
            totalCount
            edges {
              node {
                id
                url
                downloadUrl
                previewUrl
                hasPreview
                isSupportedImage
                caption
                createdByName
                createdAt
                fileName
                canDelete
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    photos {
      totalCount
      edges {
        node {
          id
          url
          downloadUrl
          previewUrl
          hasPreview
          isSupportedImage
          caption
          createdByName
          createdAt
          fileName
          canDelete
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}

```

## OwnerDashboardMaintenanceMaintenanceRequestUsers
- Seen: 4 time(s)
- HAR files: maintenance_update_hemlane.com.har, work-order_hemlane.com.har
- Sample variables:
```json
{
  "id": "8609a66f-8403-483c-aaef-fecfa199c9bd"
}
```
- Sample query excerpt:
```graphql
query OwnerDashboardMaintenanceMaintenanceRequestUsers($id: ID!) {
  maintenanceRequest(id: $id) {
    id
    maintenanceRequestUsers {
      edges {
        node {
          id
          role
          user {
            id
            userType
            fullName
            email
            formattedPhoneNumber
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}

```

## OwnerDashboardMaintenanceMaintenanceRequestWorkOrders
- Seen: 4 time(s)
- HAR files: maintenance_update_hemlane.com.har, work-order_hemlane.com.har
- Sample variables:
```json
{
  "id": "8609a66f-8403-483c-aaef-fecfa199c9bd"
}
```
- Sample query excerpt:
```graphql
query OwnerDashboardMaintenanceMaintenanceRequestWorkOrders($id: ID!) {
  maintenanceRequest(id: $id) {
    id
    status
    property {
      id
      timeZone
      __typename
    }
    workOrders {
      edges {
        node {
          id
          assigneeUser {
            id
            fullName
            companyName
            email
            formattedPhoneNumber
            __typename
          }
          assigneeServiceProvider {
            id
            contactName
            companyName
            email
            phoneNumber
            formattedPhoneNumber
            email2
            phoneNumber2
            formattedPhoneNumber2
            __typename
          }
          title
          referenceNumber
          status
          scheduledDate
          localScheduledDateStart
          localScheduledDateEnd
          createdAt
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}

```

## OwnerMaintenanceWorkOrder
- Seen: 2 time(s)
- HAR files: work-order_hemlane.com.har
- Sample variables:
```json
{
  "id": "d05b854e-eee7-46e1-9e48-e280f16477ed"
}
```
- Sample query excerpt:
```graphql
query OwnerMaintenanceWorkOrder($id: ID!) {
  currentUser {
    id
    email
    userType
    currentUserServiceProvider {
      id
      __typename
    }
    __typename
  }
  maintenanceCoordinator {
    id
    formattedPhoneNumber
    __typename
  }
  maintenanceWorkOrder(id: $id) {
    title
    referenceNumber
    billToPaymentAccount
    version
    assigneeUser {
      id
      fullName
      formattedPhoneNumber
      email
      __typename
    }
    assigneeServiceProvider {
      id
      contactName
      formattedPhoneNumber
      email
      formattedPhoneNumber2
      email2
      companyName
      status
      usePremiumBilling
      isHemlaneServiceProvider
      token
      serviceProviderUser {
        id
        __typename
      }
      __typename
    }
    id
    instructions
    invoiceUploads {
      id
      paymentRequest {
        id
        privacyTransaction {
          id
          __typename
        }
        __typename
      }
      __typename
    }
    billToUser {
      id
      email
      fullName
      formattedPhoneNumber
      mailingAddress
      creditCardStored
      __typename
    }
    maintenanceRequest {
      title
      description
      id
      isHemlaneCoordinated
      managedBy {
        id
        fullName
        formattedPhoneNumber
        __typename
      }
      coordinatedBy {
        id
        fullName
        formattedPhoneNumber
        __typename
      }
      turnoverManagedBy {
        id
        fullName
       
```

## OwnerMaintenanceWorkOrderCommentCreate
- Seen: 1 time(s)
- HAR files: work-order_hemlane.com.har
- Sample variables:
```json
{
  "input": {
    "maintenanceWorkOrderId": "d05b854e-eee7-46e1-9e48-e280f16477ed",
    "body": "I do see the $140 pulled out of this property's account without bouncing or any issues, so it looks like we're good here and this work order can be closed."
  }
}
```
- Sample query excerpt:
```graphql
mutation OwnerMaintenanceWorkOrderCommentCreate($input: MaintenanceWorkOrderCommentCreateInput!) {
  maintenanceWorkOrderCommentCreate(input: $input) {
    maintenanceWorkOrderComment {
      id
      body
      __typename
    }
    errors {
      base
      body
      __typename
    }
    __typename
  }
}

```

## OwnerMaintenanceWorkOrderComments
- Seen: 3 time(s)
- HAR files: work-order_hemlane.com.har
- Sample variables:
```json
{
  "maintenanceWorkOrderId": "d05b854e-eee7-46e1-9e48-e280f16477ed"
}
```
- Sample query excerpt:
```graphql
query OwnerMaintenanceWorkOrderComments($maintenanceWorkOrderId: ID!, $after: String) {
  maintenanceWorkOrderComments(maintenanceWorkOrderId: $maintenanceWorkOrderId, after: $after, first: 30) {
    edges {
      node {
        body
        isPinnedToTop
        isAdminOnly
        createdAt
        createdByInfo {
          name
          __typename
        }
        createdByServiceProvider {
          id
          contactName
          __typename
        }
        createdByUser {
          id
          fullName
          isAdmin
          vendorProfile {
            id
            profileImageUrl
            __typename
          }
          __typename
        }
        createdDuringWorkOrderStatus
        id
        updatedAt
        __typename
      }
      __typename
    }
    pageInfo {
      startCursor
      endCursor
      hasNextPage
      hasPreviousPage
      __typename
    }
    __typename
  }
}

```

## OwnerMaintenanceWorkOrderPhotos
- Seen: 1 time(s)
- HAR files: work-order_hemlane.com.har
- Sample variables:
```json
{
  "id": "d05b854e-eee7-46e1-9e48-e280f16477ed"
}
```
- Sample query excerpt:
```graphql
query OwnerMaintenanceWorkOrderPhotos($id: ID!) {
  maintenanceWorkOrder(id: $id) {
    id
    status
    assigneeUser {
      id
      fullName
      formattedPhoneNumber
      email
      __typename
    }
    assigneeServiceProvider {
      id
      contactName
      formattedPhoneNumber
      email
      companyName
      __typename
    }
    maintenanceRequest {
      id
      isHemlaneCoordinated
      managedBy {
        id
        fullName
        formattedPhoneNumber
        __typename
      }
      __typename
    }
    photos {
      edges {
        node {
          id
          url
          downloadUrl
          previewUrl
          hasPreview
          isSupportedImage
          caption
          createdByName
          createdAt
          fileName
          canDelete
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}

```

## OwnerMaintenanceWorkOrderRequestPhotos
- Seen: 1 time(s)
- HAR files: work-order_hemlane.com.har
- Sample variables:
```json
{
  "id": "d05b854e-eee7-46e1-9e48-e280f16477ed"
}
```
- Sample query excerpt:
```graphql
query OwnerMaintenanceWorkOrderRequestPhotos($id: ID!) {
  maintenanceWorkOrder(id: $id) {
    id
    assigneeUser {
      id
      fullName
      formattedPhoneNumber
      email
      __typename
    }
    assigneeServiceProvider {
      id
      contactName
      formattedPhoneNumber
      email
      companyName
      __typename
    }
    maintenanceRequest {
      id
      isHemlaneCoordinated
      managedBy {
        id
        fullName
        formattedPhoneNumber
        __typename
      }
      photos {
        edges {
          node {
            id
            url
            downloadUrl
            previewUrl
            hasPreview
            isSupportedImage
            caption
            createdByName
            createdAt
            fileName
            canDelete
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}

```

## OwnerTenancyMessages
- Seen: 3 time(s)
- HAR files: tenant-reply_hemlane.com.har
- Sample variables:
```json
{
  "tenantGroupId": "1b45d37c-144a-4106-b16e-5f0cec4f57cd",
  "first": 20
}
```
- Sample query excerpt:
```graphql
query OwnerTenancyMessages($tenantGroupId: ID!, $first: Int, $after: String) {
  tenantGroup(tenantGroupId: $tenantGroupId) {
    property {
      id
      packageType
      isCompleteV2
      activeUnitCount
      billToUser {
        id
        fullName
        isOnStarterPlan
        __typename
      }
      __typename
    }
    __typename
  }
  tenancyMessages(tenantGroupId: $tenantGroupId, first: $first, after: $after) {
    edges {
      cursor
      node {
        id
        body
        createdAt
        createdByInfo {
          id
          email
          name
          type
          __typename
        }
        isSystem
        isOwnerPrivate
        isAdminOnly
        isPinned
        sourceable {
          ... on TenantGroupMessage {
            serviceType
            messageAttachments(first: 10) {
              edges {
                node {
                  id
                  url
                  viewUrl
                  __typename
                }
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
      __typename
    }
    __typename
  }
}

```

## OwnerVendorMaintenanceWorkOrderInvoices
- Seen: 2 time(s)
- HAR files: work-order_hemlane.com.har
- Sample variables:
```json
{
  "invoicable": {
    "id": "d05b854e-eee7-46e1-9e48-e280f16477ed",
    "type": "MaintenanceWorkOrder"
  }
}
```
- Sample query excerpt:
```graphql
query OwnerVendorMaintenanceWorkOrderInvoices($id: ID, $invoicable: InvoicableInput) {
  initialMaintenanceTransactionFeeBasisPoint
  invoiceUploads(id: $id, invoicable: $invoicable) {
    id
    invoicable {
      ... on MaintenanceWorkOrder {
        __typename
        id
        title
      }
      __typename
    }
    amount
    paymentRequest {
      id
      paymentStatus
      amount
      amountConfirmed
      isOverride
      status
      canCancel
      privacyTransaction {
        id
        amount
        __typename
      }
      __typename
    }
    description
    dueDate
    createdAt
    updatedAt
    invoiceUploadDocuments {
      id
      invoiceUploadId
      document
      rank
      createdAt
      updatedAt
      __typename
    }
    __typename
  }
}

```

## PagedFinancialTransactions
- Seen: 1 time(s)
- HAR files: transactions_hemlane.com.har
- Sample variables:
```json
{
  "page": 1,
  "plaidAccountId": null,
  "minAbsAmountInCents": null,
  "maxAbsAmountInCents": null,
  "paymentSubcategoryId": null,
  "paymentCategoryId": null,
  "keyword": null,
  "portfolioId": null,
  "ownerUserId": null,
  "propertyId": null,
  "propertyUnitId": null,
  "view": "all"
}
```
- Sample query excerpt:
```graphql
query PagedFinancialTransactions($page: Int!, $plaidAccountId: ID, $propertyId: ID, $propertyUnitId: ID, $paymentCategoryId: ID, $paymentSubcategoryId: ID, $minAbsAmountInCents: Int, $maxAbsAmountInCents: Int, $minTransactedAt: ISO8601DateTime, $maxTransactedAt: ISO8601DateTime, $keyword: String, $portfolioId: ID, $ownerUserId: ID, $view: FinancialTransactionsView!) {
  financialTransactions(pagination: {page: $page}, plaidAccountId: $plaidAccountId, propertyId: $propertyId, propertyUnitId: $propertyUnitId, paymentCategoryId: $paymentCategoryId, paymentSubcategoryId: $paymentSubcategoryId, minAbsAmountInCents: $minAbsAmountInCents, maxAbsAmountInCents: $maxAbsAmountInCents, minTransactedAt: $minTransactedAt, maxTransactedAt: $maxTransactedAt, textSearch: $keyword, portfolioId: $portfolioId, ownerUserId: $ownerUserId, view: $view) {
    pageInfo {
      page
      totalPages
      totalCount
      __typename
    }
    data {
      id
      amountInCents
      transactedAt
      description
      status
      isHidden
      memo
      documents {
        id
        downloadUrl
        filename
        __typename
      }
      party {
        __typename
        ... on User {
          id
          fullName
          __typename
        }
      }
      counterparty {
        __typename
        ... on TenantGroup {
          id
          tenants {
            id
            user {
              id
              fullName
              __typename
            }
            __typename

```

## TGTenantGroup
- Seen: 3 time(s)
- HAR files: tenant-reply_hemlane.com.har
- Sample variables:
```json
{
  "tenantGroupId": "1b45d37c-144a-4106-b16e-5f0cec4f57cd"
}
```
- Sample query excerpt:
```graphql
query TGTenantGroup($tenantGroupId: ID!) {
  tenantGroup(tenantGroupId: $tenantGroupId) {
    id
    terminationDate
    memberNotes
    isProcessingSetMoveOut
    hasPets
    tenantScreeningRequired
    maxExpectedMoveInDate
    terminationDate
    status
    jurisdiction
    evictionStatus
    onlinePaymentsDisabled
    tenantLedgerBalanceInCents
    overdueRentBalanceInCents: tenantLedgerBalanceInCents(paymentSubcategoryPurpose: "rent", excludeLastDate: true)
    tenantLedgerUncollectibleInCents
    tenantGroupStat {
      checklistCreditSummary {
        averageScore
        processCompleteCount
        requestedCount
        __typename
      }
      screeningRecommendation {
        status
        actual {
          averageCreditScore
          grossIncomePerMonth
          otherIncomePerMonth
          hasEvictions
          __typename
        }
        __typename
      }
      checklistLeaseAgreementSummary {
        docsComplete
        __typename
      }
      __typename
    }
    recurringPaymentRequests {
      id
      amount
      amountInCents
      interval
      monthlyAnchor
      weeklyAnchor
      startDate
      endDate
      confirmedAmount
      status
      allowCreditCard
      singlePaymentRequired
      isSourcePayingProcessingFee
      memo
      lastRequestDueDate
      nextProjectedDueDate
      destinationUser {
        id
        fullName
        __typename
      }
      destinationPaymentAccount {
        id
        accountLast4
        account
```

## TasksCount
- Seen: 3 time(s)
- HAR files: requests_hemlane.com.har
- Sample variables:
```json
{}
```
- Sample query excerpt:
```graphql

      query TasksCount {
        onboardingBankSyncConnectTasks: tasksByType(
          taskType: OnboardingBankSyncConnect          
        ) {
          taskType
          displayRank
          canDefer
          canBulkDefer
          totalCount          
        }
        onboardingConfirmOwnerAddressTasks: tasksByType(
          taskType: OnboardingConfirmOwnerAddress, 
        ) {
          taskType
          displayRank
          canDefer
          canBulkDefer
          totalCount
        }
        onboardingReactivateSubscriptionTasks: tasksByType(
          taskType: OnboardingReactivateSubscription
        ) {
          taskType
          displayRank
          canDefer
          canBulkDefer
          totalCount
        }
        onboardingSetupBankAccountTasks: tasksByType(
          taskType: OnboardingSetupBankAccount
        ) {
          taskType
          displayRank
          canDefer
          canBulkDefer
          totalCount
        }
        onboardingSetupLeasingAgentProfileTasks: tasksByType(
          taskType: OnboardingSetupLeasingAgentProfile
        ) {
          taskType
          displayRank
          canDefer
          canBulkDefer
          totalCount
        }
        onboardingSetupOwnerTypesTasks: tasksByType(
          taskType: OnboardingSetupOwnerTypes
        ) {
          taskType
          displayRank
          canDefer
          canBulkDefer
          totalCount
        }
        onboardingStartSubscriptionTasks: tasksByType(
     
```

## TransactionsNextCursorQuery
- Seen: 2 time(s)
- HAR files: requests_hemlane.com.har, transactions_hemlane.com.har
- Sample variables:
```json
{
  "paymentReferenceNumber": null,
  "dueDateBegin": null,
  "dueDateEnd": null,
  "propertyId": null,
  "propertyUnitId": null,
  "portfolioId": null,
  "ownerUserId": null,
  "pagination": {
    "page": 1,
    "limit": 20
  },
  "status": "all-active",
  "paymentCategoryId": null,
  "paymentSubcategoryId": null,
  "destinationUserId": null,
  "sourceUserId": null,
  "sourceTenantGroupId": null,
  "sortOrder": "desc"
}
```
- Sample query excerpt:
```graphql
query TransactionsNextCursorQuery($pagination: PagedPaginationInput!, $status: String!, $propertyId: ID, $propertyUnitId: ID, $portfolioId: ID, $ownerUserId: ID, $dueDateBegin: DateTime2, $dueDateEnd: DateTime2, $paymentReferenceNumber: String, $recurringPaymentRequestId: ID, $paymentCategoryId: ID, $paymentSubcategoryId: ID, $destinationUserId: ID, $sourceUserId: ID, $sourceTenantGroupId: ID, $sortOrder: String) {
  transactionsNextCursor(pagination: $pagination, status: $status, propertyId: $propertyId, propertyUnitId: $propertyUnitId, portfolioId: $portfolioId, ownerUserId: $ownerUserId, dueDateBegin: $dueDateBegin, dueDateEnd: $dueDateEnd, paymentReferenceNumber: $paymentReferenceNumber, recurringPaymentRequestId: $recurringPaymentRequestId, paymentCategoryId: $paymentCategoryId, paymentSubcategoryId: $paymentSubcategoryId, destinationUserId: $destinationUserId, sourceUserId: $sourceUserId, sourceTenantGroupId: $sourceTenantGroupId, sortOrder: $sortOrder) {
    pageInfo {
      page
      hasNextPage
      hasPreviousPage
      __typename
    }
    data {
      maintenanceWorkOrder {
        id
        assigneeUser {
          id
          fullName
          __typename
        }
        assigneeServiceProvider {
          id
          fullName
          companyName
          __typename
        }
        __typename
      }
      id
      singlePaymentRequired
      allowCreditCard
      amount
      status
      successAmount
      pendingAmount
      initializedAmount
   
```
