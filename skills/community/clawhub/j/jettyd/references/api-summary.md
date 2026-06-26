# jettyd API Reference

Base URL: `https://api.jettyd.com/v1`  
Auth: `Authorization: Bearer <api_key>`

## Devices

| Method | Path | Description |
|--------|------|-------------|
| GET | `/devices` | List all devices |
| GET | `/devices/:id` | Device detail |
| GET | `/devices/:id/shadow` | Latest sensor readings |
| GET | `/devices/:id/telemetry?metric=&from=&limit=` | Historical telemetry |
| POST | `/devices/:id/commands` | Send command `{action, params}` |
| PUT | `/devices/:id/config` | Push JettyScript rules config |
| GET | `/devices/:id/commands` | List recent commands |

## Device Types & Fleet

| Method | Path | Description |
|--------|------|-------------|
| GET | `/device-types` | List device types |
| POST | `/device-types` | Create device type |
| GET | `/fleet-tokens` | List fleet tokens |
| POST | `/fleet-tokens` | Create fleet token |

## Webhooks

| Method | Path | Description |
|--------|------|-------------|
| GET | `/webhooks` | List webhooks |
| POST | `/webhooks` | Create webhook `{name, url, events, secret}` |
| PUT | `/webhooks/:id` | Update webhook |
| DELETE | `/webhooks/:id` | Delete webhook |
| POST | `/webhooks/:id/test` | Send test event |

## Command actions (built-in)

| Action | Params | Description |
|--------|--------|-------------|
| `relay.on` | `{duration?: ms}` | Turn relay on |
| `relay.off` | — | Turn relay off |
| `led.on` | — | Turn LED on |
| `led.off` | — | Turn LED off |
| `led.blink` | `{count, interval_ms}` | Blink LED |
| `led.toggle` | — | Toggle LED |

## Webhook event types

`device.online` `device.offline` `device.alert.info` `device.alert.warning` `device.alert.critical` `device.config_loaded` `device.config_rejected` `command.sent` `command.acked` `command.failed` `telemetry.received`
