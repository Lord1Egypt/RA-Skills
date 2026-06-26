// @bun
// node_modules/komodo_client/dist/terminal.js
var terminal_methods = (url, state) => {
  const connect_terminal = ({ query, on_message, on_login, on_open, on_close }) => {
    const url_query = new URLSearchParams(query).toString();
    const ws = new WebSocket(url.replace("http", "ws") + "/ws/terminal?" + url_query);
    ws.onopen = () => {
      const login_msg = state.jwt ? {
        type: "Jwt",
        params: {
          jwt: state.jwt
        }
      } : {
        type: "ApiKeys",
        params: {
          key: state.key,
          secret: state.secret
        }
      };
      ws.send(JSON.stringify(login_msg));
      on_open?.();
    };
    ws.onmessage = (e) => {
      if (e.data == "LOGGED_IN") {
        ws.binaryType = "arraybuffer";
        ws.onmessage = (e2) => on_message?.(e2);
        on_login?.();
        return;
      } else {
        on_message?.(e);
      }
    };
    ws.onclose = () => on_close?.();
    return ws;
  };
  const execute_terminal = async (request, callbacks) => {
    const stream = await execute_terminal_stream(request);
    for await (const line of stream) {
      if (line.startsWith("__KOMODO_EXIT_CODE")) {
        await callbacks?.onFinish?.(line.split(":")[1]);
        return;
      } else {
        await callbacks?.onLine?.(line);
      }
    }
    await callbacks?.onFinish?.("Early exit without code");
  };
  const execute_terminal_stream = (request) => execute_stream("/terminal/execute", request);
  const connect_container_exec = ({ query, ...callbacks }) => connect_exec({ query: { type: "container", query }, ...callbacks });
  const connect_deployment_exec = ({ query, ...callbacks }) => connect_exec({ query: { type: "deployment", query }, ...callbacks });
  const connect_stack_exec = ({ query, ...callbacks }) => connect_exec({ query: { type: "stack", query }, ...callbacks });
  const connect_exec = ({ query: { type, query }, on_message, on_login, on_open, on_close }) => {
    const url_query = new URLSearchParams(query).toString();
    const ws = new WebSocket(url.replace("http", "ws") + `/ws/${type}/terminal?` + url_query);
    ws.onopen = () => {
      const login_msg = state.jwt ? {
        type: "Jwt",
        params: {
          jwt: state.jwt
        }
      } : {
        type: "ApiKeys",
        params: {
          key: state.key,
          secret: state.secret
        }
      };
      ws.send(JSON.stringify(login_msg));
      on_open?.();
    };
    ws.onmessage = (e) => {
      if (e.data == "LOGGED_IN") {
        ws.binaryType = "arraybuffer";
        ws.onmessage = (e2) => on_message?.(e2);
        on_login?.();
        return;
      } else {
        on_message?.(e);
      }
    };
    ws.onclose = () => on_close?.();
    return ws;
  };
  const execute_container_exec = (body, callbacks) => execute_exec({ type: "container", body }, callbacks);
  const execute_deployment_exec = (body, callbacks) => execute_exec({ type: "deployment", body }, callbacks);
  const execute_stack_exec = (body, callbacks) => execute_exec({ type: "stack", body }, callbacks);
  const execute_exec = async (request, callbacks) => {
    const stream = await execute_exec_stream(request);
    for await (const line of stream) {
      if (line.startsWith("__KOMODO_EXIT_CODE")) {
        await callbacks?.onFinish?.(line.split(":")[1]);
        return;
      } else {
        await callbacks?.onLine?.(line);
      }
    }
    await callbacks?.onFinish?.("Early exit without code");
  };
  const execute_container_exec_stream = (body) => execute_exec_stream({ type: "container", body });
  const execute_deployment_exec_stream = (body) => execute_exec_stream({ type: "deployment", body });
  const execute_stack_exec_stream = (body) => execute_exec_stream({ type: "stack", body });
  const execute_exec_stream = (request) => execute_stream(`/terminal/execute/${request.type}`, request.body);
  const execute_stream = (path, request) => new Promise(async (res, rej) => {
    try {
      let response = await fetch(url + path, {
        method: "POST",
        body: JSON.stringify(request),
        headers: {
          ...state.jwt ? {
            authorization: state.jwt
          } : state.key && state.secret ? {
            "x-api-key": state.key,
            "x-api-secret": state.secret
          } : {},
          "content-type": "application/json"
        }
      });
      if (response.status === 200) {
        if (response.body) {
          const stream = response.body.pipeThrough(new TextDecoderStream("utf-8")).pipeThrough(new TransformStream({
            start(_controller) {
              this.tail = "";
            },
            transform(chunk, controller) {
              const data = this.tail + chunk;
              const parts = data.split(/\r?\n/);
              this.tail = parts.pop();
              for (const line of parts)
                controller.enqueue(line);
            },
            flush(controller) {
              if (this.tail)
                controller.enqueue(this.tail);
            }
          }));
          res(stream);
        } else {
          rej({
            status: response.status,
            result: { error: "No response body", trace: [] }
          });
        }
      } else {
        try {
          const result = await response.json();
          rej({ status: response.status, result });
        } catch (error) {
          rej({
            status: response.status,
            result: {
              error: "Failed to get response body",
              trace: [JSON.stringify(error)]
            },
            error
          });
        }
      }
    } catch (error) {
      rej({
        status: 1,
        result: {
          error: "Request failed with error",
          trace: [JSON.stringify(error)]
        },
        error
      });
    }
  });
  return {
    connect_terminal,
    execute_terminal,
    execute_terminal_stream,
    connect_exec,
    connect_container_exec,
    execute_container_exec,
    execute_container_exec_stream,
    connect_deployment_exec,
    execute_deployment_exec,
    execute_deployment_exec_stream,
    connect_stack_exec,
    execute_stack_exec,
    execute_stack_exec_stream
  };
};

