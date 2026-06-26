import { describe, expect, it } from "vitest";

import { shouldProcessAgentInboundMessage, shouldSuppressAgentReplyText } from "./handler.js";

describe("shouldProcessAgentInboundMessage", () => {
    it("allows enter_agent/subscribe through the filter (handled earlier by static welcome)", () => {
        const enterAgent = shouldProcessAgentInboundMessage({
            msgType: "event",
            eventType: "enter_agent",
            fromUser: "zhangsan",
        });
        expect(enterAgent.shouldProcess).toBe(true);
        expect(enterAgent.reason).toBe("allowed_event:enter_agent");

        const subscribe = shouldProcessAgentInboundMessage({
            msgType: "event",
            eventType: "subscribe",
            fromUser: "lisi",
        });
        expect(subscribe.shouldProcess).toBe(true);
        expect(subscribe.reason).toBe("allowed_event:subscribe");
    });

    it("skips unknown event callbacks so they do not create sessions", () => {
        const unknown = shouldProcessAgentInboundMessage({
            msgType: "event",
            eventType: "some_random_event",
            fromUser: "zhangsan",
        });
        expect(unknown.shouldProcess).toBe(false);
        expect(unknown.reason).toBe("event:some_random_event");
    });

    it("skips system sender callbacks", () => {
        const systemSender = shouldProcessAgentInboundMessage({
            msgType: "text",
            fromUser: "sys",
        });
        expect(systemSender.shouldProcess).toBe(false);
        expect(systemSender.reason).toBe("system_sender");
    });

    it("skips messages with missing sender id", () => {
        const missingSender = shouldProcessAgentInboundMessage({
            msgType: "text",
            fromUser: "   ",
        });
        expect(missingSender.shouldProcess).toBe(false);
        expect(missingSender.reason).toBe("missing_sender");
    });


    it("allows group chat messages when sender id is missing", () => {
        const groupWithoutSender = shouldProcessAgentInboundMessage({
            msgType: "file",
            fromUser: "   ",
            chatId: "wrbchat_123",
        });
        expect(groupWithoutSender.shouldProcess).toBe(true);
        expect(groupWithoutSender.reason).toBe("missing_sender_but_group_chat");
    });

    it("allows normal user text message processing", () => {
        const normalMessage = shouldProcessAgentInboundMessage({
            msgType: "text",
            fromUser: "wangwu",
        });
        expect(normalMessage.shouldProcess).toBe(true);
        expect(normalMessage.reason).toBe("user_message");
    });
});

describe("shouldSuppressAgentReplyText", () => {
    it("keeps plain text replies when no media reply has been seen", () => {
        expect(
            shouldSuppressAgentReplyText({
                text: "这里是正常文本",
                mediaReplySeen: false,
            }),
        ).toBe(false);
    });

    it("suppresses companion text once the reply flow includes media", () => {
        expect(
            shouldSuppressAgentReplyText({
                text: "文件已发送，请查收",
                mediaReplySeen: true,
            }),
        ).toBe(true);
    });

    it("does not suppress empty text even after media replies", () => {
        expect(
            shouldSuppressAgentReplyText({
                text: "   ",
                mediaReplySeen: true,
            }),
        ).toBe(false);
    });
});
