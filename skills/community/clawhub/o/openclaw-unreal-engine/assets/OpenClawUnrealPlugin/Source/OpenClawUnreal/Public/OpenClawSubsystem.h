#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "OpenClawTypes.h"
#include "OpenClawSubsystem.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOpenClawConnected);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOpenClawDisconnected, const FString&, Reason);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOpenClawTaskResult, const FString&, RequestId, const FString&, ResponseJson);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOpenClawError, const FString&, ErrorMessage);

UCLASS(BlueprintType)
class OPENCLAWUNREAL_API UOpenClawSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    UPROPERTY(BlueprintAssignable, Category = "OpenClaw")
    FOpenClawConnected OnConnected;

    UPROPERTY(BlueprintAssignable, Category = "OpenClaw")
    FOpenClawDisconnected OnDisconnected;

    UPROPERTY(BlueprintAssignable, Category = "OpenClaw")
    FOpenClawTaskResult OnTaskResult;

    UPROPERTY(BlueprintAssignable, Category = "OpenClaw")
    FOpenClawError OnError;

    UFUNCTION(BlueprintCallable, Category = "OpenClaw")
    void Configure(const FString& InBaseUrl, const FString& InApiKey);

    UFUNCTION(BlueprintCallable, Category = "OpenClaw")
    bool Connect();

    UFUNCTION(BlueprintCallable, Category = "OpenClaw")
    void Disconnect();

    UFUNCTION(BlueprintCallable, Category = "OpenClaw")
    void SendTaskJson(const FString& RequestId, const FString& TaskJson);

    UFUNCTION(BlueprintCallable, Category = "OpenClaw")
    void SendTaskRequest(const FOpenClawTaskRequest& Request);

    UFUNCTION(BlueprintCallable, Category = "OpenClaw")
    void SendPing();

    UFUNCTION(BlueprintPure, Category = "OpenClaw")
    bool IsConfigured() const;

    UFUNCTION(BlueprintPure, Category = "OpenClaw")
    bool IsConnected() const;

    UFUNCTION(BlueprintPure, Category = "OpenClaw")
    FString GetBaseUrl() const;

    UFUNCTION(BlueprintPure, Category = "OpenClaw")
    EOpenClawConnectionStatus GetConnectionStatus() const;

private:
    FString BaseUrl;
    FString ApiKey;
    bool bConnected = false;

    void BroadcastHttpError(const FString& Context, const FString& Details);
};
