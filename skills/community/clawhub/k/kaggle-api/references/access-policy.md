# Kaggle access policy

An access policy limits which endpoints Kaggle connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/kaggle#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Kaggle: its 93 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create kaggle --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "POST", "path": "v1/agents.AgentsApiService/GetAgent"},
    {"method": "POST", "path": "v1/agents.AgentsApiService/GetHarness"},
    {"method": "POST", "path": "v1/agents.AgentsApiService/GetHarnessVersion"},
    {"method": "POST", "path": "v1/agents.AgentsApiService/ListAgents"},
    {"method": "POST", "path": "v1/agents.AgentsApiService/ListHarnesses"},
    {"method": "POST", "path": "v1/benchmarks.BenchmarkTasksApiService/ApiGetBenchmarkSchedulerStatus"},
    {"method": "POST", "path": "v1/benchmarks.BenchmarkTasksApiService/DownloadBenchmarkTaskRunOutput"},
    {"method": "POST", "path": "v1/benchmarks.BenchmarkTasksApiService/GetBenchmarkTask"},
    {"method": "POST", "path": "v1/benchmarks.BenchmarkTasksApiService/GetBenchmarkTaskQuota"},
    {"method": "POST", "path": "v1/benchmarks.BenchmarkTasksApiService/GetBenchmarkTaskRunLogs"},
    {"method": "POST", "path": "v1/benchmarks.BenchmarkTasksApiService/ListBenchmarkTaskRuns"},
    {"method": "POST", "path": "v1/benchmarks.BenchmarkTasksApiService/ListBenchmarkTasks"},
    {"method": "POST", "path": "v1/benchmarks.BenchmarksApiService/GetBenchmarkArenaSettings"},
    {"method": "POST", "path": "v1/benchmarks.BenchmarksApiService/GetBenchmarkLeaderboard"},
    {"method": "POST", "path": "v1/benchmarks.BenchmarksApiService/GetBenchmarkModelVersionConfig"},
    {"method": "POST", "path": "v1/benchmarks.BenchmarksApiService/ListBenchmarkArenaCombinations"},
    {"method": "POST", "path": "v1/benchmarks.BenchmarksApiService/ListBenchmarkModelVersionConfigs"},
    {"method": "POST", "path": "v1/benchmarks.BenchmarksApiService/ListBenchmarkModels"},
    {"method": "POST", "path": "v1/benchmarks.BenchmarksApiService/ListBenchmarkVersionAgentMappings"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/DownloadDataFile"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/DownloadDataFiles"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/DownloadLeaderboard"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/DownloadSubmission"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/GetCompetition"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/GetCompetitionDataFilesSummary"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/GetCompetitionSettings"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/GetCompetitionSolutionStatus"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/GetEpisodeAgentLogs"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/GetEpisodeReplay"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/GetLeaderboard"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/GetSubmission"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/GetSubmissionLimits"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/ListCompetitionHosts"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/ListCompetitionJudges"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/ListCompetitionPages"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/ListCompetitionTopics"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/ListCompetitions"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/ListDataFiles"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/ListDataTreeFiles"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/ListSubmissionEpisodes"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/ListSubmissions"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/ListTeamPublicSubmissions"},
    {"method": "POST", "path": "v1/competitions.CompetitionApiService/ListTopicMessages"},
    {"method": "POST", "path": "v1/datasets.DatasetApiService/DownloadDataset"},
    {"method": "POST", "path": "v1/datasets.DatasetApiService/DownloadDatasetRaw"},
    {"method": "POST", "path": "v1/datasets.DatasetApiService/GetDataset"},
    {"method": "POST", "path": "v1/datasets.DatasetApiService/GetDatasetFilesSummary"},
    {"method": "POST", "path": "v1/datasets.DatasetApiService/GetDatasetMetadata"},
    {"method": "POST", "path": "v1/datasets.DatasetApiService/GetDatasetStatus"},
    {"method": "POST", "path": "v1/datasets.DatasetApiService/ListDatasetFiles"},
    {"method": "POST", "path": "v1/datasets.DatasetApiService/ListDatasets"},
    {"method": "POST", "path": "v1/datasets.DatasetApiService/ListTreeDatasetFiles"},
    {"method": "POST", "path": "v1/discussions.DiscussionApiService/GetTopic"},
    {"method": "POST", "path": "v1/discussions.DiscussionApiService/ListBenchmarkTopics"},
    {"method": "POST", "path": "v1/discussions.DiscussionApiService/ListComments"},
    {"method": "POST", "path": "v1/discussions.DiscussionApiService/ListDatasetTopics"},
    {"method": "POST", "path": "v1/discussions.DiscussionApiService/ListForums"},
    {"method": "POST", "path": "v1/discussions.DiscussionApiService/ListKernelTopics"},
    {"method": "POST", "path": "v1/discussions.DiscussionApiService/ListModelTopics"},
    {"method": "POST", "path": "v1/discussions.DiscussionApiService/ListTopics"},
    {"method": "POST", "path": "v1/discussions.WriteUpsApiService/GetResolvedWriteUpLinks"},
    {"method": "POST", "path": "v1/competitions.HackathonApiService/ExportHackathonWriteUpsCsv"},
    {"method": "POST", "path": "v1/competitions.HackathonApiService/GetHackathonOverview"},
    {"method": "POST", "path": "v1/competitions.HackathonApiService/GetHackathonWriteUp"},
    {"method": "POST", "path": "v1/competitions.HackathonApiService/ListHackathonTracks"},
    {"method": "POST", "path": "v1/competitions.HackathonApiService/ListHackathonWriteUps"},
    {"method": "POST", "path": "v1/competitions.HackathonService/ExportEnrichedHackathonWriteUpsCsv"},
    {"method": "POST", "path": "v1/kernels.KernelsApiService/DownloadKernelOutput"},
    {"method": "POST", "path": "v1/kernels.KernelsApiService/DownloadKernelOutputZip"},
    {"method": "POST", "path": "v1/kernels.KernelsApiService/GetAcceleratorQuotaStatistics"},
    {"method": "POST", "path": "v1/kernels.KernelsApiService/GetKernel"},
    {"method": "POST", "path": "v1/kernels.KernelsApiService/GetKernelSessionLogsStream"},
    {"method": "POST", "path": "v1/kernels.KernelsApiService/GetKernelSessionStatus"},
    {"method": "POST", "path": "v1/kernels.KernelsApiService/ListKernelFiles"},
    {"method": "POST", "path": "v1/kernels.KernelsApiService/ListKernelSessionOutput"},
    {"method": "POST", "path": "v1/kernels.KernelsApiService/ListKernels"},
    {"method": "POST", "path": "v1/models.ModelApiService/DownloadModelInstanceVersion"},
    {"method": "POST", "path": "v1/models.ModelApiService/GetModel"},
    {"method": "POST", "path": "v1/models.ModelApiService/GetModelInstance"},
    {"method": "POST", "path": "v1/models.ModelApiService/Keys"},
    {"method": "POST", "path": "v1/models.ModelApiService/ListModelGatingUserConsents"},
    {"method": "POST", "path": "v1/models.ModelApiService/ListModelInstanceVersionFiles"},
    {"method": "POST", "path": "v1/models.ModelApiService/ListModelInstanceVersions"},
    {"method": "POST", "path": "v1/models.ModelApiService/ListModelInstances"},
    {"method": "POST", "path": "v1/models.ModelApiService/ListModels"},
    {"method": "POST", "path": "v1/models.ModelApiService/WellKnowEndpoint"},
    {"method": "POST", "path": "v1/models.ModelProxyApiService/GetModelProxyQuotas"},
    {"method": "POST", "path": "v1/common.OperationsService/GetOperation"},
    {"method": "POST", "path": "v1/search.SearchApiService/ListEntities"},
    {"method": "POST", "path": "v1/security.IamService/GetIamPolicy"},
    {"method": "POST", "path": "v1/security.OAuthService/IntrospectToken"},
    {"method": "POST", "path": "v1/users.GroupApiService/ListSynchronizedGroupMemberships"},
    {"method": "POST", "path": "v1/users.GroupApiService/ListUserManagedGroupMemberships"}
  ],
  "deny": []
}
```

## Endpoints

The Kaggle endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| POST | v1/admin.InboxFileService/CreateInboxFile | write | admin | Create inbox file. |
| POST | v1/agents.AgentsApiService/CreateAgent | write | agents | Create agent. |
| POST | v1/agents.AgentsApiService/CreateHarness | write | agents | Create harness. |
| POST | v1/agents.AgentsApiService/CreateHarnessVersion | write | agents | Create harness version. |
| POST | v1/agents.AgentsApiService/GetAgent | read | agents | Get agent. |
| POST | v1/agents.AgentsApiService/GetHarness | read | agents | Get harness. |
| POST | v1/agents.AgentsApiService/GetHarnessVersion | read | agents | Get harness version. |
| POST | v1/agents.AgentsApiService/ListAgents | read | agents | List agents. |
| POST | v1/agents.AgentsApiService/ListHarnesses | read | agents | List harnesses. |
| POST | v1/benchmarks.BenchmarkTasksApiService/ApiCancelBenchmarkTaskRuns | write | benchmarks | Cancel benchmark task runs. |
| POST | v1/benchmarks.BenchmarkTasksApiService/ApiGetBenchmarkSchedulerStatus | read | benchmarks | Get benchmark scheduler status. |
| POST | v1/benchmarks.BenchmarkTasksApiService/BatchScheduleBenchmarkTaskRuns | write | benchmarks | Batch schedule benchmark task runs. |
| POST | v1/benchmarks.BenchmarkTasksApiService/CreateBenchmarkTask | write | benchmarks | Create benchmark task. |
| POST | v1/benchmarks.BenchmarkTasksApiService/DownloadBenchmarkTaskRunOutput | read | benchmarks | Download benchmark task run output. |
| POST | v1/benchmarks.BenchmarkTasksApiService/GetBenchmarkTask | read | benchmarks | Get benchmark task. |
| POST | v1/benchmarks.BenchmarkTasksApiService/GetBenchmarkTaskQuota | read | benchmarks | Get benchmark task quota. |
| POST | v1/benchmarks.BenchmarkTasksApiService/GetBenchmarkTaskRunLogs | read | benchmarks | Get benchmark task run logs. |
| POST | v1/benchmarks.BenchmarkTasksApiService/ListBenchmarkTaskRuns | read | benchmarks | List benchmark task runs. |
| POST | v1/benchmarks.BenchmarkTasksApiService/ListBenchmarkTasks | read | benchmarks | List benchmark tasks. |
| POST | v1/benchmarks.BenchmarkTasksApiService/PublishBenchmarkTask | write | benchmarks | Publish benchmark task. |
| POST | v1/benchmarks.BenchmarkTasksApiService/UpdateBenchmarkTask | write | benchmarks | Update benchmark task. |
| POST | v1/benchmarks.BenchmarkTasksApiService/UpdateBenchmarkTaskVersion | write | benchmarks | Update benchmark task version. |
| POST | v1/benchmarks.BenchmarksApiService/AddTasksToBenchmark | write | benchmarks | Add tasks to benchmark. |
| POST | v1/benchmarks.BenchmarksApiService/CreateBenchmarkArenaSettings | write | benchmarks | Create benchmark arena settings. |
| POST | v1/benchmarks.BenchmarksApiService/CreateBenchmarkModelVersionConfig | write | benchmarks | Create benchmark model version config. |
| POST | v1/benchmarks.BenchmarksApiService/CreateBenchmarkVersionAgentMappings | write | benchmarks | Create benchmark version agent mappings. |
| POST | v1/benchmarks.BenchmarksApiService/DeleteBenchmarkVersionAgentMappings | write | benchmarks | Delete benchmark version agent mappings. |
| POST | v1/benchmarks.BenchmarksApiService/GetBenchmarkArenaSettings | read | benchmarks | Get benchmark arena settings. |
| POST | v1/benchmarks.BenchmarksApiService/GetBenchmarkLeaderboard | read | benchmarks | Get benchmark leaderboard. |
| POST | v1/benchmarks.BenchmarksApiService/GetBenchmarkModelVersionConfig | read | benchmarks | Get benchmark model version config. |
| POST | v1/benchmarks.BenchmarksApiService/ListBenchmarkArenaCombinations | read | benchmarks | List benchmark arena combinations. |
| POST | v1/benchmarks.BenchmarksApiService/ListBenchmarkModelVersionConfigs | read | benchmarks | List benchmark model version configs. |
| POST | v1/benchmarks.BenchmarksApiService/ListBenchmarkModels | read | benchmarks | List benchmark models. |
| POST | v1/benchmarks.BenchmarksApiService/ListBenchmarkVersionAgentMappings | read | benchmarks | List benchmark version agent mappings. |
| POST | v1/benchmarks.BenchmarksApiService/RegisterAuxiliaryModelVersionConfigs | write | benchmarks | Register auxiliary model version configs. |
| POST | v1/benchmarks.BenchmarksApiService/RemoveTasksFromBenchmark | write | benchmarks | Remove tasks from benchmark. |
| POST | v1/benchmarks.BenchmarksApiService/UnregisterAuxiliaryModelVersionConfigs | write | benchmarks | Unregister auxiliary model version configs. |
| POST | v1/benchmarks.BenchmarksApiService/UpdateBenchmarkArenaCombinations | write | benchmarks | Update benchmark arena combinations. |
| POST | v1/benchmarks.BenchmarksApiService/UpdateBenchmarkArenaSettings | write | benchmarks | Update benchmark arena settings. |
| POST | v1/blobs.BlobApiService/StartBlobUpload | write | blobs | Start blob upload. |
| POST | v1/competitions.CompetitionApiService/AddCompetitionHost | write | competitions | Add competition host. |
| POST | v1/competitions.CompetitionApiService/AddCompetitionJudge | write | competitions | Add competition judge. |
| POST | v1/competitions.CompetitionApiService/CreateCodeSubmission | write | competitions | Create code submission. |
| POST | v1/competitions.CompetitionApiService/CreateCompetition | write | competitions | Create competition. |
| POST | v1/competitions.CompetitionApiService/CreateCompetitionData | write | competitions | Create competition data. |
| POST | v1/competitions.CompetitionApiService/CreateCompetitionPage | write | competitions | Create competition page. |
| POST | v1/competitions.CompetitionApiService/CreateCompetitionSampleSubmission | write | competitions | Create competition sample submission. |
| POST | v1/competitions.CompetitionApiService/CreateCompetitionSolution | write | competitions | Create competition solution. |
| POST | v1/competitions.CompetitionApiService/CreateSubmission | write | competitions | Create submission. |
| POST | v1/competitions.CompetitionApiService/DeleteCompetitionPage | write | competitions | Delete competition page. |
| POST | v1/competitions.CompetitionApiService/DownloadDataFile | read | competitions | Download data file. |
| POST | v1/competitions.CompetitionApiService/DownloadDataFiles | read | competitions | Download data files. |
| POST | v1/competitions.CompetitionApiService/DownloadLeaderboard | read | competitions | Download leaderboard. |
| POST | v1/competitions.CompetitionApiService/DownloadSubmission | read | competitions | Download submission. |
| POST | v1/competitions.CompetitionApiService/GetCompetition | read | competitions | Get competition. |
| POST | v1/competitions.CompetitionApiService/GetCompetitionDataFilesSummary | read | competitions | Get competition data files summary. |
| POST | v1/competitions.CompetitionApiService/GetCompetitionSettings | read | competitions | Get competition settings. |
| POST | v1/competitions.CompetitionApiService/GetCompetitionSolutionStatus | read | competitions | Get competition solution status. |
| POST | v1/competitions.CompetitionApiService/GetEpisodeAgentLogs | read | competitions | Get episode agent logs. |
| POST | v1/competitions.CompetitionApiService/GetEpisodeReplay | read | competitions | Get episode replay. |
| POST | v1/competitions.CompetitionApiService/GetLeaderboard | read | competitions | Get leaderboard. |
| POST | v1/competitions.CompetitionApiService/GetSubmission | read | competitions | Get submission. |
| POST | v1/competitions.CompetitionApiService/GetSubmissionLimits | read | competitions | Get submission limits. |
| POST | v1/competitions.CompetitionApiService/LaunchCompetition | write | competitions | Launch competition. |
| POST | v1/competitions.CompetitionApiService/ListCompetitionHosts | read | competitions | List competition hosts. |
| POST | v1/competitions.CompetitionApiService/ListCompetitionJudges | read | competitions | List competition judges. |
| POST | v1/competitions.CompetitionApiService/ListCompetitionPages | read | competitions | List competition pages. |
| POST | v1/competitions.CompetitionApiService/ListCompetitionTopics | read | competitions | List competition topics. |
| POST | v1/competitions.CompetitionApiService/ListCompetitions | read | competitions | List competitions. |
| POST | v1/competitions.CompetitionApiService/ListDataFiles | read | competitions | List data files. |
| POST | v1/competitions.CompetitionApiService/ListDataTreeFiles | read | competitions | List data tree files. |
| POST | v1/competitions.CompetitionApiService/ListSubmissionEpisodes | read | competitions | List submission episodes. |
| POST | v1/competitions.CompetitionApiService/ListSubmissions | read | competitions | List submissions. |
| POST | v1/competitions.CompetitionApiService/ListTeamPublicSubmissions | read | competitions | List team public submissions. |
| POST | v1/competitions.CompetitionApiService/ListTopicMessages | read | competitions | List topic messages. |
| POST | v1/competitions.CompetitionApiService/StartSubmissionUpload | write | competitions | Start submission upload. |
| POST | v1/competitions.CompetitionApiService/UpdateCompetitionPage | write | competitions | Update competition page. |
| POST | v1/competitions.CompetitionApiService/UpdateCompetitionSettings | write | competitions | Update competition settings. |
| POST | v1/competitions.CompetitionApiService/UpdateSubmissionBenchmark | write | competitions | Update submission benchmark. |
| POST | v1/datasets.DatasetApiService/CreateDataset | write | datasets | Create dataset. |
| POST | v1/datasets.DatasetApiService/CreateDatasetVersion | write | datasets | Create dataset version. |
| POST | v1/datasets.DatasetApiService/CreateDatasetVersionById | write | datasets | Create dataset version by id. |
| POST | v1/datasets.DatasetApiService/DeleteDataset | write | datasets | Delete dataset. |
| POST | v1/datasets.DatasetApiService/DownloadDataset | read | datasets | Download dataset. |
| POST | v1/datasets.DatasetApiService/DownloadDatasetRaw | read | datasets | Download dataset raw. |
| POST | v1/datasets.DatasetApiService/GetDataset | read | datasets | Get dataset. |
| POST | v1/datasets.DatasetApiService/GetDatasetFilesSummary | read | datasets | Get dataset files summary. |
| POST | v1/datasets.DatasetApiService/GetDatasetMetadata | read | datasets | Get dataset metadata. |
| POST | v1/datasets.DatasetApiService/GetDatasetStatus | read | datasets | Get dataset status. |
| POST | v1/datasets.DatasetApiService/ListDatasetFiles | read | datasets | List dataset files. |
| POST | v1/datasets.DatasetApiService/ListDatasets | read | datasets | List datasets. |
| POST | v1/datasets.DatasetApiService/ListTreeDatasetFiles | read | datasets | List tree dataset files. |
| POST | v1/datasets.DatasetApiService/UpdateDatasetMetadata | write | datasets | Update dataset metadata. |
| POST | v1/datasets.DatasetApiService/UploadDatasetFile | write | datasets | Upload dataset file. |
| POST | v1/discussions.DiscussionApiService/GetTopic | read | discussions | Get topic. |
| POST | v1/discussions.DiscussionApiService/ListBenchmarkTopics | read | discussions | List benchmark topics. |
| POST | v1/discussions.DiscussionApiService/ListComments | read | discussions | List comments. |
| POST | v1/discussions.DiscussionApiService/ListDatasetTopics | read | discussions | List dataset topics. |
| POST | v1/discussions.DiscussionApiService/ListForums | read | discussions | List forums. |
| POST | v1/discussions.DiscussionApiService/ListKernelTopics | read | discussions | List kernel topics. |
| POST | v1/discussions.DiscussionApiService/ListModelTopics | read | discussions | List model topics. |
| POST | v1/discussions.DiscussionApiService/ListTopics | read | discussions | List topics. |
| POST | v1/discussions.WriteUpsApiService/GetResolvedWriteUpLinks | read | discussions | Get resolved write up links. |
| POST | v1/education.EducationApiService/TrackExerciseInteraction | write | education | Track exercise interaction. |
| POST | v1/competitions.HackathonApiService/ExportHackathonWriteUpsCsv | read | hackathons | Export hackathon write ups csv. |
| POST | v1/competitions.HackathonApiService/GetHackathonOverview | read | hackathons | Get hackathon overview. |
| POST | v1/competitions.HackathonApiService/GetHackathonWriteUp | read | hackathons | Get hackathon write up. |
| POST | v1/competitions.HackathonApiService/ListHackathonTracks | read | hackathons | List hackathon tracks. |
| POST | v1/competitions.HackathonApiService/ListHackathonWriteUps | read | hackathons | List hackathon write ups. |
| POST | v1/competitions.HackathonService/ExportEnrichedHackathonWriteUpsCsv | read | hackathons | Export enriched hackathon write ups csv. |
| POST | v1/kernels.KernelsApiService/CancelKernelSession | write | kernels | Cancel kernel session. |
| POST | v1/kernels.KernelsApiService/CreateKernelSession | write | kernels | Create kernel session. |
| POST | v1/kernels.KernelsApiService/DeleteKernel | write | kernels | Delete kernel. |
| POST | v1/kernels.KernelsApiService/DownloadKernelOutput | read | kernels | Download kernel output. |
| POST | v1/kernels.KernelsApiService/DownloadKernelOutputZip | read | kernels | Download kernel output zip. |
| POST | v1/kernels.KernelsApiService/GetAcceleratorQuotaStatistics | read | kernels | Get accelerator quota statistics. |
| POST | v1/kernels.KernelsApiService/GetKernel | read | kernels | Get kernel. |
| POST | v1/kernels.KernelsApiService/GetKernelSessionLogsStream | read | kernels | Get kernel session logs stream. |
| POST | v1/kernels.KernelsApiService/GetKernelSessionStatus | read | kernels | Get kernel session status. |
| POST | v1/kernels.KernelsApiService/ListKernelFiles | read | kernels | List kernel files. |
| POST | v1/kernels.KernelsApiService/ListKernelSessionOutput | read | kernels | List kernel session output. |
| POST | v1/kernels.KernelsApiService/ListKernels | read | kernels | List kernels. |
| POST | v1/kernels.KernelsApiService/SaveKernel | write | kernels | Save kernel. |
| POST | v1/models.ModelApiService/CreateModel | write | models | Create model. |
| POST | v1/models.ModelApiService/CreateModelInstance | write | models | Create model instance. |
| POST | v1/models.ModelApiService/CreateModelInstanceVersion | write | models | Create model instance version. |
| POST | v1/models.ModelApiService/CreateModelSigningToken | write | models | Create model signing token. |
| POST | v1/models.ModelApiService/DeleteModel | write | models | Delete model. |
| POST | v1/models.ModelApiService/DeleteModelInstance | write | models | Delete model instance. |
| POST | v1/models.ModelApiService/DeleteModelInstanceVersion | write | models | Delete model instance version. |
| POST | v1/models.ModelApiService/DownloadModelInstanceVersion | read | models | Download model instance version. |
| POST | v1/models.ModelApiService/GetModel | read | models | Get model. |
| POST | v1/models.ModelApiService/GetModelInstance | read | models | Get model instance. |
| POST | v1/models.ModelApiService/Keys | read | models | Keys. |
| POST | v1/models.ModelApiService/ListModelGatingUserConsents | read | models | List model gating user consents. |
| POST | v1/models.ModelApiService/ListModelInstanceVersionFiles | read | models | List model instance version files. |
| POST | v1/models.ModelApiService/ListModelInstanceVersions | read | models | List model instance versions. |
| POST | v1/models.ModelApiService/ListModelInstances | read | models | List model instances. |
| POST | v1/models.ModelApiService/ListModels | read | models | List models. |
| POST | v1/models.ModelApiService/ReviewModelGatingUserConsent | write | models | Review model gating user consent. |
| POST | v1/models.ModelApiService/UpdateModel | write | models | Update model. |
| POST | v1/models.ModelApiService/UpdateModelInstance | write | models | Update model instance. |
| POST | v1/models.ModelApiService/UploadModelFile | write | models | Upload model file. |
| POST | v1/models.ModelApiService/WellKnowEndpoint | read | models | Well know endpoint. |
| POST | v1/models.ModelProxyApiService/CreateDefaultModelProxyToken | write | models | Create default model proxy token. |
| POST | v1/models.ModelProxyApiService/GetModelProxyQuotas | read | models | Get model proxy quotas. |
| POST | v1/common.OperationsService/GetOperation | read | operations | Get operation. |
| POST | v1/search.SearchApiService/ListEntities | read | search | List entities. |
| POST | v1/security.IamService/GetIamPolicy | read | security | Get iam policy. |
| POST | v1/security.IamService/SetIamPolicy | write | security | Set iam policy. |
| POST | v1/security.OAuthService/ExchangeOAuthToken | write | security | Exchange oauth token. |
| POST | v1/security.OAuthService/IntrospectToken | read | security | Introspect token. |
| POST | v1/security.OAuthService/RegisterOAuthClient | write | security | Register oauth client. |
| POST | v1/security.OAuthService/StartOAuthFlow | write | security | Start oauth flow. |
| POST | v1/users.AccountService/ExpireApiToken | write | users | Expire api token. |
| POST | v1/users.AccountService/GenerateAccessToken | write | users | Generate access token. |
| POST | v1/users.GroupApiService/ListSynchronizedGroupMemberships | read | users | List synchronized group memberships. |
| POST | v1/users.GroupApiService/ListUserManagedGroupMemberships | read | users | List user managed group memberships. |
