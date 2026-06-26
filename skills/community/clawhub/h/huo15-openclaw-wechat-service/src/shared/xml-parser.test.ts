import { describe, expect, it } from "vitest";
import { buildPassiveReplyXml, extractEncryptField, parseInboundMessage } from "./xml-parser.js";

const SAMPLE_TEXT_XML = `
<xml>
  <ToUserName><![CDATA[gh_abc]]></ToUserName>
  <FromUserName><![CDATA[oUserOpenId]]></FromUserName>
  <CreateTime>1735000000</CreateTime>
  <MsgType><![CDATA[text]]></MsgType>
  <Content><![CDATA[你好]]></Content>
  <MsgId>123456789</MsgId>
</xml>`.trim();

const SAMPLE_EVENT_XML = `
<xml>
  <ToUserName><![CDATA[gh_abc]]></ToUserName>
  <FromUserName><![CDATA[oUserOpenId]]></FromUserName>
  <CreateTime>1735000000</CreateTime>
  <MsgType><![CDATA[event]]></MsgType>
  <Event><![CDATA[subscribe]]></Event>
  <EventKey><![CDATA[qrscene_1]]></EventKey>
  <Ticket><![CDATA[TICKET]]></Ticket>
</xml>`.trim();

describe("parseInboundMessage", () => {
  it("parses a text message", () => {
    const msg = parseInboundMessage(SAMPLE_TEXT_XML);
    expect(msg.msgType).toBe("text");
    expect(msg.content).toBe("你好");
    expect(msg.fromUserName).toBe("oUserOpenId");
    expect(msg.msgId).toBe("123456789");
  });
  it("parses an event message with EventKey/Ticket", () => {
    const msg = parseInboundMessage(SAMPLE_EVENT_XML);
    expect(msg.msgType).toBe("event");
    expect(msg.event).toBe("subscribe");
    expect(msg.eventKey).toBe("qrscene_1");
    expect(msg.ticket).toBe("TICKET");
  });
  it("treats unknown MsgType as 'unknown'", () => {
    const xml = `<xml><ToUserName>a</ToUserName><FromUserName>b</FromUserName><CreateTime>1</CreateTime><MsgType>weirdtype</MsgType></xml>`;
    expect(parseInboundMessage(xml).msgType).toBe("unknown");
  });
});

describe("extractEncryptField", () => {
  it("returns the Encrypt field from wrapped envelope", () => {
    const xml = `<xml><ToUserName><![CDATA[x]]></ToUserName><Encrypt><![CDATA[CIPHER_VALUE]]></Encrypt></xml>`;
    expect(extractEncryptField(xml)).toBe("CIPHER_VALUE");
  });
  it("throws when Encrypt missing", () => {
    expect(() => extractEncryptField("<xml><ToUserName>x</ToUserName></xml>")).toThrow();
  });
});

describe("buildPassiveReplyXml", () => {
  it("builds a text passive reply", () => {
    const out = buildPassiveReplyXml({
      toUser: "openid",
      fromUser: "gh_abc",
      reply: { type: "text", content: "你好&<>" },
      createTime: 1,
    });
    expect(out).toContain("<MsgType><![CDATA[text]]></MsgType>");
    expect(out).toContain("<Content><![CDATA[你好&<>]]></Content>");
    expect(out).toContain("<ToUserName><![CDATA[openid]]></ToUserName>");
  });
  it("builds a news passive reply with multiple articles", () => {
    const out = buildPassiveReplyXml({
      toUser: "openid",
      fromUser: "gh_abc",
      reply: {
        type: "news",
        articles: [
          { title: "t1", url: "http://x" },
          { title: "t2", description: "d", picUrl: "http://y" },
        ],
      },
    });
    expect(out).toContain("<ArticleCount>2</ArticleCount>");
    expect(out).toContain("<Title><![CDATA[t1]]></Title>");
    expect(out).toContain("<Title><![CDATA[t2]]></Title>");
  });
  it("builds transfer_customer_service with kfAccount", () => {
    const out = buildPassiveReplyXml({
      toUser: "openid",
      fromUser: "gh_abc",
      reply: { type: "transfer_customer_service", kfAccount: "kf@gh_abc" },
    });
    expect(out).toContain("<MsgType><![CDATA[transfer_customer_service]]></MsgType>");
    expect(out).toContain("<KfAccount><![CDATA[kf@gh_abc]]></KfAccount>");
  });
});
