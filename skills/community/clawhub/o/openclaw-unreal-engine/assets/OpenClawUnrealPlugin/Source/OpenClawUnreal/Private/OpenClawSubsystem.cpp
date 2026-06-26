#include "OpenClawSubsystem.h"

#include "HttpModule.h"
#include "Interfaces/IHttpRequest.h"
#include "Interfaces/IHttpResponse.h"
#include "Serialization/JsonSerializer.h"
#include "Serialization/JsonWriter.h"

void UOpenClawSubsystem::Configure(const FString& InBaseUrl, const FString& InApiKey)
{
    BaseUrl = InBaseUrl;
    ApiKey = InApiKey;
}

bool UOpenClawSubsystem::Connect()
{
    if (BaseUrl.IsEmpty())
    {
        BroadcastHttpError(TEXT("Connect"), TEXT("Base URL is empty."));
        return false;
    }

    bConnected = true;
    OnConnected.Broadcast();
    return true;
}

void UOpenClawSubsystem::Disconnect()
{
    if (bConnected)
    {
        bConnected = false;
        OnDisconnected.Broadcast(TEXT("Disconnected by caller."));
    }
}

void UOpenClawSubsystem::SendTaskJson(const FString& RequestId, const FString& TaskJson)
{
    if (!bConnected)
    {
        BroadcastHttpError(TEXT("SendTaskJson"), TEXT("Not connected."));
        return;
    }

    if (BaseUrl.IsEmpty())
    {
        BroadcastHttpError(TEXT("SendTaskJson"), TEXT("Base URL is empty."));
        return;
    }

    const FString Url = BaseUrl.EndsWith(TEXT("/")) ? BaseUrl + TEXT("api/unreal/task") : BaseUrl + TEXT("/api/unreal/task");

    TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = FHttpModule::Get().CreateRequest();
    Request->SetURL(Url);
    Request->SetVerb(TEXT("POST"));
    Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));

    if (!ApiKey.IsEmpty())
    {
        Request->SetHeader(TEXT("Authorization"), FString::Printf(TEXT("Bearer %s"), *ApiKey));
    }

    Request->SetContentAsString(TaskJson);

    Request->OnProcessRequestComplete().BindLambda(
        [this, RequestId](FHttpRequestPtr HttpRequest, FHttpResponsePtr HttpResponse, bool bSucceeded)
        {
            if (!bSucceeded || !HttpResponse.IsValid())
            {
                BroadcastHttpError(TEXT("SendTaskJson"), TEXT("HTTP request failed."));
                return;
            }

            const int32 Code = HttpResponse->GetResponseCode();
            const FString Body = HttpResponse->GetContentAsString();

            if (Code >= 200 && Code < 300)
            {
                OnTaskResult.Broadcast(RequestId, Body);
            }
            else
            {
                BroadcastHttpError(TEXT("SendTaskJson"), FString::Printf(TEXT("HTTP %d: %s"), Code, *Body));
            }
        });

    Request->ProcessRequest();
}

void UOpenClawSubsystem::SendTaskRequest(const FOpenClawTaskRequest& Request)
{
    FString Payload = Request.PayloadJson.IsEmpty() ? TEXT("{}") : Request.PayloadJson;
    FString Envelope = FString::Printf(
        TEXT("{\"id\":\"%s\",\"type\":\"%s\",\"task\":\"%s\",\"payload\":%s}"),
        *Request.RequestId,
        *Request.Type,
        *Request.Task,
        *Payload);

    SendTaskJson(Request.RequestId, Envelope);
}

void UOpenClawSubsystem::SendPing()
{
    FOpenClawTaskRequest Request;
    Request.RequestId = TEXT("ping");
    Request.Type = TEXT("runtime.query.status");
    Request.Task = TEXT("ping");
    Request.PayloadJson = TEXT("{}");
    SendTaskRequest(Request);
}

bool UOpenClawSubsystem::IsConfigured() const
{
    return !BaseUrl.IsEmpty();
}

bool UOpenClawSubsystem::IsConnected() const
{
    return bConnected;
}

FString UOpenClawSubsystem::GetBaseUrl() const
{
    return BaseUrl;
}

EOpenClawConnectionStatus UOpenClawSubsystem::GetConnectionStatus() const
{
    if (bConnected)
    {
        return EOpenClawConnectionStatus::Connected;
    }

    if (!BaseUrl.IsEmpty())
    {
        return EOpenClawConnectionStatus::Configured;
    }

    return EOpenClawConnectionStatus::Disconnected;
}

void UOpenClawSubsystem::BroadcastHttpError(const FString& Context, const FString& Details)
{
    OnError.Broadcast(Context + TEXT(": ") + Details);
}
