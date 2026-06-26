# Google Voice call HAR notes

Source HAR: `/home/umbrel/Downloads/har/call_voice.google.com.har`.

Sanitized summary:

- The capture does **not** show a stable `/voiceclient/.../call` placement endpoint.
- It mostly contains existing SMS/thread endpoints plus contact autocomplete, recaptcha, telemetry, and UI audio assets:
  - `POST /voice/v1/voiceclient/api2thread/list`
  - `POST /voice/v1/voiceclient/api2thread/get`
  - `POST /voice/v1/voiceclient/api2thread/search`
  - `POST /voice/v1/voiceclient/threadinginfo/get`
  - `POST /voice/v1/voiceclient/thread/batchupdateattributes`
  - `POST /voice/v1/voiceclient/thread/markallread`
  - `POST /$rpc/peoplestack.PeopleStackAutocompleteService/Autocomplete|Lookup|Warmup`
  - recaptcha enterprise reload/clr calls
  - call UI audio assets like ringing/busy/call ended tones

Conclusion: call placement is better handled by browser UI automation against the logged-in Google Voice web session unless a future HAR captures a clear call placement RPC/WebRTC signaling endpoint. Do not commit HAR payloads, cookies, recaptcha tokens, phone numbers, or auth headers.
