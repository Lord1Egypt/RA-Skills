# HiLink API Reference

## Authentication

Every API call needs a session/CSRF token pair from `GET /api/webserver/SesTokInfo`.

```xml
<response>
  <SesInfo>SessionID=xxx</SesInfo>
  <TokInfo>csrf_token_value</TokInfo>
</response>
```

Use as headers:
- `Cookie: <SesInfo value>`
- `__RequestVerificationToken: <TokInfo value>`

**Important:** Tokens are single-use for POST requests. Get fresh tokens before each write operation.

## Endpoints

### Device Info
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/device/information` | Device model, serial, IMEI |
| GET | `/api/device/signal` | Signal strength (RSRP, RSSI, SINR, band) |
| GET | `/api/monitoring/status` | Network status, SIM state, unread SMS count |
| GET | `/api/net/current-plmn` | Current carrier name and MCC/MNC |

### SMS
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/sms/send-sms` | Send SMS |
| POST | `/api/sms/sms-list` | List SMS (inbox/outbox) |
| POST | `/api/sms/delete-sms` | Delete SMS by index |
| POST | `/api/sms/sms-count` | Count SMS per box |

#### Send SMS
```xml
<request>
  <Index>-1</Index>
  <Phones><Phone>+41791234567</Phone></Phones>
  <Sca></Sca>
  <Content>Message text</Content>
  <Length>12</Length>
  <Reserved>1</Reserved>
  <Date>2026-03-08 02:00:00</Date>
  <SendType>0</SendType>
</request>
```

#### List SMS
```xml
<request>
  <PageIndex>1</PageIndex>
  <ReadCount>20</ReadCount>
  <BoxType>1</BoxType>        <!-- 1=inbox, 2=outbox -->
  <SortType>0</SortType>
  <Ascending>0</Ascending>
  <UnreadPreferred>1</UnreadPreferred>
</request>
```

#### Delete SMS
```xml
<request><Index>40001</Index></request>
```

### SIM PIN
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/pin/status` | PIN state (SimState, attempts remaining) |
| POST | `/api/pin/operate` | Enter/change/enable/disable PIN |

#### PIN Operations
```xml
<!-- OperateType: 0=enter, 1=enable, 2=disable, 3=change -->
<request>
  <OperateType>0</OperateType>
  <CurrentPin>1234</CurrentPin>
  <NewPin></NewPin>
  <PukCode></PukCode>
</request>
```

#### SimState Values
| Value | Meaning |
|-------|---------|
| 255 | No SIM |
| 256 | PIN locked |
| 257 | PIN verified (or auto-entered) |
| 258 | PUK required |
| 260 | PIN required |

### USSD (Balance etc.)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ussd/send` | Send USSD code |
| GET | `/api/ussd/get` | Get USSD response |

```xml
<!-- Send USSD -->
<request>
  <content>*#100#</content>
  <codeType>CodeType</codeType>
  <timeout></timeout>
</request>
```

### DHCP Settings
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dhcp/settings` | Get DHCP/gateway settings |
| POST | `/api/dhcp/settings` | Change gateway IP |

### Signal Response Fields
```xml
<response>
  <rssi>-61dBm</rssi>     <!-- Received Signal Strength -->
  <rsrp>-89dBm</rsrp>     <!-- Reference Signal Received Power -->
  <sinr>20dB</sinr>       <!-- Signal to Interference+Noise Ratio -->
  <band>B7</band>         <!-- LTE Band -->
</response>
```

## Error Codes
| Code | Meaning |
|------|---------|
| 100002 | System busy |
| 100003 | Invalid token |
| 100006 | Parameter error |
| 108001 | Invalid username |
| 108002 | Invalid password |
| 108003 | Already logged in |
| 113018 | SMS send failed (no network/balance) |
| 113055 | SMS storage full |