// node_modules/komodo_client/dist/types.js
var PermissionLevel;
(function(PermissionLevel2) {
  PermissionLevel2["None"] = "None";
  PermissionLevel2["Read"] = "Read";
  PermissionLevel2["Execute"] = "Execute";
  PermissionLevel2["Write"] = "Write";
})(PermissionLevel || (PermissionLevel = {}));
var ScheduleFormat;
(function(ScheduleFormat2) {
  ScheduleFormat2["English"] = "English";
  ScheduleFormat2["Cron"] = "Cron";
})(ScheduleFormat || (ScheduleFormat = {}));
var FileFormat;
(function(FileFormat2) {
  FileFormat2["KeyValue"] = "key_value";
  FileFormat2["Toml"] = "toml";
  FileFormat2["Yaml"] = "yaml";
  FileFormat2["Json"] = "json";
})(FileFormat || (FileFormat = {}));
var ActionState;
(function(ActionState2) {
  ActionState2["Unknown"] = "Unknown";
  ActionState2["Ok"] = "Ok";
  ActionState2["Failed"] = "Failed";
  ActionState2["Running"] = "Running";
})(ActionState || (ActionState = {}));
var TemplatesQueryBehavior;
(function(TemplatesQueryBehavior2) {
  TemplatesQueryBehavior2["Include"] = "Include";
  TemplatesQueryBehavior2["Exclude"] = "Exclude";
  TemplatesQueryBehavior2["Only"] = "Only";
})(TemplatesQueryBehavior || (TemplatesQueryBehavior = {}));
var TagQueryBehavior;
(function(TagQueryBehavior2) {
  TagQueryBehavior2["All"] = "All";
  TagQueryBehavior2["Any"] = "Any";
})(TagQueryBehavior || (TagQueryBehavior = {}));
var MaintenanceScheduleType;
(function(MaintenanceScheduleType2) {
  MaintenanceScheduleType2["Daily"] = "Daily";
  MaintenanceScheduleType2["Weekly"] = "Weekly";
  MaintenanceScheduleType2["OneTime"] = "OneTime";
})(MaintenanceScheduleType || (MaintenanceScheduleType = {}));
var Operation;
(function(Operation2) {
  Operation2["None"] = "None";
  Operation2["CreateServer"] = "CreateServer";
  Operation2["UpdateServer"] = "UpdateServer";
  Operation2["DeleteServer"] = "DeleteServer";
  Operation2["RenameServer"] = "RenameServer";
  Operation2["StartContainer"] = "StartContainer";
  Operation2["RestartContainer"] = "RestartContainer";
  Operation2["PauseContainer"] = "PauseContainer";
  Operation2["UnpauseContainer"] = "UnpauseContainer";
  Operation2["StopContainer"] = "StopContainer";
  Operation2["DestroyContainer"] = "DestroyContainer";
  Operation2["StartAllContainers"] = "StartAllContainers";
  Operation2["RestartAllContainers"] = "RestartAllContainers";
  Operation2["PauseAllContainers"] = "PauseAllContainers";
  Operation2["UnpauseAllContainers"] = "UnpauseAllContainers";
  Operation2["StopAllContainers"] = "StopAllContainers";
  Operation2["PruneContainers"] = "PruneContainers";
  Operation2["CreateNetwork"] = "CreateNetwork";
  Operation2["DeleteNetwork"] = "DeleteNetwork";
  Operation2["PruneNetworks"] = "PruneNetworks";
  Operation2["DeleteImage"] = "DeleteImage";
  Operation2["PruneImages"] = "PruneImages";
  Operation2["DeleteVolume"] = "DeleteVolume";
  Operation2["PruneVolumes"] = "PruneVolumes";
  Operation2["PruneDockerBuilders"] = "PruneDockerBuilders";
  Operation2["PruneBuildx"] = "PruneBuildx";
  Operation2["PruneSystem"] = "PruneSystem";
  Operation2["CreateStack"] = "CreateStack";
  Operation2["UpdateStack"] = "UpdateStack";
  Operation2["RenameStack"] = "RenameStack";
  Operation2["DeleteStack"] = "DeleteStack";
  Operation2["WriteStackContents"] = "WriteStackContents";
  Operation2["RefreshStackCache"] = "RefreshStackCache";
  Operation2["PullStack"] = "PullStack";
  Operation2["DeployStack"] = "DeployStack";
  Operation2["StartStack"] = "StartStack";
  Operation2["RestartStack"] = "RestartStack";
  Operation2["PauseStack"] = "PauseStack";
  Operation2["UnpauseStack"] = "UnpauseStack";
  Operation2["StopStack"] = "StopStack";
  Operation2["DestroyStack"] = "DestroyStack";
  Operation2["RunStackService"] = "RunStackService";
  Operation2["DeployStackService"] = "DeployStackService";
  Operation2["PullStackService"] = "PullStackService";
  Operation2["StartStackService"] = "StartStackService";
  Operation2["RestartStackService"] = "RestartStackService";
  Operation2["PauseStackService"] = "PauseStackService";
  Operation2["UnpauseStackService"] = "UnpauseStackService";
  Operation2["StopStackService"] = "StopStackService";
  Operation2["DestroyStackService"] = "DestroyStackService";
  Operation2["CreateDeployment"] = "CreateDeployment";
  Operation2["UpdateDeployment"] = "UpdateDeployment";
  Operation2["RenameDeployment"] = "RenameDeployment";
  Operation2["DeleteDeployment"] = "DeleteDeployment";
  Operation2["Deploy"] = "Deploy";
  Operation2["PullDeployment"] = "PullDeployment";
  Operation2["StartDeployment"] = "StartDeployment";
  Operation2["RestartDeployment"] = "RestartDeployment";
  Operation2["PauseDeployment"] = "PauseDeployment";
  Operation2["UnpauseDeployment"] = "UnpauseDeployment";
  Operation2["StopDeployment"] = "StopDeployment";
  Operation2["DestroyDeployment"] = "DestroyDeployment";
  Operation2["CreateBuild"] = "CreateBuild";
  Operation2["UpdateBuild"] = "UpdateBuild";
  Operation2["RenameBuild"] = "RenameBuild";
  Operation2["DeleteBuild"] = "DeleteBuild";
  Operation2["RunBuild"] = "RunBuild";
  Operation2["CancelBuild"] = "CancelBuild";
  Operation2["WriteDockerfile"] = "WriteDockerfile";
  Operation2["CreateRepo"] = "CreateRepo";
  Operation2["UpdateRepo"] = "UpdateRepo";
  Operation2["RenameRepo"] = "RenameRepo";
  Operation2["DeleteRepo"] = "DeleteRepo";
  Operation2["CloneRepo"] = "CloneRepo";
  Operation2["PullRepo"] = "PullRepo";
  Operation2["BuildRepo"] = "BuildRepo";
  Operation2["CancelRepoBuild"] = "CancelRepoBuild";
  Operation2["CreateProcedure"] = "CreateProcedure";
  Operation2["UpdateProcedure"] = "UpdateProcedure";
  Operation2["RenameProcedure"] = "RenameProcedure";
  Operation2["DeleteProcedure"] = "DeleteProcedure";
  Operation2["RunProcedure"] = "RunProcedure";
  Operation2["CreateAction"] = "CreateAction";
  Operation2["UpdateAction"] = "UpdateAction";
  Operation2["RenameAction"] = "RenameAction";
  Operation2["DeleteAction"] = "DeleteAction";
  Operation2["RunAction"] = "RunAction";
  Operation2["CreateBuilder"] = "CreateBuilder";
  Operation2["UpdateBuilder"] = "UpdateBuilder";
  Operation2["RenameBuilder"] = "RenameBuilder";
  Operation2["DeleteBuilder"] = "DeleteBuilder";
  Operation2["CreateAlerter"] = "CreateAlerter";
  Operation2["UpdateAlerter"] = "UpdateAlerter";
  Operation2["RenameAlerter"] = "RenameAlerter";
  Operation2["DeleteAlerter"] = "DeleteAlerter";
  Operation2["TestAlerter"] = "TestAlerter";
  Operation2["SendAlert"] = "SendAlert";
  Operation2["CreateResourceSync"] = "CreateResourceSync";
  Operation2["UpdateResourceSync"] = "UpdateResourceSync";
  Operation2["RenameResourceSync"] = "RenameResourceSync";
  Operation2["DeleteResourceSync"] = "DeleteResourceSync";
  Operation2["WriteSyncContents"] = "WriteSyncContents";
  Operation2["CommitSync"] = "CommitSync";
  Operation2["RunSync"] = "RunSync";
  Operation2["ClearRepoCache"] = "ClearRepoCache";
  Operation2["BackupCoreDatabase"] = "BackupCoreDatabase";
  Operation2["GlobalAutoUpdate"] = "GlobalAutoUpdate";
  Operation2["CreateVariable"] = "CreateVariable";
  Operation2["UpdateVariableValue"] = "UpdateVariableValue";
  Operation2["DeleteVariable"] = "DeleteVariable";
  Operation2["CreateGitProviderAccount"] = "CreateGitProviderAccount";
  Operation2["UpdateGitProviderAccount"] = "UpdateGitProviderAccount";
  Operation2["DeleteGitProviderAccount"] = "DeleteGitProviderAccount";
  Operation2["CreateDockerRegistryAccount"] = "CreateDockerRegistryAccount";
  Operation2["UpdateDockerRegistryAccount"] = "UpdateDockerRegistryAccount";
  Operation2["DeleteDockerRegistryAccount"] = "DeleteDockerRegistryAccount";
})(Operation || (Operation = {}));
var UpdateStatus;
(function(UpdateStatus2) {
  UpdateStatus2["Queued"] = "Queued";
  UpdateStatus2["InProgress"] = "InProgress";
  UpdateStatus2["Complete"] = "Complete";
})(UpdateStatus || (UpdateStatus = {}));
var BuildState;
(function(BuildState2) {
  BuildState2["Building"] = "Building";
  BuildState2["Ok"] = "Ok";
  BuildState2["Failed"] = "Failed";
  BuildState2["Unknown"] = "Unknown";
})(BuildState || (BuildState = {}));
var RestartMode;
(function(RestartMode2) {
  RestartMode2["NoRestart"] = "no";
  RestartMode2["OnFailure"] = "on-failure";
  RestartMode2["Always"] = "always";
  RestartMode2["UnlessStopped"] = "unless-stopped";
})(RestartMode || (RestartMode = {}));
var TerminationSignal;
(function(TerminationSignal2) {
  TerminationSignal2["SigHup"] = "SIGHUP";
  TerminationSignal2["SigInt"] = "SIGINT";
  TerminationSignal2["SigQuit"] = "SIGQUIT";
  TerminationSignal2["SigTerm"] = "SIGTERM";
})(TerminationSignal || (TerminationSignal = {}));
var DeploymentState;
(function(DeploymentState2) {
  DeploymentState2["Deploying"] = "deploying";
  DeploymentState2["Running"] = "running";
  DeploymentState2["Created"] = "created";
  DeploymentState2["Restarting"] = "restarting";
  DeploymentState2["Removing"] = "removing";
  DeploymentState2["Paused"] = "paused";
  DeploymentState2["Exited"] = "exited";
  DeploymentState2["Dead"] = "dead";
  DeploymentState2["NotDeployed"] = "not_deployed";
  DeploymentState2["Unknown"] = "unknown";
})(DeploymentState || (DeploymentState = {}));
var SeverityLevel;
(function(SeverityLevel2) {
  SeverityLevel2["Ok"] = "OK";
  SeverityLevel2["Warning"] = "WARNING";
  SeverityLevel2["Critical"] = "CRITICAL";
})(SeverityLevel || (SeverityLevel = {}));
var StackFileRequires;
(function(StackFileRequires2) {
  StackFileRequires2["Redeploy"] = "Redeploy";
  StackFileRequires2["Restart"] = "Restart";
  StackFileRequires2["None"] = "None";
})(StackFileRequires || (StackFileRequires = {}));
var Timelength;
(function(Timelength2) {
  Timelength2["OneSecond"] = "1-sec";
  Timelength2["FiveSeconds"] = "5-sec";
  Timelength2["TenSeconds"] = "10-sec";
  Timelength2["FifteenSeconds"] = "15-sec";
  Timelength2["ThirtySeconds"] = "30-sec";
  Timelength2["OneMinute"] = "1-min";
  Timelength2["TwoMinutes"] = "2-min";
  Timelength2["FiveMinutes"] = "5-min";
  Timelength2["TenMinutes"] = "10-min";
  Timelength2["FifteenMinutes"] = "15-min";
  Timelength2["ThirtyMinutes"] = "30-min";
  Timelength2["OneHour"] = "1-hr";
  Timelength2["TwoHours"] = "2-hr";
  Timelength2["SixHours"] = "6-hr";
  Timelength2["EightHours"] = "8-hr";
  Timelength2["TwelveHours"] = "12-hr";
  Timelength2["OneDay"] = "1-day";
  Timelength2["ThreeDay"] = "3-day";
  Timelength2["OneWeek"] = "1-wk";
  Timelength2["TwoWeeks"] = "2-wk";
  Timelength2["ThirtyDays"] = "30-day";
})(Timelength || (Timelength = {}));
var TagColor;
(function(TagColor2) {
  TagColor2["LightSlate"] = "LightSlate";
  TagColor2["Slate"] = "Slate";
  TagColor2["DarkSlate"] = "DarkSlate";
  TagColor2["LightRed"] = "LightRed";
  TagColor2["Red"] = "Red";
  TagColor2["DarkRed"] = "DarkRed";
  TagColor2["LightOrange"] = "LightOrange";
  TagColor2["Orange"] = "Orange";
  TagColor2["DarkOrange"] = "DarkOrange";
  TagColor2["LightAmber"] = "LightAmber";
  TagColor2["Amber"] = "Amber";
  TagColor2["DarkAmber"] = "DarkAmber";
  TagColor2["LightYellow"] = "LightYellow";
  TagColor2["Yellow"] = "Yellow";
  TagColor2["DarkYellow"] = "DarkYellow";
  TagColor2["LightLime"] = "LightLime";
  TagColor2["Lime"] = "Lime";
  TagColor2["DarkLime"] = "DarkLime";
  TagColor2["LightGreen"] = "LightGreen";
  TagColor2["Green"] = "Green";
  TagColor2["DarkGreen"] = "DarkGreen";
  TagColor2["LightEmerald"] = "LightEmerald";
  TagColor2["Emerald"] = "Emerald";
  TagColor2["DarkEmerald"] = "DarkEmerald";
  TagColor2["LightTeal"] = "LightTeal";
  TagColor2["Teal"] = "Teal";
  TagColor2["DarkTeal"] = "DarkTeal";
  TagColor2["LightCyan"] = "LightCyan";
  TagColor2["Cyan"] = "Cyan";
  TagColor2["DarkCyan"] = "DarkCyan";
  TagColor2["LightSky"] = "LightSky";
  TagColor2["Sky"] = "Sky";
  TagColor2["DarkSky"] = "DarkSky";
  TagColor2["LightBlue"] = "LightBlue";
  TagColor2["Blue"] = "Blue";
  TagColor2["DarkBlue"] = "DarkBlue";
  TagColor2["LightIndigo"] = "LightIndigo";
  TagColor2["Indigo"] = "Indigo";
  TagColor2["DarkIndigo"] = "DarkIndigo";
  TagColor2["LightViolet"] = "LightViolet";
  TagColor2["Violet"] = "Violet";
  TagColor2["DarkViolet"] = "DarkViolet";
  TagColor2["LightPurple"] = "LightPurple";
  TagColor2["Purple"] = "Purple";
  TagColor2["DarkPurple"] = "DarkPurple";
  TagColor2["LightFuchsia"] = "LightFuchsia";
  TagColor2["Fuchsia"] = "Fuchsia";
  TagColor2["DarkFuchsia"] = "DarkFuchsia";
  TagColor2["LightPink"] = "LightPink";
  TagColor2["Pink"] = "Pink";
  TagColor2["DarkPink"] = "DarkPink";
  TagColor2["LightRose"] = "LightRose";
  TagColor2["Rose"] = "Rose";
  TagColor2["DarkRose"] = "DarkRose";
})(TagColor || (TagColor = {}));
var ContainerStateStatusEnum;
(function(ContainerStateStatusEnum2) {
  ContainerStateStatusEnum2["Running"] = "running";
  ContainerStateStatusEnum2["Created"] = "created";
  ContainerStateStatusEnum2["Paused"] = "paused";
  ContainerStateStatusEnum2["Restarting"] = "restarting";
  ContainerStateStatusEnum2["Exited"] = "exited";
  ContainerStateStatusEnum2["Removing"] = "removing";
  ContainerStateStatusEnum2["Dead"] = "dead";
  ContainerStateStatusEnum2["Empty"] = "";
})(ContainerStateStatusEnum || (ContainerStateStatusEnum = {}));
var HealthStatusEnum;
(function(HealthStatusEnum2) {
  HealthStatusEnum2["Empty"] = "";
  HealthStatusEnum2["None"] = "none";
  HealthStatusEnum2["Starting"] = "starting";
  HealthStatusEnum2["Healthy"] = "healthy";
  HealthStatusEnum2["Unhealthy"] = "unhealthy";
})(HealthStatusEnum || (HealthStatusEnum = {}));
var RestartPolicyNameEnum;
(function(RestartPolicyNameEnum2) {
  RestartPolicyNameEnum2["Empty"] = "";
  RestartPolicyNameEnum2["No"] = "no";
  RestartPolicyNameEnum2["Always"] = "always";
  RestartPolicyNameEnum2["UnlessStopped"] = "unless-stopped";
  RestartPolicyNameEnum2["OnFailure"] = "on-failure";
})(RestartPolicyNameEnum || (RestartPolicyNameEnum = {}));
var MountTypeEnum;
(function(MountTypeEnum2) {
  MountTypeEnum2["Empty"] = "";
  MountTypeEnum2["Bind"] = "bind";
  MountTypeEnum2["Volume"] = "volume";
  MountTypeEnum2["Image"] = "image";
  MountTypeEnum2["Tmpfs"] = "tmpfs";
  MountTypeEnum2["Npipe"] = "npipe";
  MountTypeEnum2["Cluster"] = "cluster";
})(MountTypeEnum || (MountTypeEnum = {}));
var MountBindOptionsPropagationEnum;
(function(MountBindOptionsPropagationEnum2) {
  MountBindOptionsPropagationEnum2["Empty"] = "";
  MountBindOptionsPropagationEnum2["Private"] = "private";
  MountBindOptionsPropagationEnum2["Rprivate"] = "rprivate";
  MountBindOptionsPropagationEnum2["Shared"] = "shared";
  MountBindOptionsPropagationEnum2["Rshared"] = "rshared";
  MountBindOptionsPropagationEnum2["Slave"] = "slave";
  MountBindOptionsPropagationEnum2["Rslave"] = "rslave";
})(MountBindOptionsPropagationEnum || (MountBindOptionsPropagationEnum = {}));
var HostConfigCgroupnsModeEnum;
(function(HostConfigCgroupnsModeEnum2) {
  HostConfigCgroupnsModeEnum2["Empty"] = "";
  HostConfigCgroupnsModeEnum2["Private"] = "private";
  HostConfigCgroupnsModeEnum2["Host"] = "host";
})(HostConfigCgroupnsModeEnum || (HostConfigCgroupnsModeEnum = {}));
var HostConfigIsolationEnum;
(function(HostConfigIsolationEnum2) {
  HostConfigIsolationEnum2["Empty"] = "";
  HostConfigIsolationEnum2["Default"] = "default";
  HostConfigIsolationEnum2["Process"] = "process";
  HostConfigIsolationEnum2["Hyperv"] = "hyperv";
})(HostConfigIsolationEnum || (HostConfigIsolationEnum = {}));
var VolumeScopeEnum;
(function(VolumeScopeEnum2) {
  VolumeScopeEnum2["Empty"] = "";
  VolumeScopeEnum2["Local"] = "local";
  VolumeScopeEnum2["Global"] = "global";
})(VolumeScopeEnum || (VolumeScopeEnum = {}));
var ClusterVolumeSpecAccessModeScopeEnum;
(function(ClusterVolumeSpecAccessModeScopeEnum2) {
  ClusterVolumeSpecAccessModeScopeEnum2["Empty"] = "";
  ClusterVolumeSpecAccessModeScopeEnum2["Single"] = "single";
  ClusterVolumeSpecAccessModeScopeEnum2["Multi"] = "multi";
})(ClusterVolumeSpecAccessModeScopeEnum || (ClusterVolumeSpecAccessModeScopeEnum = {}));
var ClusterVolumeSpecAccessModeSharingEnum;
(function(ClusterVolumeSpecAccessModeSharingEnum2) {
  ClusterVolumeSpecAccessModeSharingEnum2["Empty"] = "";
  ClusterVolumeSpecAccessModeSharingEnum2["None"] = "none";
  ClusterVolumeSpecAccessModeSharingEnum2["Readonly"] = "readonly";
  ClusterVolumeSpecAccessModeSharingEnum2["Onewriter"] = "onewriter";
  ClusterVolumeSpecAccessModeSharingEnum2["All"] = "all";
})(ClusterVolumeSpecAccessModeSharingEnum || (ClusterVolumeSpecAccessModeSharingEnum = {}));
var ClusterVolumeSpecAccessModeAvailabilityEnum;
(function(ClusterVolumeSpecAccessModeAvailabilityEnum2) {
  ClusterVolumeSpecAccessModeAvailabilityEnum2["Empty"] = "";
  ClusterVolumeSpecAccessModeAvailabilityEnum2["Active"] = "active";
  ClusterVolumeSpecAccessModeAvailabilityEnum2["Pause"] = "pause";
  ClusterVolumeSpecAccessModeAvailabilityEnum2["Drain"] = "drain";
})(ClusterVolumeSpecAccessModeAvailabilityEnum || (ClusterVolumeSpecAccessModeAvailabilityEnum = {}));
var ClusterVolumePublishStatusStateEnum;
(function(ClusterVolumePublishStatusStateEnum2) {
  ClusterVolumePublishStatusStateEnum2["Empty"] = "";
  ClusterVolumePublishStatusStateEnum2["PendingPublish"] = "pending-publish";
  ClusterVolumePublishStatusStateEnum2["Published"] = "published";
  ClusterVolumePublishStatusStateEnum2["PendingNodeUnpublish"] = "pending-node-unpublish";
  ClusterVolumePublishStatusStateEnum2["PendingControllerUnpublish"] = "pending-controller-unpublish";
})(ClusterVolumePublishStatusStateEnum || (ClusterVolumePublishStatusStateEnum = {}));
var PortTypeEnum;
(function(PortTypeEnum2) {
  PortTypeEnum2["EMPTY"] = "";
  PortTypeEnum2["TCP"] = "tcp";
  PortTypeEnum2["UDP"] = "udp";
  PortTypeEnum2["SCTP"] = "sctp";
})(PortTypeEnum || (PortTypeEnum = {}));
var ProcedureState;
(function(ProcedureState2) {
  ProcedureState2["Running"] = "Running";
  ProcedureState2["Ok"] = "Ok";
  ProcedureState2["Failed"] = "Failed";
  ProcedureState2["Unknown"] = "Unknown";
})(ProcedureState || (ProcedureState = {}));
var RepoState;
(function(RepoState2) {
  RepoState2["Unknown"] = "Unknown";
  RepoState2["Ok"] = "Ok";
  RepoState2["Failed"] = "Failed";
  RepoState2["Cloning"] = "Cloning";
  RepoState2["Pulling"] = "Pulling";
  RepoState2["Building"] = "Building";
})(RepoState || (RepoState = {}));
var ResourceSyncState;
(function(ResourceSyncState2) {
  ResourceSyncState2["Syncing"] = "Syncing";
  ResourceSyncState2["Pending"] = "Pending";
  ResourceSyncState2["Ok"] = "Ok";
  ResourceSyncState2["Failed"] = "Failed";
  ResourceSyncState2["Unknown"] = "Unknown";
})(ResourceSyncState || (ResourceSyncState = {}));
var ServerState;
(function(ServerState2) {
  ServerState2["Ok"] = "Ok";
  ServerState2["NotOk"] = "NotOk";
  ServerState2["Disabled"] = "Disabled";
})(ServerState || (ServerState = {}));
var StackState;
(function(StackState2) {
  StackState2["Deploying"] = "deploying";
  StackState2["Running"] = "running";
  StackState2["Paused"] = "paused";
  StackState2["Stopped"] = "stopped";
  StackState2["Created"] = "created";
  StackState2["Restarting"] = "restarting";
  StackState2["Dead"] = "dead";
  StackState2["Removing"] = "removing";
  StackState2["Unhealthy"] = "unhealthy";
  StackState2["Down"] = "down";
  StackState2["Unknown"] = "unknown";
})(StackState || (StackState = {}));
var RepoWebhookAction;
(function(RepoWebhookAction2) {
  RepoWebhookAction2["Clone"] = "Clone";
  RepoWebhookAction2["Pull"] = "Pull";
  RepoWebhookAction2["Build"] = "Build";
})(RepoWebhookAction || (RepoWebhookAction = {}));
var StackWebhookAction;
(function(StackWebhookAction2) {
  StackWebhookAction2["Refresh"] = "Refresh";
  StackWebhookAction2["Deploy"] = "Deploy";
})(StackWebhookAction || (StackWebhookAction = {}));
var SyncWebhookAction;
(function(SyncWebhookAction2) {
  SyncWebhookAction2["Refresh"] = "Refresh";
  SyncWebhookAction2["Sync"] = "Sync";
})(SyncWebhookAction || (SyncWebhookAction = {}));
var TerminalRecreateMode;
(function(TerminalRecreateMode2) {
  TerminalRecreateMode2["Never"] = "Never";
  TerminalRecreateMode2["Always"] = "Always";
  TerminalRecreateMode2["DifferentCommand"] = "DifferentCommand";
})(TerminalRecreateMode || (TerminalRecreateMode = {}));
var DefaultRepoFolder;
(function(DefaultRepoFolder2) {
  DefaultRepoFolder2["Stacks"] = "Stacks";
  DefaultRepoFolder2["Builds"] = "Builds";
  DefaultRepoFolder2["Repos"] = "Repos";
  DefaultRepoFolder2["NotApplicable"] = "NotApplicable";
})(DefaultRepoFolder || (DefaultRepoFolder = {}));
var SearchCombinator;
(function(SearchCombinator2) {
  SearchCombinator2["Or"] = "Or";
  SearchCombinator2["And"] = "And";
})(SearchCombinator || (SearchCombinator = {}));
var DayOfWeek;
(function(DayOfWeek2) {
  DayOfWeek2["Monday"] = "Monday";
  DayOfWeek2["Tuesday"] = "Tuesday";
  DayOfWeek2["Wednesday"] = "Wednesday";
  DayOfWeek2["Thursday"] = "Thursday";
  DayOfWeek2["Friday"] = "Friday";
  DayOfWeek2["Saturday"] = "Saturday";
  DayOfWeek2["Sunday"] = "Sunday";
})(DayOfWeek || (DayOfWeek = {}));
var IanaTimezone;
(function(IanaTimezone2) {
  IanaTimezone2["EtcGmtMinus12"] = "Etc/GMT+12";
  IanaTimezone2["PacificPagoPago"] = "Pacific/Pago_Pago";
  IanaTimezone2["PacificHonolulu"] = "Pacific/Honolulu";
  IanaTimezone2["PacificMarquesas"] = "Pacific/Marquesas";
  IanaTimezone2["AmericaAnchorage"] = "America/Anchorage";
  IanaTimezone2["AmericaLosAngeles"] = "America/Los_Angeles";
  IanaTimezone2["AmericaDenver"] = "America/Denver";
  IanaTimezone2["AmericaChicago"] = "America/Chicago";
  IanaTimezone2["AmericaNewYork"] = "America/New_York";
  IanaTimezone2["AmericaHalifax"] = "America/Halifax";
  IanaTimezone2["AmericaStJohns"] = "America/St_Johns";
  IanaTimezone2["AmericaSaoPaulo"] = "America/Sao_Paulo";
  IanaTimezone2["AmericaNoronha"] = "America/Noronha";
  IanaTimezone2["AtlanticAzores"] = "Atlantic/Azores";
  IanaTimezone2["EtcUtc"] = "Etc/UTC";
  IanaTimezone2["EuropeBerlin"] = "Europe/Berlin";
  IanaTimezone2["EuropeBucharest"] = "Europe/Bucharest";
  IanaTimezone2["EuropeMoscow"] = "Europe/Moscow";
  IanaTimezone2["AsiaTehran"] = "Asia/Tehran";
  IanaTimezone2["AsiaDubai"] = "Asia/Dubai";
  IanaTimezone2["AsiaKabul"] = "Asia/Kabul";
  IanaTimezone2["AsiaKarachi"] = "Asia/Karachi";
  IanaTimezone2["AsiaKolkata"] = "Asia/Kolkata";
  IanaTimezone2["AsiaKathmandu"] = "Asia/Kathmandu";
  IanaTimezone2["AsiaDhaka"] = "Asia/Dhaka";
  IanaTimezone2["AsiaYangon"] = "Asia/Yangon";
  IanaTimezone2["AsiaBangkok"] = "Asia/Bangkok";
  IanaTimezone2["AsiaShanghai"] = "Asia/Shanghai";
  IanaTimezone2["AustraliaEucla"] = "Australia/Eucla";
  IanaTimezone2["AsiaTokyo"] = "Asia/Tokyo";
  IanaTimezone2["AustraliaAdelaide"] = "Australia/Adelaide";
  IanaTimezone2["AustraliaSydney"] = "Australia/Sydney";
  IanaTimezone2["AustraliaLordHowe"] = "Australia/Lord_Howe";
  IanaTimezone2["PacificPortMoresby"] = "Pacific/Port_Moresby";
  IanaTimezone2["PacificAuckland"] = "Pacific/Auckland";
  IanaTimezone2["PacificChatham"] = "Pacific/Chatham";
  IanaTimezone2["PacificTongatapu"] = "Pacific/Tongatapu";
  IanaTimezone2["PacificKiritimati"] = "Pacific/Kiritimati";
})(IanaTimezone || (IanaTimezone = {}));
var SpecificPermission;
(function(SpecificPermission2) {
  SpecificPermission2["Terminal"] = "Terminal";
  SpecificPermission2["Attach"] = "Attach";
  SpecificPermission2["Inspect"] = "Inspect";
  SpecificPermission2["Logs"] = "Logs";
  SpecificPermission2["Processes"] = "Processes";
})(SpecificPermission || (SpecificPermission = {}));

