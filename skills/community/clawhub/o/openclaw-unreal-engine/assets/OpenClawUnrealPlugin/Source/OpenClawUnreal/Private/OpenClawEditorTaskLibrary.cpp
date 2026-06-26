#include "OpenClawEditorTaskLibrary.h"

FString UOpenClawEditorTaskLibrary::BuildRemoteControlCallEnvelope(const FString& RequestId, const FString& ObjectPath, const FString& FunctionName, const FString& ParametersJson)
{
    return FString::Printf(
        TEXT("{\"id\":\"%s\",\"type\":\"editor.remote_control.call\",\"task\":\"%s\",\"payload\":{\"objectPath\":\"%s\",\"parameters\":%s}}"),
        *RequestId,
        *FunctionName,
        *ObjectPath,
        ParametersJson.IsEmpty() ? TEXT("{}") : *ParametersJson);
}

FString UOpenClawEditorTaskLibrary::BuildRemoteControlSetPropertyEnvelope(const FString& RequestId, const FString& ObjectPath, const FString& PropertyName, const FString& PropertyValueJson)
{
    return FString::Printf(
        TEXT("{\"id\":\"%s\",\"type\":\"editor.remote_control.set_property\",\"task\":\"%s\",\"payload\":{\"objectPath\":\"%s\",\"value\":%s}}"),
        *RequestId,
        *PropertyName,
        *ObjectPath,
        PropertyValueJson.IsEmpty() ? TEXT("null") : *PropertyValueJson);
}
