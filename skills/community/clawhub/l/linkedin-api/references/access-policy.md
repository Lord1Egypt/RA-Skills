# LinkedIn access policy

An access policy limits which endpoints LinkedIn connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/linkedin#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for LinkedIn: its 73 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create linkedin --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "rest/adAccountUsers"},
    {"method": "GET", "path": "rest/adAccountUsers/{id}"},
    {"method": "GET", "path": "rest/adAccounts"},
    {"method": "GET", "path": "rest/adAccounts/{id}"},
    {"method": "GET", "path": "rest/adAnalytics"},
    {"method": "GET", "path": "rest/adBudgetPricing"},
    {"method": "GET", "path": "rest/adLibrary"},
    {"method": "GET", "path": "rest/adPreviews"},
    {"method": "POST", "path": "rest/adPreviews"},
    {"method": "GET", "path": "rest/assets/{id}"},
    {"method": "GET", "path": "rest/adAccountTrustPreferences/{id}"},
    {"method": "GET", "path": "rest/adPublisherRestrictions"},
    {"method": "GET", "path": "rest/adPublisherRestrictions/{id}"},
    {"method": "GET", "path": "rest/adAccounts/{id}/adCampaignGroups"},
    {"method": "GET", "path": "rest/adAccounts/{id}/adCampaignGroups/{id}"},
    {"method": "GET", "path": "rest/adAccounts/{id}/adCampaigns"},
    {"method": "GET", "path": "rest/adAccounts/{id}/adCampaigns/{id}"},
    {"method": "GET", "path": "rest/conversationAds"},
    {"method": "GET", "path": "rest/conversationAds/{id}"},
    {"method": "GET", "path": "rest/conversationAds/{id}/sponsoredMessageContents"},
    {"method": "GET", "path": "rest/conversationAds/{id}/sponsoredMessageContents/{id}"},
    {"method": "GET", "path": "rest/campaignConversions"},
    {"method": "GET", "path": "rest/campaignConversions/{id}"},
    {"method": "GET", "path": "rest/conversions"},
    {"method": "GET", "path": "rest/conversions/{id}"},
    {"method": "GET", "path": "rest/insightTagDomains"},
    {"method": "GET", "path": "rest/insightTagDomains/{id}"},
    {"method": "GET", "path": "rest/insightTags"},
    {"method": "GET", "path": "rest/insightTags/{id}"},
    {"method": "GET", "path": "rest/insightTagsPermission"},
    {"method": "GET", "path": "rest/adAccounts/{id}/creatives"},
    {"method": "GET", "path": "rest/adAccounts/{id}/creatives/{id}"},
    {"method": "GET", "path": "rest/documents"},
    {"method": "GET", "path": "rest/documents/{id}"},
    {"method": "GET", "path": "rest/adExperimentResults"},
    {"method": "GET", "path": "rest/adExperimentResults/{id}"},
    {"method": "GET", "path": "rest/adExperiments"},
    {"method": "GET", "path": "rest/adExperiments/{id}"},
    {"method": "GET", "path": "rest/adLiftTestBenchmark"},
    {"method": "GET", "path": "rest/adLiftTestResults"},
    {"method": "GET", "path": "rest/adLiftTests"},
    {"method": "GET", "path": "rest/adLiftTests/{id}"},
    {"method": "GET", "path": "rest/adLiftTests/{id}/adLiftTestSurveys"},
    {"method": "GET", "path": "rest/images"},
    {"method": "GET", "path": "rest/images/{id}"},
    {"method": "GET", "path": "rest/jobLibrary"},
    {"method": "GET", "path": "rest/inMailContents"},
    {"method": "GET", "path": "rest/inMailContents/{id}"},
    {"method": "GET", "path": "rest/organizationAcls"},
    {"method": "GET", "path": "rest/organizationAuthorizations"},
    {"method": "GET", "path": "rest/organizationAuthorizations/{id}"},
    {"method": "GET", "path": "rest/organizations"},
    {"method": "GET", "path": "rest/organizations/{id}"},
    {"method": "GET", "path": "rest/organizationsLookup"},
    {"method": "GET", "path": "rest/posts"},
    {"method": "GET", "path": "rest/posts/{id}"},
    {"method": "GET", "path": "rest/me"},
    {"method": "GET", "path": "v2/me"},
    {"method": "GET", "path": "v2/userinfo"},
    {"method": "GET", "path": "rest/organizationalEntityShareStatistics"},
    {"method": "GET", "path": "rest/adSupplyForecasts"},
    {"method": "GET", "path": "rest/adTargetTemplates"},
    {"method": "GET", "path": "rest/adTargetTemplates/{id}"},
    {"method": "GET", "path": "rest/adTargetingEntities"},
    {"method": "GET", "path": "rest/adTargetingFacets"},
    {"method": "GET", "path": "rest/audienceCounts"},
    {"method": "GET", "path": "rest/countryGroups"},
    {"method": "GET", "path": "v2/geo/{id}"},
    {"method": "GET", "path": "rest/adTrackingParameters/{id}"},
    {"method": "GET", "path": "rest/thirdPartyTrackingTags"},
    {"method": "GET", "path": "rest/thirdPartyTrackingTags/{id}"},
    {"method": "GET", "path": "rest/videos"},
    {"method": "GET", "path": "rest/videos/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The LinkedIn endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | rest/adAccountUsers | read | ad account users | List ad account users. |
| GET | rest/adAccountUsers/{id} | read | ad account users | Get an ad account user. |
| POST | rest/adAccountUsers/{id} | write | ad account users | Update an ad account user. |
| PUT | rest/adAccountUsers/{id} | write | ad account users | Create or replace an ad account user. |
| DELETE | rest/adAccountUsers/{id} | write | ad account users | Remove an ad account user. |
| GET | rest/adAccounts | read | ad accounts | List or search ad accounts. |
| POST | rest/adAccounts | write | ad accounts | Create an ad account. |
| GET | rest/adAccounts/{id} | read | ad accounts | Get an ad account. |
| POST | rest/adAccounts/{id} | write | ad accounts | Partially update an ad account. |
| DELETE | rest/adAccounts/{id} | write | ad accounts | Delete an ad account. |
| GET | rest/adAnalytics | read | ad analytics | Get ad analytics. |
| GET | rest/adBudgetPricing | read | ad analytics | Get ad budget pricing. |
| GET | rest/adLibrary | read | ad library | Search the ad library. |
| GET | rest/adPreviews | read | ad previews | Get ad previews. |
| POST | rest/adPreviews | read | ad previews | Render a live preview for a creative. |
| POST | rest/assets | write | assets | Register an asset upload. |
| GET | rest/assets/{id} | read | assets | Get an asset. |
| GET | rest/adAccountTrustPreferences/{id} | read | audience restrictions | Get brand safety preferences of an ad account. |
| PUT | rest/adAccountTrustPreferences/{id} | write | audience restrictions | Set brand safety preferences of an ad account. |
| GET | rest/adPublisherRestrictions | read | audience restrictions | List publisher restrictions. |
| POST | rest/adPublisherRestrictions | write | audience restrictions | Create a publisher restriction. |
| GET | rest/adPublisherRestrictions/{id} | read | audience restrictions | Get a publisher restriction. |
| POST | rest/adPublisherRestrictions/{id} | write | audience restrictions | Update a publisher restriction. |
| POST | rest/globalPublisherList | write | audience restrictions | Create a global publisher list. |
| GET | rest/adAccounts/{id}/adCampaignGroups | read | campaign groups | List or search campaign groups. |
| POST | rest/adAccounts/{id}/adCampaignGroups | write | campaign groups | Create a campaign group. |
| DELETE | rest/adAccounts/{id}/adCampaignGroups | write | campaign groups | Batch delete campaign groups. |
| GET | rest/adAccounts/{id}/adCampaignGroups/{id} | read | campaign groups | Get a campaign group. |
| POST | rest/adAccounts/{id}/adCampaignGroups/{id} | write | campaign groups | Partially update a campaign group. |
| DELETE | rest/adAccounts/{id}/adCampaignGroups/{id} | write | campaign groups | Delete a campaign group. |
| GET | rest/adAccounts/{id}/adCampaigns | read | campaigns | List or search campaigns. |
| POST | rest/adAccounts/{id}/adCampaigns | write | campaigns | Create a campaign. |
| GET | rest/adAccounts/{id}/adCampaigns/{id} | read | campaigns | Get a campaign. |
| POST | rest/adAccounts/{id}/adCampaigns/{id} | write | campaigns | Partially update a campaign. |
| DELETE | rest/adAccounts/{id}/adCampaigns/{id} | write | campaigns | Delete a campaign. |
| GET | rest/conversationAds | read | conversation ads | List conversation ads. |
| POST | rest/conversationAds | write | conversation ads | Create a conversation ad. |
| GET | rest/conversationAds/{id} | read | conversation ads | Get a conversation ad. |
| POST | rest/conversationAds/{id} | write | conversation ads | Partially update a conversation ad. |
| GET | rest/conversationAds/{id}/sponsoredMessageContents | read | conversation ads | List sponsored message contents of a conversation ad. |
| POST | rest/conversationAds/{id}/sponsoredMessageContents | write | conversation ads | Create sponsored message contents. |
| DELETE | rest/conversationAds/{id}/sponsoredMessageContents | write | conversation ads | Batch delete sponsored message contents. |
| GET | rest/conversationAds/{id}/sponsoredMessageContents/{id} | read | conversation ads | Get sponsored message contents. |
| POST | rest/conversationAds/{id}/sponsoredMessageContents/{id} | write | conversation ads | Partially update sponsored message contents. |
| GET | rest/campaignConversions | read | conversion tracking | List campaign conversion associations. |
| PUT | rest/campaignConversions | write | conversion tracking | Associate conversions with campaigns. |
| DELETE | rest/campaignConversions | write | conversion tracking | Batch remove campaign conversion associations. |
| GET | rest/campaignConversions/{id} | read | conversion tracking | Get a campaign conversion association. |
| PUT | rest/campaignConversions/{id} | write | conversion tracking | Associate a conversion with a campaign. |
| DELETE | rest/campaignConversions/{id} | write | conversion tracking | Remove a campaign conversion association. |
| GET | rest/conversions | read | conversion tracking | List conversion rules. |
| POST | rest/conversions | write | conversion tracking | Create a conversion rule. |
| GET | rest/conversions/{id} | read | conversion tracking | Get a conversion rule. |
| POST | rest/conversions/{id} | write | conversion tracking | Partially update a conversion rule. |
| GET | rest/insightTagDomains | read | conversion tracking | List Insight Tag domains. |
| POST | rest/insightTagDomains | write | conversion tracking | Create an Insight Tag domain. |
| GET | rest/insightTagDomains/{id} | read | conversion tracking | Get an Insight Tag domain. |
| POST | rest/insightTagDomains/{id} | write | conversion tracking | Update an Insight Tag domain. |
| GET | rest/insightTags | read | conversion tracking | List Insight Tags. |
| POST | rest/insightTags | write | conversion tracking | Create an Insight Tag. |
| GET | rest/insightTags/{id} | read | conversion tracking | Get an Insight Tag. |
| POST | rest/insightTags/{id} | write | conversion tracking | Update an Insight Tag. |
| GET | rest/insightTagsPermission | read | conversion tracking | List Insight Tag permissions. |
| POST | rest/insightTagsPermission | write | conversion tracking | Grant Insight Tag permission. |
| GET | rest/adAccounts/{id}/creatives | read | creatives | List or search creatives. |
| POST | rest/adAccounts/{id}/creatives | write | creatives | Create a creative. |
| DELETE | rest/adAccounts/{id}/creatives | write | creatives | Batch delete creatives. |
| GET | rest/adAccounts/{id}/creatives/{id} | read | creatives | Get a creative. |
| POST | rest/adAccounts/{id}/creatives/{id} | write | creatives | Partially update a creative. |
| DELETE | rest/adAccounts/{id}/creatives/{id} | write | creatives | Delete a creative. |
| GET | rest/documents | read | documents | Batch get documents. |
| POST | rest/documents | write | documents | Initialize a document upload. |
| GET | rest/documents/{id} | read | documents | Get a document. |
| GET | rest/adExperimentResults | read | experiments | List A/B test results. |
| GET | rest/adExperimentResults/{id} | read | experiments | Get A/B test results. |
| GET | rest/adExperiments | read | experiments | List A/B tests. |
| POST | rest/adExperiments | write | experiments | Create an A/B test. |
| GET | rest/adExperiments/{id} | read | experiments | Get an A/B test. |
| POST | rest/adExperiments/{id} | write | experiments | Partially update an A/B test. |
| DELETE | rest/adExperiments/{id} | write | experiments | Delete an A/B test. |
| GET | rest/adLiftTestBenchmark | read | experiments | Get brand lift test benchmarks. |
| GET | rest/adLiftTestResults | read | experiments | Get brand lift test results. |
| GET | rest/adLiftTests | read | experiments | List brand lift tests. |
| POST | rest/adLiftTests | write | experiments | Create a brand lift test. |
| GET | rest/adLiftTests/{id} | read | experiments | Get a brand lift test. |
| POST | rest/adLiftTests/{id} | write | experiments | Partially update a brand lift test. |
| DELETE | rest/adLiftTests/{id} | write | experiments | Delete a brand lift test. |
| GET | rest/adLiftTests/{id}/adLiftTestSurveys | read | experiments | List brand lift test surveys. |
| POST | rest/adLiftTests/{id}/adLiftTestSurveys | write | experiments | Create brand lift test surveys. |
| DELETE | rest/adLiftTests/{id}/adLiftTestSurveys | write | experiments | Delete brand lift test surveys. |
| GET | rest/images | read | images | Batch get images. |
| POST | rest/images | write | images | Initialize an image upload. |
| GET | rest/images/{id} | read | images | Get an image. |
| POST | rest/images/{id} | write | images | Update an image. |
| GET | rest/jobLibrary | read | job library | Search the job library. |
| GET | rest/inMailContents | read | message ads | List InMail contents. |
| POST | rest/inMailContents | write | message ads | Create InMail contents. |
| GET | rest/inMailContents/{id} | read | message ads | Get InMail contents. |
| POST | rest/inMailContents/{id} | write | message ads | Partially update InMail contents. |
| GET | rest/organizationAcls | read | organization access | List organization role assignments. |
| PUT | rest/organizationAcls/{id} | write | organization access | Assign or update an organization role. |
| GET | rest/organizationAuthorizations | read | organization access | List organization authorizations. |
| GET | rest/organizationAuthorizations/{id} | read | organization access | Get an organization authorization. |
| GET | rest/organizations | read | organizations | List organizations, or look one up by vanity name or parent. |
| GET | rest/organizations/{id} | read | organizations | Get an organization. |
| GET | rest/organizationsLookup | read | organizations | Batch look up organizations. |
| GET | rest/posts | read | posts | List posts by author, or batch get posts by URN. |
| POST | rest/posts | write | posts | Create a post, or reshare a post. |
| GET | rest/posts/{id} | read | posts | Get a post. |
| POST | rest/posts/{id} | write | posts | Partially update a post. |
| DELETE | rest/posts/{id} | write | posts | Delete a post. |
| GET | rest/me | read | profile | Get the current member. |
| GET | v2/me | read | profile | Get the current member (v2). |
| GET | v2/userinfo | read | profile | Get OpenID Connect userinfo for the current member. |
| GET | rest/organizationalEntityShareStatistics | read | statistics | Get share statistics for an organization or its posts. |
| GET | rest/adSupplyForecasts | read | targeting | Get an ad supply forecast. |
| GET | rest/adTargetTemplates | read | targeting | List saved audience templates. |
| POST | rest/adTargetTemplates | write | targeting | Create a saved audience template. |
| DELETE | rest/adTargetTemplates | write | targeting | Delete a saved audience template. |
| GET | rest/adTargetTemplates/{id} | read | targeting | Get a saved audience template. |
| POST | rest/adTargetTemplates/{id} | write | targeting | Update a saved audience template. |
| DELETE | rest/adTargetTemplates/{id} | write | targeting | Delete a saved audience template. |
| GET | rest/adTargetingEntities | read | targeting | Find ad targeting entities. |
| GET | rest/adTargetingFacets | read | targeting | List ad targeting facets. |
| GET | rest/audienceCounts | read | targeting | Get the audience count for a targeting criteria. |
| GET | rest/countryGroups | read | targeting | List country groups. |
| GET | v2/geo/{id} | read | targeting | Get a geo location. |
| GET | rest/adTrackingParameters/{id} | read | tracking | Get dynamic UTM tracking parameters. |
| PUT | rest/adTrackingParameters/{id} | write | tracking | Set dynamic UTM tracking parameters. |
| DELETE | rest/adTrackingParameters/{id} | write | tracking | Delete dynamic UTM tracking parameters. |
| GET | rest/thirdPartyTrackingTags | read | tracking | List third-party tracking tags. |
| POST | rest/thirdPartyTrackingTags | write | tracking | Create a third-party tracking tag. |
| GET | rest/thirdPartyTrackingTags/{id} | read | tracking | Get a third-party tracking tag. |
| DELETE | rest/thirdPartyTrackingTags/{id} | write | tracking | Delete a third-party tracking tag. |
| GET | rest/videos | read | videos | Batch get videos. |
| POST | rest/videos | write | videos | Initialize or finalize a video upload. |
| GET | rest/videos/{id} | read | videos | Get a video. |
| POST | rest/videos/{id} | write | videos | Update a video. |
