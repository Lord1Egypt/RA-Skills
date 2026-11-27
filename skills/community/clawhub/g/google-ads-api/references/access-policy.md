# Google Ads access policy

An access policy limits which endpoints Google Ads connections may call through Maton. Google Ads doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-ads#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Google Ads: its 48 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create google-ads --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "POST", "path": "v24/audienceInsights:listInsightsEligibleDates"},
    {"method": "GET", "path": "v24/customers/{id}/batchJobs/{id}:listResults"},
    {"method": "GET", "path": "v24/customers/{id}/campaignDrafts/{id}:listAsyncErrors"},
    {"method": "GET", "path": "v24/customers/{id}/getIdentityVerification"},
    {"method": "POST", "path": "v24/customers/{id}:generateAdGroupThemes"},
    {"method": "POST", "path": "v24/customers/{id}:generateAudienceCompositionInsights"},
    {"method": "POST", "path": "v24/customers/{id}:generateAudienceDefinition"},
    {"method": "POST", "path": "v24/customers/{id}:generateAudienceOverlapInsights"},
    {"method": "POST", "path": "v24/customers/{id}:generateBenchmarksMetrics"},
    {"method": "POST", "path": "v24/customers/{id}:generateCreatorInsights"},
    {"method": "POST", "path": "v24/customers/{id}:generateKeywordForecastMetrics"},
    {"method": "POST", "path": "v24/customers/{id}:generateKeywordHistoricalMetrics"},
    {"method": "POST", "path": "v24/customers/{id}:generateKeywordIdeas"},
    {"method": "POST", "path": "v24/customers/{id}:generateReachForecast"},
    {"method": "POST", "path": "v24/customers/{id}:generateSuggestedTargetingInsights"},
    {"method": "POST", "path": "v24/customers/{id}:generateTargetingSuggestionMetrics"},
    {"method": "POST", "path": "v24/customers/{id}:generateTrendingInsights"},
    {"method": "POST", "path": "v24/customers/{id}:searchAudienceInsightsAttributes"},
    {"method": "POST", "path": "v24/customers/{id}:suggestBrands"},
    {"method": "POST", "path": "v24/customers/{id}:suggestKeywordThemes"},
    {"method": "POST", "path": "v24/customers/{id}:suggestSmartCampaignAd"},
    {"method": "POST", "path": "v24/customers/{id}:suggestSmartCampaignBudgetOptions"},
    {"method": "GET", "path": "v24/customers:listAccessibleCustomers"},
    {"method": "GET", "path": "v24/customers/{id}/experiments/{id}:listExperimentAsyncErrors"},
    {"method": "POST", "path": "v24/geoTargetConstants:suggest"},
    {"method": "POST", "path": "v24/customers/{id}/googleAds:search"},
    {"method": "POST", "path": "v24/customers/{id}/googleAds:searchStream"},
    {"method": "GET", "path": "v24/googleAdsFields/{id}"},
    {"method": "POST", "path": "v24/googleAdsFields:search"},
    {"method": "GET", "path": "v24/incentives:fetchIncentive"},
    {"method": "GET", "path": "v24/customers/{id}/invoices"},
    {"method": "POST", "path": "v24/keywordThemeConstants:suggest"},
    {"method": "GET", "path": "v24/customers/{id}/operations"},
    {"method": "GET", "path": "v24/customers/{id}/operations/{id}"},
    {"method": "POST", "path": "v24/customers/{id}/operations/{id}:wait"},
    {"method": "GET", "path": "v24/customers/{id}/paymentsAccounts"},
    {"method": "POST", "path": "v24/customers/{id}/recommendations:generate"},
    {"method": "POST", "path": "v24/customers/{id}/reservations:quoteCampaigns"},
    {"method": "GET", "path": "v24/customers/{id}/smartCampaignSettings/{id}:getSmartCampaignStatus"},
    {"method": "POST", "path": "v24:generateConversionRates"},
    {"method": "POST", "path": "v24:listBenchmarksAvailableDates"},
    {"method": "POST", "path": "v24:listBenchmarksLocations"},
    {"method": "POST", "path": "v24:listBenchmarksProducts"},
    {"method": "POST", "path": "v24:listBenchmarksSources"},
    {"method": "POST", "path": "v24:listPlannableLocations"},
    {"method": "POST", "path": "v24:listPlannableProducts"},
    {"method": "POST", "path": "v24:listPlannableUserInterests"},
    {"method": "POST", "path": "v24:listPlannableUserLists"}
  ],
  "deny": []
}
```

## Endpoints

The Google Ads endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| POST | v24/customers/{id}/AdGroupCriterionCustomizers:mutate | write | AdGroupCriterionCustomizers | Creates, updates or removes ad group criterion customizers. |
| POST | v24/customers/{id}/CampaignGoalConfigs:mutate | write | CampaignGoalConfigs | Create or update campaign goal configs. |
| POST | v24/customers/{id}/CustomerCustomizers:mutate | write | CustomerCustomizers | Creates, updates or removes customer customizers. |
| POST | v24/customers/{id}/Goals:mutate | write | Goals | Create or update goals. |
| POST | v24/customers/{id}/accountBudgetProposals:mutate | write | accountBudgetProposals | Creates, updates, or removes account budget proposals. |
| POST | v24/customers/{id}/accountLinks:create | write | accountLinks | Creates an account link. |
| POST | v24/customers/{id}/accountLinks:mutate | write | accountLinks | Creates or removes an account link. |
| POST | v24/customers/{id}/adGroupAdLabels:mutate | write | adGroupAdLabels | Creates and removes ad group ad labels. |
| POST | v24/customers/{id}/adGroupAds/{id}:removeAutomaticallyCreatedAssets | write | adGroupAds | Remove text customization (formerly automatically created assets) from an ad. |
| POST | v24/customers/{id}/adGroupAds:mutate | write | adGroupAds | Creates, updates, or removes ads. |
| POST | v24/customers/{id}/adGroupAssetSets:mutate | write | adGroupAssetSets | Creates, or removes ad group asset sets. |
| POST | v24/customers/{id}/adGroupAssets:mutate | write | adGroupAssets | Creates, updates, or removes ad group assets. |
| POST | v24/customers/{id}/adGroupBidModifiers:mutate | write | adGroupBidModifiers | Creates, updates, or removes ad group bid modifiers. |
| POST | v24/customers/{id}/adGroupCriteria:mutate | write | adGroupCriteria | Creates, updates, or removes criteria. |
| POST | v24/customers/{id}/adGroupCriterionLabels:mutate | write | adGroupCriterionLabels | Creates and removes ad group criterion labels. |
| POST | v24/customers/{id}/adGroupCustomizers:mutate | write | adGroupCustomizers | Creates, updates or removes ad group customizers. |
| POST | v24/customers/{id}/adGroupLabels:mutate | write | adGroupLabels | Creates and removes ad group labels. |
| POST | v24/customers/{id}/adGroups:mutate | write | adGroups | Creates, updates, or removes ad groups. |
| POST | v24/customers/{id}/adParameters:mutate | write | adParameters | Creates, updates, or removes ad parameters. |
| POST | v24/customers/{id}/ads:mutate | write | ads | Updates ads. |
| POST | v24/customers/{id}/assetGenerations:generateImages | write | assetGenerations | Uses generative AI to generate images that can be used as assets in a campaign. |
| POST | v24/customers/{id}/assetGenerations:generateText | write | assetGenerations | Uses generative AI to generate text that can be used as assets in a campaign. |
| POST | v24/customers/{id}/assetGroupAssets:mutate | write | assetGroupAssets | Creates, updates or removes asset group assets. |
| POST | v24/customers/{id}/assetGroupListingGroupFilters:mutate | write | assetGroupListingGroupFilters | Creates, updates or removes asset group listing group filters. |
| POST | v24/customers/{id}/assetGroupSignals:mutate | write | assetGroupSignals | Creates or removes asset group signals. |
| POST | v24/customers/{id}/assetGroups:mutate | write | assetGroups | Creates, updates or removes asset groups. |
| POST | v24/customers/{id}/assetSetAssets:mutate | write | assetSetAssets | Creates, updates or removes asset set assets. |
| POST | v24/customers/{id}/assetSets:mutate | write | assetSets | Creates, updates or removes asset sets. |
| POST | v24/customers/{id}/assets:mutate | write | assets | Creates assets. |
| POST | v24/audienceInsights:listInsightsEligibleDates | read | audienceInsights | Lists date ranges for which audience insights data can be requested. |
| POST | v24/customers/{id}/audiences:mutate | write | audiences | Creates audiences. |
| POST | v24/customers/{id}/batchJobs/{id}:addOperations | write | batchJobs | Add operations to the batch job. |
| GET | v24/customers/{id}/batchJobs/{id}:listResults | read | batchJobs | Returns the results of the batch job. |
| POST | v24/customers/{id}/batchJobs/{id}:run | write | batchJobs | Runs the batch job. |
| POST | v24/customers/{id}/batchJobs:mutate | write | batchJobs | Mutates a batch job. |
| POST | v24/customers/{id}/biddingDataExclusions:mutate | write | biddingDataExclusions | Creates, updates, or removes data exclusions. |
| POST | v24/customers/{id}/biddingSeasonalityAdjustments:mutate | write | biddingSeasonalityAdjustments | Creates, updates, or removes seasonality adjustments. |
| POST | v24/customers/{id}/biddingStrategies:mutate | write | biddingStrategies | Creates, updates, or removes bidding strategies. |
| POST | v24/customers/{id}/billingSetups:mutate | write | billingSetups | Creates a billing setup, or cancels an existing billing setup. |
| POST | v24/customers/{id}/campaignAssetSets:mutate | write | campaignAssetSets | Creates, updates or removes campaign asset sets. |
| POST | v24/customers/{id}/campaignAssets:mutate | write | campaignAssets | Creates, updates, or removes campaign assets. |
| POST | v24/customers/{id}/campaignBidModifiers:mutate | write | campaignBidModifiers | Creates, updates, or removes campaign bid modifiers. |
| POST | v24/customers/{id}/campaignBudgets:mutate | write | campaignBudgets | Creates, updates, or removes campaign budgets. |
| POST | v24/customers/{id}/campaignConversionGoals:mutate | write | campaignConversionGoals | Creates, updates or removes campaign conversion goals. |
| POST | v24/customers/{id}/campaignCriteria:mutate | write | campaignCriteria | Creates, updates, or removes criteria. |
| POST | v24/customers/{id}/campaignCustomizers:mutate | write | campaignCustomizers | Creates, updates or removes campaign customizers. |
| GET | v24/customers/{id}/campaignDrafts/{id}:listAsyncErrors | read | campaignDrafts | Returns all errors that occurred during CampaignDraft promote. |
| POST | v24/customers/{id}/campaignDrafts/{id}:promote | write | campaignDrafts | Promotes the changes in a draft back to the base campaign. |
| POST | v24/customers/{id}/campaignDrafts:mutate | write | campaignDrafts | Creates, updates, or removes campaign drafts. |
| POST | v24/customers/{id}/campaignGroups:mutate | write | campaignGroups | Creates, updates, or removes campaign groups. |
| POST | v24/customers/{id}/campaignLabels:mutate | write | campaignLabels | Creates and removes campaign-label relationships. |
| POST | v24/customers/{id}/campaignLifecycleGoal:configureCampaignLifecycleGoals | write | campaignLifecycleGoal | Process the given campaign lifecycle configurations. |
| POST | v24/customers/{id}/campaignSharedSets:mutate | write | campaignSharedSets | Creates or removes campaign shared sets. |
| POST | v24/customers/{id}/campaigns:enablePMaxBrandGuidelines | write | campaigns | Enables Brand Guidelines for Performance Max campaigns. |
| POST | v24/customers/{id}/campaigns:mutate | write | campaigns | Creates, updates, or removes campaigns. |
| POST | v24/customers/{id}/conversionActions:mutate | write | conversionActions | Creates, updates or removes conversion actions. |
| POST | v24/customers/{id}/conversionCustomVariables:mutate | write | conversionCustomVariables | Creates or updates conversion custom variables. |
| POST | v24/customers/{id}/conversionGoalCampaignConfigs:mutate | write | conversionGoalCampaignConfigs | Creates, updates or removes conversion goal campaign config. |
| POST | v24/customers/{id}/conversionValueRuleSets:mutate | write | conversionValueRuleSets | Creates, updates or removes conversion value rule sets. |
| POST | v24/customers/{id}/conversionValueRules:mutate | write | conversionValueRules | Creates, updates, or removes conversion value rules. |
| POST | v24/customers/{id}/customAudiences:mutate | write | customAudiences | Creates or updates custom audiences. |
| POST | v24/customers/{id}/customConversionGoals:mutate | write | customConversionGoals | Creates, updates or removes custom conversion goals. |
| POST | v24/customers/{id}/customInterests:mutate | write | customInterests | Creates or updates custom interests. |
| POST | v24/customers/{id}/customerAssetSets:mutate | write | customerAssetSets | Creates, or removes customer asset sets. |
| POST | v24/customers/{id}/customerAssets:mutate | write | customerAssets | Creates, updates, or removes customer assets. |
| POST | v24/customers/{id}/customerClientLinks:mutate | write | customerClientLinks | Creates or updates a customer client link. |
| POST | v24/customers/{id}/customerConversionGoals:mutate | write | customerConversionGoals | Creates, updates or removes customer conversion goals. |
| POST | v24/customers/{id}/customerLabels:mutate | write | customerLabels | Creates and removes customer-label relationships. |
| POST | v24/customers/{id}/customerLifecycleGoal:configureCustomerLifecycleGoals | write | customerLifecycleGoal | Process the given customer lifecycle configurations. |
| POST | v24/customers/{id}/customerManagerLinks:moveManagerLink | write | customerManagerLinks | Moves a client customer to a new manager customer. |
| POST | v24/customers/{id}/customerManagerLinks:mutate | write | customerManagerLinks | Updates customer manager links. |
| POST | v24/customers/{id}/customerNegativeCriteria:mutate | write | customerNegativeCriteria | Creates or removes criteria. |
| POST | v24/customers/{id}/customerSkAdNetworkConversionValueSchemas:mutate | write | customerSkAdNetworkConversionValueSchemas | Creates or updates the CustomerSkAdNetworkConversionValueSchema. |
| POST | v24/customers/{id}/customerUserAccessInvitations:mutate | write | customerUserAccessInvitations | Creates or removes an access invitation. |
| POST | v24/customers/{id}/customerUserAccesses:mutate | write | customerUserAccesses | Updates, removes permission of a user on a given customer. |
| GET | v24/customers/{id}/getIdentityVerification | read | customers | Returns Identity Verification information. |
| POST | v24/customers/{id}:createCustomerClient | write | customers | Creates a new client under manager. |
| POST | v24/customers/{id}:generateAdGroupThemes | read | customers | Returns a list of suggested AdGroups and suggested modifications (text, match type) for the given keywords. |
| POST | v24/customers/{id}:generateAudienceCompositionInsights | read | customers | Returns a collection of attributes that are represented in an audience of interest, with metrics that compare each attribute's share of the audience with its sh |
| POST | v24/customers/{id}:generateAudienceDefinition | read | customers | Returns a collection of audience attributes using generative AI based on the provided audience description. |
| POST | v24/customers/{id}:generateAudienceOverlapInsights | read | customers | Returns a collection of audience attributes along with estimates of the overlap between their potential YouTube reach and that of a given input attribute. |
| POST | v24/customers/{id}:generateBenchmarksMetrics | read | customers | Returns YouTube advertisement metrics for the given client against industry benchmarks. |
| POST | v24/customers/{id}:generateCreatorInsights | read | customers | Returns insights for a collection of YouTube Creators and Channels. |
| POST | v24/customers/{id}:generateInsightsFinderReport | write | customers | Creates a saved report that can be viewed in the Insights Finder tool. |
| POST | v24/customers/{id}:generateKeywordForecastMetrics | read | customers | Returns metrics (such as impressions, clicks, total cost) of a keyword forecast for the given campaign. |
| POST | v24/customers/{id}:generateKeywordHistoricalMetrics | read | customers | Returns a list of keyword historical metrics. |
| POST | v24/customers/{id}:generateKeywordIdeas | read | customers | Returns a list of keyword ideas. |
| POST | v24/customers/{id}:generateReachForecast | read | customers | Generates a reach forecast for a given targeting / product mix. |
| POST | v24/customers/{id}:generateShareablePreviews | write | customers | Returns the requested Shareable Preview. |
| POST | v24/customers/{id}:generateSuggestedTargetingInsights | read | customers | Returns a collection of targeting insights (e.g. |
| POST | v24/customers/{id}:generateTargetingSuggestionMetrics | read | customers | Returns potential reach metrics for targetable audiences. |
| POST | v24/customers/{id}:generateTrendingInsights | read | customers | Returns insights for trending content on YouTube. |
| POST | v24/customers/{id}:mutate | write | customers | Updates a customer. |
| POST | v24/customers/{id}:removeCampaignAutomaticallyCreatedAsset | write | customers | Removes text customization (formerly automatically created assets) from a campaign. |
| POST | v24/customers/{id}:searchAudienceInsightsAttributes | read | customers | Searches for audience attributes that can be used to generate insights. |
| POST | v24/customers/{id}:startIdentityVerification | write | customers | Starts Identity Verification for a given verification program type. |
| POST | v24/customers/{id}:suggestBrands | read | customers | Rpc to return a list of matching brands based on a prefix for this customer. |
| POST | v24/customers/{id}:suggestKeywordThemes | read | customers | Suggests keyword themes to advertise on. |
| POST | v24/customers/{id}:suggestSmartCampaignAd | read | customers | Suggests a Smart campaign ad compatible with the Ad family of resources, based on data points such as targeting and the business to advertise. |
| POST | v24/customers/{id}:suggestSmartCampaignBudgetOptions | read | customers | Returns BudgetOption suggestions. |
| POST | v24/customers/{id}:suggestTravelAssets | write | customers | Returns Travel Asset suggestions. |
| POST | v24/customers/{id}:uploadCallConversions | write | customers | Processes the given call conversions. |
| POST | v24/customers/{id}:uploadClickConversions | write | customers | Processes the given click conversions. |
| POST | v24/customers/{id}:uploadConversionAdjustments | write | customers | Processes the given conversion adjustments. |
| POST | v24/customers/{id}:uploadUserData | write | customers | Uploads the given user data. |
| GET | v24/customers:listAccessibleCustomers | read | customers | Returns resource names of customers directly accessible by the user authenticating the call. |
| POST | v24/customers/{id}/customizerAttributes:mutate | write | customizerAttributes | Creates, updates or removes customizer attributes. |
| POST | v24/customers/{id}/dataLinks:create | write | dataLinks | Creates a data link. |
| POST | v24/customers/{id}/dataLinks:remove | write | dataLinks | Remove a data link. |
| POST | v24/customers/{id}/dataLinks:update | write | dataLinks | Update a data link. |
| POST | v24/customers/{id}/experimentArms:mutate | write | experimentArms | Creates, updates, or removes experiment arms. |
| POST | v24/customers/{id}/experiments/{id}:endExperiment | write | experiments | Immediately ends an experiment, changing the experiment's scheduled end date and without waiting for end of day. |
| POST | v24/customers/{id}/experiments/{id}:graduateExperiment | write | experiments | Graduates an experiment to a full campaign. |
| GET | v24/customers/{id}/experiments/{id}:listExperimentAsyncErrors | read | experiments | Returns all errors that occurred during the last Experiment update (either scheduling or promotion). |
| POST | v24/customers/{id}/experiments/{id}:promoteExperiment | write | experiments | Promotes the trial campaign thus applying changes in the trial campaign to the base campaign. |
| POST | v24/customers/{id}/experiments/{id}:scheduleExperiment | write | experiments | Schedule an experiment. |
| POST | v24/customers/{id}/experiments:mutate | write | experiments | Creates, updates, or removes experiments. |
| POST | v24/geoTargetConstants:suggest | read | geoTargetConstants | Returns GeoTargetConstant suggestions by location name or by resource name. |
| POST | v24/customers/{id}/googleAds:mutate | write | googleAds | Executes mutate and actions operations. |
| POST | v24/customers/{id}/googleAds:search | read | googleAds | Returns all rows that match the search query. |
| POST | v24/customers/{id}/googleAds:searchStream | read | googleAds | Returns all rows that match the search stream query. |
| GET | v24/googleAdsFields/{id} | read | googleAdsFields | Returns just the requested field. |
| POST | v24/googleAdsFields:search | read | googleAdsFields | Returns all fields that match the search query. |
| POST | v24/customers/{id}/incentives/{id}:applyIncentive | write | incentives | Applies the incentive for the ads customer. |
| GET | v24/incentives:fetchIncentive | read | incentives | Returns incentives for a given user. |
| GET | v24/customers/{id}/invoices | read | invoices | Returns all invoices associated with a billing setup, for a given month. |
| POST | v24/customers/{id}/keywordPlanAdGroupKeywords:mutate | write | keywordPlanAdGroupKeywords | Creates, updates, or removes Keyword Plan ad group keywords. |
| POST | v24/customers/{id}/keywordPlanAdGroups:mutate | write | keywordPlanAdGroups | Creates, updates, or removes Keyword Plan ad groups. |
| POST | v24/customers/{id}/keywordPlanCampaignKeywords:mutate | write | keywordPlanCampaignKeywords | Creates, updates, or removes Keyword Plan campaign keywords. |
| POST | v24/customers/{id}/keywordPlanCampaigns:mutate | write | keywordPlanCampaigns | Creates, updates, or removes Keyword Plan campaigns. |
| POST | v24/customers/{id}/keywordPlans:mutate | write | keywordPlans | Creates, updates, or removes keyword plans. |
| POST | v24/keywordThemeConstants:suggest | read | keywordThemeConstants | Returns KeywordThemeConstant suggestions by keyword themes. |
| POST | v24/customers/{id}/labels:mutate | write | labels | Creates, updates, or removes labels. |
| POST | v24/customers/{id}/localServices:appendLeadConversation | write | localServices | RPC to append Local Services Lead Conversation resources to Local Services Lead resources. |
| POST | v24/customers/{id}/localServicesLeads/{id}:provideLeadFeedback | write | localServicesLeads | RPC to provide feedback on Local Services Lead resources. |
| POST | upload/v24/customers/{id}/youTubeVideoUploads:create | write | media | Uploads a video to Google-managed or advertiser owned (brand) YouTube channel. (media upload) |
| POST | v24/customers/{id}/youTubeVideoUploads:create | write | media | Uploads a video to Google-managed or advertiser owned (brand) YouTube channel. |
| POST | v24/customers/{id}/multiPartyAuthReview:resolve | write | multiPartyAuthReview | Resolves the status of a Multi-Party Authorization review. |
| POST | v24/customers/{id}/offlineUserDataJobs/{id}:addOperations | write | offlineUserDataJobs | Adds operations to the offline user data job. |
| POST | v24/customers/{id}/offlineUserDataJobs/{id}:run | write | offlineUserDataJobs | Runs the offline user data job. |
| POST | v24/customers/{id}/offlineUserDataJobs:create | write | offlineUserDataJobs | Creates an offline user data job. |
| GET | v24/customers/{id}/operations | read | operations | Lists operations that match the specified filter in the request. |
| GET | v24/customers/{id}/operations/{id} | read | operations | Gets the latest state of a long-running operation. |
| DELETE | v24/customers/{id}/operations/{id} | write | operations | Deletes a long-running operation. |
| POST | v24/customers/{id}/operations/{id}:cancel | write | operations | Starts asynchronous cancellation on a long-running operation. |
| POST | v24/customers/{id}/operations/{id}:wait | read | operations | Waits until the specified long-running operation is done or reaches at most a specified timeout, returning the latest state. |
| GET | v24/customers/{id}/paymentsAccounts | read | paymentsAccounts | Returns all payments accounts associated with all managers between the login customer ID and specified serving customer in the hierarchy, inclusive. |
| POST | v24/customers/{id}/productLinkInvitations:create | write | productLinkInvitations | Creates a product link invitation. |
| POST | v24/customers/{id}/productLinkInvitations:remove | write | productLinkInvitations | Remove a product link invitation. |
| POST | v24/customers/{id}/productLinkInvitations:update | write | productLinkInvitations | Update a product link invitation. |
| POST | v24/customers/{id}/productLinks:create | write | productLinks | Creates a product link. |
| POST | v24/customers/{id}/productLinks:remove | write | productLinks | Removes a product link. |
| POST | v24/customers/{id}/recommendationSubscriptions:mutateRecommendationSubscription | write | recommendationSubscriptions | Mutates given subscription with corresponding apply parameters. |
| POST | v24/customers/{id}/recommendations:apply | write | recommendations | Applies given recommendations with corresponding apply parameters. |
| POST | v24/customers/{id}/recommendations:dismiss | write | recommendations | Dismisses given recommendations. |
| POST | v24/customers/{id}/recommendations:generate | read | recommendations | Generates Recommendations based off the requested recommendation_types. |
| POST | v24/customers/{id}/remarketingActions:mutate | write | remarketingActions | Creates or updates remarketing actions. |
| POST | v24/customers/{id}/reservations:bookCampaigns | write | reservations | Books the requested campaigns. |
| POST | v24/customers/{id}/reservations:quoteCampaigns | read | reservations | Proposes quotes for booking campaigns. |
| POST | v24/customers/{id}/sharedCriteria:mutate | write | sharedCriteria | Creates or removes shared criteria. |
| POST | v24/customers/{id}/sharedSets:mutate | write | sharedSets | Creates, updates, or removes shared sets. |
| GET | v24/customers/{id}/smartCampaignSettings/{id}:getSmartCampaignStatus | read | smartCampaignSettings | Returns the status of the requested Smart campaign. |
| POST | v24/customers/{id}/smartCampaignSettings:mutate | write | smartCampaignSettings | Updates Smart campaign settings for campaigns. |
| POST | v24/customers/{id}/thirdPartyAppAnalyticsLinks/{id}:regenerateShareableLinkId | write | thirdPartyAppAnalyticsLinks | Regenerate ThirdPartyAppAnalyticsLink.shareable_link_id that should be provided to the third party when setting up app analytics. |
| POST | v24/customers/{id}/userListCustomerTypes:mutate | write | userListCustomerTypes | Attach or remove user list customer types. |
| POST | v24/customers/{id}/userLists:mutate | write | userLists | Creates or updates user lists. |
| POST | v24:generateConversionRates | read | v24 | Returns a collection of conversion rate suggestions for supported plannable products. |
| POST | v24:listBenchmarksAvailableDates | read | v24 | Returns a date range that supports benchmarks. |
| POST | v24:listBenchmarksLocations | read | v24 | Returns the list of locations that support benchmarks (for example, countries). |
| POST | v24:listBenchmarksProducts | read | v24 | Returns the list of products that supports benchmarks. |
| POST | v24:listBenchmarksSources | read | v24 | Returns the list of benchmarks sources (for example, Industry Verticals). |
| POST | v24:listPlannableLocations | read | v24 | Returns the list of plannable locations (for example, countries). |
| POST | v24:listPlannableProducts | read | v24 | Returns the list of per-location plannable YouTube ad formats with allowed targeting. |
| POST | v24:listPlannableUserInterests | read | v24 | Returns the list of plannable user interests. |
| POST | v24:listPlannableUserLists | read | v24 | Returns the list of plannable user lists with their plannable status. |
| POST | v24/customers/{id}/youTubeVideoUploads:remove | write | youTubeVideoUploads | Removes YouTube videos uploaded using this API. |
| POST | v24/customers/{id}/youTubeVideoUploads:update | write | youTubeVideoUploads | Updates YouTube video's metadata, but only for videos uploaded using this API. |
