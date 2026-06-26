#pragma once

#include "CoreMinimal.h"

class IWebSocket;

class OPENCLAWUNREAL_API FOpenClawWebSocketClient
{
public:
    FOpenClawWebSocketClient();
    ~FOpenClawWebSocketClient();

    bool Connect(const FString& InUrl, const FString& InAuthToken);
    void Disconnect();
    bool Send(const FString& Message);
    bool IsConnected() const;

    TFunction<void()> OnConnected;
    TFunction<void(const FString&)> OnConnectionError;
    TFunction<void(const FString&)> OnMessage;
    TFunction<void(const FString&)> OnClosed;

private:
    TSharedPtr<IWebSocket> Socket;
    FString Url;
};