// node_modules/komodo_client/dist/lib.js
class CancelToken {
  cancelled;
  constructor() {
    this.cancelled = false;
  }
  cancel() {
    this.cancelled = true;
  }
}
function KomodoClient(url, options) {
  const state = {
    jwt: options.type === "jwt" ? options.params.jwt : undefined,
    key: options.type === "api-key" ? options.params.key : undefined,
    secret: options.type === "api-key" ? options.params.secret : undefined
  };
  const request = (path, type, params) => new Promise(async (res, rej) => {
    try {
      let response = await fetch(`${url}${path}/${type}`, {
        method: "POST",
        body: JSON.stringify(params),
        headers: {
          ...state.jwt ? {
            authorization: state.jwt
          } : state.key && state.secret ? {
            "x-api-key": state.key,
            "x-api-secret": state.secret
          } : {},
          "content-type": "application/json"
        }
      });
      if (response.status === 200) {
        const body = await response.json();
        res(body);
      } else {
        try {
          const result = await response.json();
          rej({ status: response.status, result });
        } catch (error) {
          rej({
            status: response.status,
            result: {
              error: "Failed to get response body",
              trace: [JSON.stringify(error)]
            },
            error
          });
        }
      }
    } catch (error) {
      rej({
        status: 1,
        result: {
          error: "Request failed with error",
          trace: [JSON.stringify(error)]
        },
        error
      });
    }
  });
  const auth = async (type, params) => await request("/auth", type, params);
  const user = async (type, params) => await request("/user", type, params);
  const read = async (type, params) => await request("/read", type, params);
  const write = async (type, params) => await request("/write", type, params);
  const execute = async (type, params) => await request("/execute", type, params);
  const execute_and_poll = async (type, params) => {
    const res = await execute(type, params);
    if (Array.isArray(res)) {
      const batch = res;
      return await Promise.all(batch.map(async (item) => {
        if (item.status === "Err") {
          return item;
        }
        return await poll_update_until_complete(item.data._id?.$oid);
      }));
    } else {
      const update = res;
      if (update.status === UpdateStatus.Complete || !update._id?.$oid) {
        return update;
      }
      return await poll_update_until_complete(update._id?.$oid);
    }
  };
  const poll_update_until_complete = async (update_id) => {
    while (true) {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      const update = await read("GetUpdate", { id: update_id });
      if (update.status === UpdateStatus.Complete) {
        return update;
      }
    }
  };
  const core_version = () => read("GetVersion", {}).then((res) => res.version);
  const get_update_websocket = ({ on_update, on_login, on_open, on_close }) => {
    const ws = new WebSocket(url.replace("http", "ws") + "/ws/update");
    ws.addEventListener("open", () => {
      on_open?.();
      const login_msg = options.type === "jwt" ? {
        type: "Jwt",
        params: {
          jwt: options.params.jwt
        }
      } : {
        type: "ApiKeys",
        params: {
          key: options.params.key,
          secret: options.params.secret
        }
      };
      ws.send(JSON.stringify(login_msg));
    });
    ws.addEventListener("message", ({ data }) => {
      if (data == "LOGGED_IN")
        return on_login?.();
      on_update(JSON.parse(data));
    });
    if (on_close) {
      ws.addEventListener("close", on_close);
    }
    return ws;
  };
  const subscribe_to_update_websocket = async ({ on_update, on_open, on_login, on_close, retry = true, retry_timeout_ms = 5000, cancel = new CancelToken, on_cancel }) => {
    while (true) {
      if (cancel.cancelled) {
        on_cancel?.();
        return;
      }
      try {
        const ws = get_update_websocket({
          on_open,
          on_login,
          on_update,
          on_close
        });
        while (ws.readyState !== WebSocket.CLOSING && ws.readyState !== WebSocket.CLOSED) {
          if (cancel.cancelled)
            ws.close();
          await new Promise((resolve) => setTimeout(resolve, 500));
        }
        if (retry) {
          await new Promise((resolve) => setTimeout(resolve, retry_timeout_ms));
        } else {
          return;
        }
      } catch (error) {
        console.error(error);
        if (retry) {
          await new Promise((resolve) => setTimeout(resolve, retry_timeout_ms));
        } else {
          return;
        }
      }
    }
  };
  const { connect_terminal, execute_terminal, execute_terminal_stream, connect_exec, connect_container_exec, execute_container_exec, execute_container_exec_stream, connect_deployment_exec, execute_deployment_exec, execute_deployment_exec_stream, connect_stack_exec, execute_stack_exec, execute_stack_exec_stream } = terminal_methods(url, state);
  return {
    auth,
    user,
    read,
    write,
    execute,
    execute_and_poll,
    poll_update_until_complete,
    core_version,
    get_update_websocket,
    subscribe_to_update_websocket,
    connect_terminal,
    execute_terminal,
    execute_terminal_stream,
    connect_exec,
    connect_container_exec,
    execute_container_exec,
    execute_container_exec_stream,
    connect_deployment_exec,
    execute_deployment_exec,
    execute_deployment_exec_stream,
    connect_stack_exec,
    execute_stack_exec,
    execute_stack_exec_stream
  };
}

