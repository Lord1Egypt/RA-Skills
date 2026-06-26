# Google Voice HAR notes

Source used: ~/Downloads/har/voice.google.com.har.

Important: never copy HAR cookies, authorization headers, message bodies, recipient numbers, or anti-abuse tokens into prompts or committed files. Re-inspect HAR locally if endpoint details need updating.

## Observed host and headers

Google Voice web client calls https://clients6.google.com/voice/v1/voiceclient/... with alt=protojson and a Google web API key.

Common headers observed:
- content-type: application/json+protobuf
- x-client-version: 906554935
- x-goog-authuser: 0
- x-goog-encode-response-if-executable: base64
- origin: https://clients6.google.com
- referer: https://clients6.google.com/static/proxy.html?usegapi=1

Responses can be plain JSON/protobuf arrays or base64-encoded JSON arrays. Decode base64 when the response body does not start with [ or {.

## Endpoints observed

- POST /voice/v1/voiceclient/api2thread/list
  - body observed: [1,20,15,null,null,[null,1,1,1]]
- POST /voice/v1/voiceclient/api2thread/get
  - body observed: ["t.<id>",100,"<context>",[null,1,1]]
  - third field may be a phone/thread context. Null may work in some sessions, but use raw call if not.
- POST /voice/v1/voiceclient/api2thread/sendsms
  - body observed shape: [null,null,null,null,"<message>","<thread/group>",null,null,["<recipient>"],null,["<token>"]]
  - send likely depends on browser/session anti-abuse context. Treat as experimental and only use after explicit approval.
- Other observed endpoints: threadinginfo/get, thread/batchupdateattributes, thread/batchdelete, thread/markallread.

## MCP auth modes

The bundled MCP server supports browser mode by default through CDP at GV_CDP_URL or http://127.0.0.1:19222. It evaluates fetch inside an existing Google Voice browser tab so cookies stay in-browser.

GWS mode is available with GV_AUTH_MODE=gws. It runs gws auth export locally, refreshes the OAuth token, and sends Authorization: Bearer. This may not satisfy the private Google Voice web endpoint because the HAR did not use bearer auth. Header mode is also available with GV_COOKIE or GV_AUTHORIZATION. Avoid header mode unless necessary because it puts credentials in the process environment.
