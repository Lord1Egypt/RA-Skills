# Invoice Verification Service

ClawHub skill for the `invoice-api-service` v4 plugin APIs.

## What This Skill Does

- Initialize or rotate an `appKey` with `POST /api/v4/plugin/key/init`
- Query recharge package options with `GET /api/v4/plugin/packages`
- Query remaining quota with `GET /api/v4/plugin/quota`
- Query quota ledger with `GET /api/v4/plugin/ledger`
- Verify invoice text with `POST /api/v4/plugin/verify`
- Verify invoice images with `POST /api/v4/plugin/verify`
- Verify all invoice images in a local directory and save JSON result files next to the source directory
- Create recharge orders with `POST /api/v4/plugin/orders`
- Query recharge order status with `GET /api/v4/plugin/orders/{orderNo}`

## Runtime Requirements

- Node.js 18 or newer
- Reachable backend base URL, for example `http://192.168.154.76:18888`

## Bundled Files

- `SKILL.md`: trigger instructions and execution workflow
- `agents/openai.yaml`: ClawHub/OpenClaw UI metadata
- `scripts/invoice_service.js`: executable helper script

## Local Usage

```bash
node "{baseDir}/scripts/invoice_service.js" config set --api-base-url http://192.168.154.76:18888
node "{baseDir}/scripts/invoice_service.js" init-key
node "{baseDir}/scripts/invoice_service.js" packages
node "{baseDir}/scripts/invoice_service.js" quota
node "{baseDir}/scripts/invoice_service.js" ledger --page 1 --page-size 20
node "{baseDir}/scripts/invoice_service.js" verify --text "发票代码 033002100611, 发票号码 12345678, 开票日期 2025-05-30, 金额 260.65, 校验码 123456" --format both
node "{baseDir}/scripts/invoice_service.js" verify-image --image-file C:\path\invoice.png --format both
node "{baseDir}/scripts/invoice_service.js" verify-directory --dir C:\path\invoice-images --format json
node "{baseDir}/scripts/invoice_service.js" create-order --amount 10
node "{baseDir}/scripts/invoice_service.js" query-order --order-no ORDER123456789
```

Install the skill first, then run `init-key` once before the first real use.
`init-key` calls the backend to create and persist the `appKey`, and the backend grants the free 5-trial quota at the same time.

## Publish To ClawHub

The current `clawhub` CLI publishes a skill folder directly. `SKILL.md` is mandatory; `README.md` is recommended.

```bash
clawhub login
clawhub publish . --slug invoice-verification-service --name "Invoice Verification Service" --version 0.3.0 --changelog "Add image verify and recharge order flows for invoice-api-service v4 plugin APIs."
```

## Install From ClawHub

After the skill is published publicly:

```bash
clawhub install invoice-verification-service
node "{installDir}/scripts/invoice_service.js" init-key
```

If a specific version is needed:

```bash
clawhub install invoice-verification-service --version 0.3.0
```

## Notes

- The script stores config in `~/.openclaw/invoice-skill/config.json`.
- The script also reads the legacy plugin config from `~/.openclaw/invoice-plugin/config.json` if present.
- `verify-image` can be called with image data only. `--text` is optional and is used only to supplement extracted invoice fields.
- `verify-directory` scans `.png`, `.jpg`, and `.jpeg` files in a directory. If exactly one image is found, it writes one `*.verify.json` file in the source directory. If multiple images are found, it creates an `invoice-verify-results-<timestamp>` folder under the source directory and writes one JSON per image plus `summary.json`.
- `verify-directory` reads a same-name sidecar text file by default when present, for example `invoice01.png` + `invoice01.txt`.
- When the backend reports `remainingQuota <= 3`, plugin responses may include `rechargePackages` so the caller can show package options directly in chat.
- After `create-order`, prefer `paymentPageUrl` as the payment entry. It points to the cashier page where the user can choose WeChat or Alipay. `qrCodeImageUrl` is only the QR image link.
- Payment callback handling stays on the backend internal endpoint `/api/v4/internal/payment/callback`; this skill only needs order creation and order status querying.