// openclaw.ts
var url = process.env.KOMODO_URL;
var key = process.env.KOMODO_API_KEY;
var secret = process.env.KOMODO_API_SECRET;
if (!url)
  throw new Error("Missing env: KOMODO_URL");
if (!key)
  throw new Error("Missing env: KOMODO_API_KEY");
if (!secret)
  throw new Error("Missing env: KOMODO_API_SECRET");
var komodo = KomodoClient(url, {
  type: "api-key",
  params: { key, secret }
});

// scripts/list.ts
var TYPES = ["servers", "stacks", "deployments", "builds", "repos", "procedures", "actions"];
var type = process.argv[2];
if (!type || !TYPES.includes(type)) {
  console.error("Usage: bun run scripts/list.ts <type>");
  console.error("Types:", TYPES.join(" | "));
  process.exit(1);
}
var SEP = "\u2500".repeat(72);
async function listServers() {
  const servers = await komodo.read("ListServers", {});
  if (servers.length === 0) {
    console.log("No servers found.");
    return;
  }
  const stats = await Promise.all(servers.map(async (s) => {
    if (s.info.state !== "Ok")
      return null;
    try {
      return await komodo.read("GetSystemStats", { server: s.name });
    } catch {
      return null;
    }
  }));
  console.log(`
Servers (${servers.length})
${SEP}`);
  for (let i = 0;i < servers.length; i++) {
    const s = servers[i];
    const st = stats[i];
    const stateLabel = s.info.state === "Ok" ? "\u25CF Ok" : s.info.state === "NotOk" ? "\u2716 NotOk" : "\u25CB Disabled";
    const region = s.info.region ? ` [${s.info.region}]` : "";
    const version = s.info.version ? `  periphery ${s.info.version}` : "";
    console.log(`${s.name}${region}`);
    console.log(`  ID      : ${s.id}`);
    console.log(`  State   : ${stateLabel}${version}`);
    console.log(`  Address : ${s.info.address}`);
    if (st) {
      const memPerc = (st.mem_used_gb / st.mem_total_gb * 100).toFixed(1);
      const diskSummary = st.disks.map((d) => {
        const perc = (d.used_gb / d.total_gb * 100).toFixed(1);
        return `${d.mount} ${d.used_gb.toFixed(1)}/${d.total_gb.toFixed(1)} GB (${perc}%)`;
      }).join("  |  ");
      console.log(`  CPU     : ${st.cpu_perc.toFixed(1)}%`);
      console.log(`  Memory  : ${st.mem_used_gb.toFixed(2)}/${st.mem_total_gb.toFixed(2)} GB (${memPerc}%)`);
      console.log(`  Disk    : ${diskSummary}`);
      if (st.load_average) {
        const la = st.load_average;
        console.log(`  Load    : ${la.one.toFixed(2)}  ${la.five.toFixed(2)}  ${la.fifteen.toFixed(2)}  (1m 5m 15m)`);
      }
    }
    console.log(SEP);
  }
}
async function listStacks() {
  const stacks = await komodo.read("ListStacks", {});
  if (stacks.length === 0) {
    console.log("No stacks found.");
    return;
  }
  console.log(`
Stacks (${stacks.length})
${SEP}`);
  for (const s of stacks) {
    const state = s.info.state;
    const stateLabel = state === "running" ? "\u25CF running" : state === "stopped" ? "\u25CB stopped" : state === "paused" ? "\u23F8 paused" : state === "deploying" ? "\u21BB deploying" : state === "dead" ? "\u2716 dead" : `  ${state}`;
    const source = s.info.repo ? `${s.info.git_provider}/${s.info.repo}@${s.info.branch}` : s.info.file_contents ? "inline file contents" : s.info.files_on_host ? "files on host" : "\u2014";
    const hashLine = s.info.deployed_hash && s.info.latest_hash ? `deployed=${s.info.deployed_hash}  latest=${s.info.latest_hash}` + (s.info.deployed_hash !== s.info.latest_hash ? "  \u26A0 update available" : "") : s.info.deployed_hash ? `deployed=${s.info.deployed_hash}` : null;
    const services = s.info.services.length ? s.info.services.map((sv) => `    \u2022 ${sv.service}  image=${sv.image}${sv.update_available ? " [update available]" : ""}`).join(`
`) : "    (no services)";
    console.log(`${s.name}`);
    console.log(`  ID      : ${s.id}`);
    console.log(`  State   : ${stateLabel}${s.info.status ? `  (${s.info.status})` : ""}`);
    console.log(`  Source  : ${source}`);
    if (hashLine)
      console.log(`  Commits : ${hashLine}`);
    if (s.info.missing_files.length)
      console.log(`  \u26A0 Missing files: ${s.info.missing_files.join(", ")}`);
    console.log(`  Services:`);
    console.log(services);
    console.log(SEP);
  }
}
async function listDeployments() {
  const deployments = await komodo.read("ListDeployments", {});
  if (deployments.length === 0) {
    console.log("No deployments found.");
    return;
  }
  console.log(`
Deployments (${deployments.length})
${SEP}`);
  for (const d of deployments) {
    const state = d.info.state;
    const stateLabel = state === "running" ? "\u25CF running" : state === "exited" ? "\u25CB exited" : state === "not_deployed" ? "\u25CB not deployed" : state === "restarting" ? "\u21BB restarting" : state === "paused" ? "\u23F8 paused" : state === "dead" ? "\u2716 dead" : `  ${state}`;
    console.log(`${d.name}`);
    console.log(`  ID      : ${d.id}`);
    console.log(`  State   : ${stateLabel}${d.info.status ? `  (${d.info.status})` : ""}`);
    console.log(`  Image   : ${d.info.image}${d.info.update_available ? "  \u26A0 image update available" : ""}`);
    if (d.info.build_id)
      console.log(`  Build   : ${d.info.build_id}`);
    console.log(SEP);
  }
}
async function listBuilds() {
  const builds = await komodo.read("ListBuilds", {});
  if (builds.length === 0) {
    console.log("No builds found.");
    return;
  }
  console.log(`
Builds (${builds.length})
${SEP}`);
  for (const b of builds) {
    const state = b.info.state;
    const stateLabel = state === "Ok" ? "\u25CF Ok" : state === "Failed" ? "\u2716 Failed" : state === "Building" ? "\u21BB Building" : `  ${state}`;
    const version = `${b.info.version.major}.${b.info.version.minor}.${b.info.version.patch}`;
    const lastBuilt = b.info.last_built_at ? new Date(b.info.last_built_at).toLocaleString() : "never";
    const source = b.info.repo ? `${b.info.git_provider}/${b.info.repo}@${b.info.branch}` : b.info.dockerfile_contents ? "inline dockerfile" : b.info.files_on_host ? "files on host" : "\u2014";
    const hashLine = b.info.built_hash && b.info.latest_hash ? `built=${b.info.built_hash}  latest=${b.info.latest_hash}` + (b.info.built_hash !== b.info.latest_hash ? "  \u26A0 new commits" : "") : b.info.built_hash ? `built=${b.info.built_hash}` : null;
    console.log(`${b.name}`);
    console.log(`  ID        : ${b.id}`);
    console.log(`  State     : ${stateLabel}`);
    console.log(`  Version   : ${version}`);
    console.log(`  Last built: ${lastBuilt}`);
    console.log(`  Source    : ${source}`);
    if (hashLine)
      console.log(`  Commits   : ${hashLine}`);
    if (b.info.image_registry_domain)
      console.log(`  Registry  : ${b.info.image_registry_domain}`);
    console.log(SEP);
  }
}
async function listRepos() {
  const repos = await komodo.read("ListRepos", {});
  if (repos.length === 0) {
    console.log("No repos found.");
    return;
  }
  console.log(`
Repos (${repos.length})
${SEP}`);
  for (const r of repos) {
    const state = r.info.state;
    const stateLabel = state === "Ok" ? "\u25CF Ok" : state === "Failed" ? "\u2716 Failed" : state === "Cloning" ? "\u21BB Cloning" : state === "Pulling" ? "\u21BB Pulling" : state === "Building" ? "\u21BB Building" : `  ${state}`;
    const lastPulled = r.info.last_pulled_at ? new Date(r.info.last_pulled_at).toLocaleString() : "never";
    const lastBuilt = r.info.last_built_at ? new Date(r.info.last_built_at).toLocaleString() : "never";
    const hashLine = [
      r.info.cloned_hash ? `cloned=${r.info.cloned_hash}` : null,
      r.info.built_hash ? `built=${r.info.built_hash}` : null,
      r.info.latest_hash ? `latest=${r.info.latest_hash}` : null
    ].filter(Boolean).join("  ");
    console.log(`${r.name}`);
    console.log(`  ID         : ${r.id}`);
    console.log(`  State      : ${stateLabel}`);
    console.log(`  Source     : ${r.info.git_provider}/${r.info.repo}@${r.info.branch}`);
    console.log(`  Last pulled: ${lastPulled}`);
    console.log(`  Last built : ${lastBuilt}`);
    if (hashLine)
      console.log(`  Commits    : ${hashLine}`);
    if (r.info.cloned_message)
      console.log(`  Message    : ${r.info.cloned_message}`);
    console.log(SEP);
  }
}
async function listProcedures() {
  const procedures = await komodo.read("ListProcedures", {});
  if (procedures.length === 0) {
    console.log("No procedures found.");
    return;
  }
  console.log(`
Procedures (${procedures.length})
${SEP}`);
  for (const p of procedures) {
    const state = p.info.state;
    const stateLabel = state === "Ok" ? "\u25CF Ok" : state === "Failed" ? "\u2716 Failed" : state === "Running" ? "\u21BB Running" : `  ${state}`;
    const lastRun = p.info.last_run_at ? new Date(p.info.last_run_at).toLocaleString() : "never";
    const nextRun = p.info.next_scheduled_run ? new Date(p.info.next_scheduled_run).toLocaleString() : null;
    console.log(`${p.name}`);
    console.log(`  ID      : ${p.id}`);
    console.log(`  State   : ${stateLabel}`);
    console.log(`  Stages  : ${p.info.stages}`);
    console.log(`  Last run: ${lastRun}`);
    if (nextRun)
      console.log(`  Next run: ${nextRun}`);
    if (p.info.schedule_error)
      console.log(`  \u26A0 Schedule error: ${p.info.schedule_error}`);
    console.log(SEP);
  }
}
async function listActions() {
  const actions = await komodo.read("ListActions", {});
  if (actions.length === 0) {
    console.log("No actions found.");
    return;
  }
  console.log(`
Actions (${actions.length})
${SEP}`);
  for (const a of actions) {
    const state = a.info.state;
    const stateLabel = state === "Ok" ? "\u25CF Ok" : state === "Failed" ? "\u2716 Failed" : state === "Running" ? "\u21BB Running" : `  ${state}`;
    const lastRun = a.info.last_run_at ? new Date(a.info.last_run_at).toLocaleString() : "never";
    const nextRun = a.info.next_scheduled_run ? new Date(a.info.next_scheduled_run).toLocaleString() : null;
    console.log(`${a.name}`);
    console.log(`  ID      : ${a.id}`);
    console.log(`  State   : ${stateLabel}`);
    console.log(`  Last run: ${lastRun}`);
    if (nextRun)
      console.log(`  Next run: ${nextRun}`);
    if (a.info.schedule_error)
      console.log(`  \u26A0 Schedule error: ${a.info.schedule_error}`);
    console.log(SEP);
  }
}
switch (type) {
  case "servers":
    await listServers();
    break;
  case "stacks":
    await listStacks();
    break;
  case "deployments":
    await listDeployments();
    break;
  case "builds":
    await listBuilds();
    break;
  case "repos":
    await listRepos();
    break;
  case "procedures":
    await listProcedures();
    break;
  case "actions":
    await listActions();
    break;
}
