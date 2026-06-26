# API Pricing Reference

> Auto-generated on 2026-04-21 08:25 UTC.
> Sources: LiteLLM (direct-provider pricing) + OpenRouter (aggregator routing).
> Regenerate with: `python3 scripts/refresh_pricing.py`
> Total models: 2628 (2315 via LiteLLM, 313 via OpenRouter)

All prices are USD per 1,000,000 units of the section's billing unit.
So `$3.00` under `per 1M tokens` = $0.000003/token; `$40,000` under
`per 1M images` = $0.04/image.

## AI21 — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| jamba-1.5 | $0.2000 | $0.4000 |
| jamba-1.5-large | $2.0000 | $8.0000 |
| jamba-1.5-large@001 | $2.0000 | $8.0000 |
| jamba-1.5-mini | $0.2000 | $0.4000 |
| jamba-1.5-mini@001 | $0.2000 | $0.4000 |
| jamba-large-1.6 | $2.0000 | $8.0000 |
| jamba-large-1.7 | $2.0000 | $8.0000 |
| jamba-mini-1.6 | $0.2000 | $0.4000 |
| jamba-mini-1.7 | $0.2000 | $0.4000 |

## AI21 — completion (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| j2-light | $3.0000 | $3.0000 |
| j2-mid | $10.0000 | $10.0000 |
| j2-ultra | $15.0000 | $15.0000 |

## AWS Bedrock — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| ai21.j2-mid-v1 | $12.5000 | $12.5000 |
| ai21.j2-ultra-v1 | $18.8000 | $18.8000 |
| ai21.jamba-1-5-large-v1:0 | $2.0000 | $8.0000 |
| ai21.jamba-1-5-mini-v1:0 | $0.2000 | $0.4000 |
| ai21.jamba-instruct-v1:0 | $0.5000 | $0.7000 |
| amazon.nova-2-lite-v1:0 | $0.3000 | $2.5000 |
| amazon.nova-2-pro-preview-20251202-v1:0 | $2.1875 | $17.5000 |
| amazon.nova-lite-v1:0 | $0.0600 | $0.2400 |
| amazon.nova-micro-v1:0 | $0.0350 | $0.1400 |
| amazon.nova-pro-v1:0 | $0.8000 | $3.2000 |
| amazon.titan-text-express-v1 | $1.3000 | $1.7000 |
| amazon.titan-text-lite-v1 | $0.3000 | $0.4000 |
| amazon.titan-text-premier-v1:0 | $0.5000 | $1.5000 |
| anthropic.claude-3-5-haiku-20241022-v1:0 | $0.8000 | $4.0000 |
| anthropic.claude-3-5-sonnet-20240620-v1:0 | $3.0000 | $15.0000 |
| anthropic.claude-3-5-sonnet-20241022-v2:0 | $3.0000 | $15.0000 |
| anthropic.claude-3-7-sonnet-20240620-v1:0 | $3.6000 | $18.0000 |
| anthropic.claude-3-7-sonnet-20250219-v1:0 | $3.0000 | $15.0000 |
| anthropic.claude-3-haiku-20240307-v1:0 | $0.2500 | $1.2500 |
| anthropic.claude-3-opus-20240229-v1:0 | $15.0000 | $75.0000 |
| anthropic.claude-3-sonnet-20240229-v1:0 | $3.0000 | $15.0000 |
| anthropic.claude-haiku-4-5-20251001-v1:0 | $1.0000 | $5.0000 |
| anthropic.claude-haiku-4-5@20251001 | $1.0000 | $5.0000 |
| anthropic.claude-instant-v1 | $0.8000 | $2.4000 |
| anthropic.claude-opus-4-1-20250805-v1:0 | $15.0000 | $75.0000 |
| anthropic.claude-opus-4-20250514-v1:0 | $15.0000 | $75.0000 |
| anthropic.claude-opus-4-5-20251101-v1:0 | $5.0000 | $25.0000 |
| anthropic.claude-opus-4-6-v1 | $5.0000 | $25.0000 |
| anthropic.claude-opus-4-7 | $5.0000 | $25.0000 |
| anthropic.claude-sonnet-4-20250514-v1:0 | $3.0000 | $15.0000 |
| anthropic.claude-sonnet-4-5-20250929-v1:0 | $3.0000 | $15.0000 |
| anthropic.claude-sonnet-4-6 | $3.0000 | $15.0000 |
| anthropic.claude-v1 | $8.0000 | $24.0000 |
| anthropic.claude-v2:1 | $8.0000 | $24.0000 |
| apac.amazon.nova-2-lite-v1:0 | $0.3300 | $2.7500 |
| apac.amazon.nova-2-pro-preview-20251202-v1:0 | $2.1875 | $17.5000 |
| apac.amazon.nova-lite-v1:0 | $0.0630 | $0.2520 |
| apac.amazon.nova-micro-v1:0 | $0.0370 | $0.1480 |
| apac.amazon.nova-pro-v1:0 | $0.8400 | $3.3600 |
| apac.anthropic.claude-3-5-sonnet-20240620-v1:0 | $3.0000 | $15.0000 |
| apac.anthropic.claude-3-5-sonnet-20241022-v2:0 | $3.0000 | $15.0000 |
| apac.anthropic.claude-3-haiku-20240307-v1:0 | $0.2500 | $1.2500 |
| apac.anthropic.claude-3-sonnet-20240229-v1:0 | $3.0000 | $15.0000 |
| apac.anthropic.claude-haiku-4-5-20251001-v1:0 | $1.1000 | $5.5000 |
| apac.anthropic.claude-sonnet-4-20250514-v1:0 | $3.0000 | $15.0000 |
| au.anthropic.claude-haiku-4-5-20251001-v1:0 | $1.1000 | $5.5000 |
| au.anthropic.claude-opus-4-6-v1 | $5.5000 | $27.5000 |
| au.anthropic.claude-opus-4-7 | $5.5000 | $27.5000 |
| au.anthropic.claude-sonnet-4-5-20250929-v1:0 | $3.3000 | $16.5000 |
| au.anthropic.claude-sonnet-4-6 | $3.3000 | $16.5000 |
| bedrock/ap-northeast-1/anthropic.claude-instant-v1 | $2.2300 | $7.5500 |
| bedrock/ap-northeast-1/anthropic.claude-v1 | $8.0000 | $24.0000 |
| bedrock/ap-northeast-1/anthropic.claude-v2:1 | $8.0000 | $24.0000 |
| bedrock/ap-northeast-1/deepseek.v3.2 | $0.7400 | $2.2200 |
| bedrock/ap-northeast-1/minimax.minimax-m2.1 | $0.3600 | $1.4400 |
| bedrock/ap-northeast-1/minimax.minimax-m2.5 | $0.3600 | $1.4400 |
| bedrock/ap-northeast-1/moonshotai.kimi-k2-thinking | $0.7300 | $3.0300 |
| bedrock/ap-northeast-1/moonshotai.kimi-k2.5 | $0.7200 | $3.6000 |
| bedrock/ap-northeast-1/qwen.qwen3-coder-next | $0.6000 | $1.4400 |
| bedrock/ap-south-1/deepseek.v3.2 | $0.7400 | $2.2200 |
| bedrock/ap-south-1/meta.llama3-70b-instruct-v1:0 | $3.1800 | $4.2000 |
| bedrock/ap-south-1/meta.llama3-8b-instruct-v1:0 | $0.3600 | $0.7200 |
| bedrock/ap-south-1/minimax.minimax-m2.1 | $0.3600 | $1.4400 |
| bedrock/ap-south-1/minimax.minimax-m2.5 | $0.3600 | $1.4400 |
| bedrock/ap-south-1/moonshotai.kimi-k2-thinking | $0.7100 | $2.9400 |
| bedrock/ap-south-1/moonshotai.kimi-k2.5 | $0.7200 | $3.6000 |
| bedrock/ap-south-1/qwen.qwen3-coder-next | $0.6000 | $1.4400 |
| bedrock/ap-southeast-2/minimax.minimax-m2.5 | $0.3090 | $1.2360 |
| bedrock/ap-southeast-3/deepseek.v3.2 | $0.7400 | $2.2200 |
| bedrock/ap-southeast-3/minimax.minimax-m2.1 | $0.3600 | $1.4400 |
| bedrock/ap-southeast-3/minimax.minimax-m2.5 | $0.3600 | $1.4400 |
| bedrock/ap-southeast-3/moonshotai.kimi-k2.5 | $0.7200 | $3.6000 |
| bedrock/ap-southeast-3/qwen.qwen3-coder-next | $0.6000 | $1.4400 |
| bedrock/ca-central-1/meta.llama3-70b-instruct-v1:0 | $3.0500 | $4.0300 |
| bedrock/ca-central-1/meta.llama3-8b-instruct-v1:0 | $0.3500 | $0.6900 |
| bedrock/eu-central-1/anthropic.claude-instant-v1 | $2.4800 | $8.3800 |
| bedrock/eu-central-1/anthropic.claude-v1 | $8.0000 | $24.0000 |
| bedrock/eu-central-1/anthropic.claude-v2:1 | $8.0000 | $24.0000 |
| bedrock/eu-central-1/minimax.minimax-m2.1 | $0.3600 | $1.4400 |
| bedrock/eu-central-1/minimax.minimax-m2.5 | $0.3600 | $1.4400 |
| bedrock/eu-central-1/qwen.qwen3-coder-next | $0.6000 | $1.4400 |
| bedrock/eu-north-1/deepseek.v3.2 | $0.7400 | $2.2200 |
| bedrock/eu-north-1/minimax.minimax-m2.1 | $0.3600 | $1.4400 |
| bedrock/eu-north-1/minimax.minimax-m2.5 | $0.3600 | $1.4400 |
| bedrock/eu-north-1/moonshotai.kimi-k2.5 | $0.7200 | $3.6000 |
| bedrock/eu-south-1/minimax.minimax-m2.1 | $0.3600 | $1.4400 |
| bedrock/eu-south-1/minimax.minimax-m2.5 | $0.3600 | $1.4400 |
| bedrock/eu-south-1/qwen.qwen3-coder-next | $0.6000 | $1.4400 |
| bedrock/eu-west-1/meta.llama3-70b-instruct-v1:0 | $2.8600 | $3.7800 |
| bedrock/eu-west-1/meta.llama3-8b-instruct-v1:0 | $0.3200 | $0.6500 |
| bedrock/eu-west-1/minimax.minimax-m2.1 | $0.3600 | $1.4400 |
| bedrock/eu-west-1/minimax.minimax-m2.5 | $0.3600 | $1.4400 |
| bedrock/eu-west-1/qwen.qwen3-coder-next | $0.6000 | $1.4400 |
| bedrock/eu-west-2/meta.llama3-70b-instruct-v1:0 | $3.4500 | $4.5500 |
| bedrock/eu-west-2/meta.llama3-8b-instruct-v1:0 | $0.3900 | $0.7800 |
| bedrock/eu-west-2/minimax.minimax-m2.1 | $0.4700 | $1.8600 |
| bedrock/eu-west-2/minimax.minimax-m2.5 | $0.4700 | $1.8600 |
| bedrock/eu-west-2/qwen.qwen3-coder-next | $0.7800 | $1.8600 |
| bedrock/eu-west-3/mistral.mistral-7b-instruct-v0:2 | $0.2000 | $0.2600 |
| bedrock/eu-west-3/mistral.mistral-large-2402-v1:0 | $10.4000 | $31.2000 |
| bedrock/eu-west-3/mistral.mixtral-8x7b-instruct-v0:1 | $0.5900 | $0.9100 |
| bedrock/invoke/anthropic.claude-3-5-sonnet-20240620-v1:0 | $3.0000 | $15.0000 |
| bedrock/moonshotai.kimi-k2-thinking | $0.7300 | $3.0300 |
| bedrock/moonshotai.kimi-k2.5 | $0.6000 | $3.0300 |
| bedrock/sa-east-1/deepseek.v3.2 | $0.7400 | $2.2200 |
| bedrock/sa-east-1/meta.llama3-70b-instruct-v1:0 | $4.4500 | $5.8800 |
| bedrock/sa-east-1/meta.llama3-8b-instruct-v1:0 | $0.5000 | $1.0100 |
| bedrock/sa-east-1/minimax.minimax-m2.1 | $0.3600 | $1.4400 |
| bedrock/sa-east-1/minimax.minimax-m2.5 | $0.3600 | $1.4400 |
| bedrock/sa-east-1/moonshotai.kimi-k2-thinking | $0.7300 | $3.0300 |
| bedrock/sa-east-1/moonshotai.kimi-k2.5 | $0.7200 | $3.6000 |
| bedrock/sa-east-1/qwen.qwen3-coder-next | $0.6000 | $1.4400 |
| bedrock/us-east-1/anthropic.claude-instant-v1 | $0.8000 | $2.4000 |
| bedrock/us-east-1/anthropic.claude-v1 | $8.0000 | $24.0000 |
| bedrock/us-east-1/anthropic.claude-v2:1 | $8.0000 | $24.0000 |
| bedrock/us-east-1/deepseek.v3.2 | $0.6200 | $1.8500 |
| bedrock/us-east-1/meta.llama3-70b-instruct-v1:0 | $2.6500 | $3.5000 |
| bedrock/us-east-1/meta.llama3-8b-instruct-v1:0 | $0.3000 | $0.6000 |
| bedrock/us-east-1/minimax.minimax-m2.1 | $0.3000 | $1.2000 |
| bedrock/us-east-1/minimax.minimax-m2.5 | $0.3000 | $1.2000 |
| bedrock/us-east-1/mistral.mistral-7b-instruct-v0:2 | $0.1500 | $0.2000 |
| bedrock/us-east-1/mistral.mistral-large-2402-v1:0 | $8.0000 | $24.0000 |
| bedrock/us-east-1/mistral.mixtral-8x7b-instruct-v0:1 | $0.4500 | $0.7000 |
| bedrock/us-east-1/moonshotai.kimi-k2-thinking | $0.6000 | $2.5000 |
| bedrock/us-east-1/moonshotai.kimi-k2.5 | $0.6000 | $3.0000 |
| bedrock/us-east-1/qwen.qwen3-coder-next | $0.5000 | $1.2000 |
| bedrock/us-east-2/deepseek.v3.2 | $0.6200 | $1.8500 |
| bedrock/us-east-2/minimax.minimax-m2.1 | $0.3000 | $1.2000 |
| bedrock/us-east-2/minimax.minimax-m2.5 | $0.3000 | $1.2000 |
| bedrock/us-east-2/moonshotai.kimi-k2-thinking | $0.6000 | $2.5000 |
| bedrock/us-east-2/moonshotai.kimi-k2.5 | $0.6000 | $3.0000 |
| bedrock/us-east-2/qwen.qwen3-coder-next | $0.5000 | $1.2000 |
| bedrock/us-gov-east-1/amazon.nova-pro-v1:0 | $0.9600 | $3.8400 |
| bedrock/us-gov-east-1/amazon.titan-text-express-v1 | $1.3000 | $1.7000 |
| bedrock/us-gov-east-1/amazon.titan-text-lite-v1 | $0.3000 | $0.4000 |
| bedrock/us-gov-east-1/amazon.titan-text-premier-v1:0 | $0.5000 | $1.5000 |
| bedrock/us-gov-east-1/anthropic.claude-3-5-sonnet-20240620-v1:0 | $3.6000 | $18.0000 |
| bedrock/us-gov-east-1/anthropic.claude-3-haiku-20240307-v1:0 | $0.3000 | $1.5000 |
| bedrock/us-gov-east-1/anthropic.claude-haiku-4-5-20251001-v1:0 | $1.2000 | $6.0000 |
| bedrock/us-gov-east-1/anthropic.claude-sonnet-4-5-20250929-v1:0 | $3.3000 | $16.5000 |
| bedrock/us-gov-east-1/claude-sonnet-4-5-20250929-v1:0 | $3.3000 | $16.5000 |
| bedrock/us-gov-east-1/meta.llama3-70b-instruct-v1:0 | $2.6500 | $3.5000 |
| bedrock/us-gov-east-1/meta.llama3-8b-instruct-v1:0 | $0.3000 | $2.6500 |
| bedrock/us-gov-west-1/amazon.nova-pro-v1:0 | $0.9600 | $3.8400 |
| bedrock/us-gov-west-1/amazon.titan-text-express-v1 | $1.3000 | $1.7000 |
| bedrock/us-gov-west-1/amazon.titan-text-lite-v1 | $0.3000 | $0.4000 |
| bedrock/us-gov-west-1/amazon.titan-text-premier-v1:0 | $0.5000 | $1.5000 |
| bedrock/us-gov-west-1/anthropic.claude-3-5-sonnet-20240620-v1:0 | $3.6000 | $18.0000 |
| bedrock/us-gov-west-1/anthropic.claude-3-7-sonnet-20250219-v1:0 | $3.6000 | $18.0000 |
| bedrock/us-gov-west-1/anthropic.claude-3-haiku-20240307-v1:0 | $0.3000 | $1.5000 |
| bedrock/us-gov-west-1/anthropic.claude-haiku-4-5-20251001-v1:0 | $1.2000 | $6.0000 |
| bedrock/us-gov-west-1/anthropic.claude-sonnet-4-5-20250929-v1:0 | $3.3000 | $16.5000 |
| bedrock/us-gov-west-1/claude-sonnet-4-5-20250929-v1:0 | $3.3000 | $16.5000 |
| bedrock/us-gov-west-1/meta.llama3-70b-instruct-v1:0 | $2.6500 | $3.5000 |
| bedrock/us-gov-west-1/meta.llama3-8b-instruct-v1:0 | $0.3000 | $2.6500 |
| bedrock/us-west-1/meta.llama3-70b-instruct-v1:0 | $2.6500 | $3.5000 |
| bedrock/us-west-1/meta.llama3-8b-instruct-v1:0 | $0.3000 | $0.6000 |
| bedrock/us-west-2/anthropic.claude-instant-v1 | $0.8000 | $2.4000 |
| bedrock/us-west-2/anthropic.claude-v1 | $8.0000 | $24.0000 |
| bedrock/us-west-2/anthropic.claude-v2:1 | $8.0000 | $24.0000 |
| bedrock/us-west-2/deepseek.v3.2 | $0.6200 | $1.8500 |
| bedrock/us-west-2/minimax.minimax-m2.1 | $0.3000 | $1.2000 |
| bedrock/us-west-2/minimax.minimax-m2.5 | $0.3000 | $1.2000 |
| bedrock/us-west-2/mistral.mistral-7b-instruct-v0:2 | $0.1500 | $0.2000 |
| bedrock/us-west-2/mistral.mistral-large-2402-v1:0 | $8.0000 | $24.0000 |
| bedrock/us-west-2/mistral.mixtral-8x7b-instruct-v0:1 | $0.4500 | $0.7000 |
| bedrock/us-west-2/moonshotai.kimi-k2-thinking | $0.6000 | $2.5000 |
| bedrock/us-west-2/moonshotai.kimi-k2.5 | $0.6000 | $3.0000 |
| bedrock/us-west-2/qwen.qwen3-coder-next | $0.5000 | $1.2000 |
| bedrock/us.anthropic.claude-3-5-haiku-20241022-v1:0 | $0.8000 | $4.0000 |
| claude-sonnet-4-5-20250929-v1:0 | $3.0000 | $15.0000 |
| cohere.command-light-text-v14 | $0.3000 | $0.6000 |
| cohere.command-r-plus-v1:0 | $3.0000 | $15.0000 |
| cohere.command-r-v1:0 | $0.5000 | $1.5000 |
| cohere.command-text-v14 | $1.5000 | $2.0000 |
| deepseek.v3-v1:0 | $0.5800 | $1.6800 |
| deepseek.v3.2 | $0.6200 | $1.8500 |
| eu.amazon.nova-2-lite-v1:0 | $0.3300 | $2.7500 |
| eu.amazon.nova-2-pro-preview-20251202-v1:0 | $2.1875 | $17.5000 |
| eu.amazon.nova-lite-v1:0 | $0.0780 | $0.3120 |
| eu.amazon.nova-micro-v1:0 | $0.0460 | $0.1840 |
| eu.amazon.nova-pro-v1:0 | $1.0500 | $4.2000 |
| eu.anthropic.claude-3-5-haiku-20241022-v1:0 | $0.2500 | $1.2500 |
| eu.anthropic.claude-3-5-sonnet-20240620-v1:0 | $3.0000 | $15.0000 |
| eu.anthropic.claude-3-5-sonnet-20241022-v2:0 | $3.0000 | $15.0000 |
| eu.anthropic.claude-3-7-sonnet-20250219-v1:0 | $3.0000 | $15.0000 |
| eu.anthropic.claude-3-haiku-20240307-v1:0 | $0.2500 | $1.2500 |
| eu.anthropic.claude-3-opus-20240229-v1:0 | $15.0000 | $75.0000 |
| eu.anthropic.claude-3-sonnet-20240229-v1:0 | $3.0000 | $15.0000 |
| eu.anthropic.claude-haiku-4-5-20251001-v1:0 | $1.1000 | $5.5000 |
| eu.anthropic.claude-opus-4-1-20250805-v1:0 | $15.0000 | $75.0000 |
| eu.anthropic.claude-opus-4-20250514-v1:0 | $15.0000 | $75.0000 |
| eu.anthropic.claude-opus-4-5-20251101-v1:0 | $5.0000 | $25.0000 |
| eu.anthropic.claude-opus-4-6-v1 | $5.5000 | $27.5000 |
| eu.anthropic.claude-opus-4-7 | $5.5000 | $27.5000 |
| eu.anthropic.claude-sonnet-4-20250514-v1:0 | $3.0000 | $15.0000 |
| eu.anthropic.claude-sonnet-4-5-20250929-v1:0 | $3.3000 | $16.5000 |
| eu.anthropic.claude-sonnet-4-6 | $3.3000 | $16.5000 |
| eu.deepseek.v3.2 | $0.7400 | $2.2200 |
| eu.meta.llama3-2-1b-instruct-v1:0 | $0.1300 | $0.1300 |
| eu.meta.llama3-2-3b-instruct-v1:0 | $0.1900 | $0.1900 |
| eu.mistral.pixtral-large-2502-v1:0 | $2.0000 | $6.0000 |
| eu.twelvelabs.pegasus-1-2-v1:0 | $0.0000 | $7.5000 |
| global.amazon.nova-2-lite-v1:0 | $0.3000 | $2.5000 |
| global.anthropic.claude-haiku-4-5-20251001-v1:0 | $1.0000 | $5.0000 |
| global.anthropic.claude-opus-4-5-20251101-v1:0 | $5.0000 | $25.0000 |
| global.anthropic.claude-opus-4-6-v1 | $5.0000 | $25.0000 |
| global.anthropic.claude-opus-4-7 | $5.0000 | $25.0000 |
| global.anthropic.claude-sonnet-4-20250514-v1:0 | $3.0000 | $15.0000 |
| global.anthropic.claude-sonnet-4-5-20250929-v1:0 | $3.0000 | $15.0000 |
| global.anthropic.claude-sonnet-4-6 | $3.0000 | $15.0000 |
| google.gemma-3-12b-it | $0.0900 | $0.2900 |
| google.gemma-3-27b-it | $0.2300 | $0.3800 |
| google.gemma-3-4b-it | $0.0400 | $0.0800 |
| jp.anthropic.claude-haiku-4-5-20251001-v1:0 | $1.1000 | $5.5000 |
| jp.anthropic.claude-sonnet-4-5-20250929-v1:0 | $3.3000 | $16.5000 |
| meta.llama2-13b-chat-v1 | $0.7500 | $1.0000 |
| meta.llama2-70b-chat-v1 | $1.9500 | $2.5600 |
| meta.llama3-1-405b-instruct-v1:0 | $5.3200 | $16.0000 |
| meta.llama3-1-70b-instruct-v1:0 | $0.9900 | $0.9900 |
| meta.llama3-1-8b-instruct-v1:0 | $0.2200 | $0.2200 |
| meta.llama3-2-11b-instruct-v1:0 | $0.3500 | $0.3500 |
| meta.llama3-2-1b-instruct-v1:0 | $0.1000 | $0.1000 |
| meta.llama3-2-3b-instruct-v1:0 | $0.1500 | $0.1500 |
| meta.llama3-2-90b-instruct-v1:0 | $2.0000 | $2.0000 |
| meta.llama3-3-70b-instruct-v1:0 | $0.7200 | $0.7200 |
| meta.llama3-70b-instruct-v1:0 | $2.6500 | $3.5000 |
| meta.llama3-8b-instruct-v1:0 | $0.3000 | $0.6000 |
| meta.llama4-maverick-17b-instruct-v1:0 | $0.2400 | $0.9700 |
| meta.llama4-scout-17b-instruct-v1:0 | $0.1700 | $0.6600 |
| minimax.minimax-m2 | $0.3000 | $1.2000 |
| minimax.minimax-m2.1 | $0.3000 | $1.2000 |
| minimax.minimax-m2.5 | $0.3000 | $1.2000 |
| mistral.devstral-2-123b | $0.4000 | $2.0000 |
| mistral.magistral-small-2509 | $0.5000 | $1.5000 |
| mistral.ministral-3-14b-instruct | $0.2000 | $0.2000 |
| mistral.ministral-3-3b-instruct | $0.1000 | $0.1000 |
| mistral.ministral-3-8b-instruct | $0.1500 | $0.1500 |
| mistral.mistral-7b-instruct-v0:2 | $0.1500 | $0.2000 |
| mistral.mistral-large-2402-v1:0 | $8.0000 | $24.0000 |
| mistral.mistral-large-2407-v1:0 | $3.0000 | $9.0000 |
| mistral.mistral-large-3-675b-instruct | $0.5000 | $1.5000 |
| mistral.mistral-small-2402-v1:0 | $1.0000 | $3.0000 |
| mistral.mixtral-8x7b-instruct-v0:1 | $0.4500 | $0.7000 |
| mistral.voxtral-mini-3b-2507 | $0.0400 | $0.0400 |
| mistral.voxtral-small-24b-2507 | $0.1000 | $0.3000 |
| moonshot.kimi-k2-thinking | $0.6000 | $2.5000 |
| moonshotai.kimi-k2.5 | $0.6000 | $3.0000 |
| nvidia.nemotron-nano-12b-v2 | $0.2000 | $0.6000 |
| nvidia.nemotron-nano-3-30b | $0.0600 | $0.2400 |
| nvidia.nemotron-nano-9b-v2 | $0.0600 | $0.2300 |
| nvidia.nemotron-super-3-120b | $0.1500 | $0.6500 |
| openai.gpt-oss-120b-1:0 | $0.1500 | $0.6000 |
| openai.gpt-oss-20b-1:0 | $0.0700 | $0.3000 |
| openai.gpt-oss-safeguard-120b | $0.1500 | $0.6000 |
| openai.gpt-oss-safeguard-20b | $0.0700 | $0.2000 |
| qwen.qwen3-235b-a22b-2507-v1:0 | $0.2200 | $0.8800 |
| qwen.qwen3-32b-v1:0 | $0.1500 | $0.6000 |
| qwen.qwen3-coder-30b-a3b-v1:0 | $0.1500 | $0.6000 |
| qwen.qwen3-coder-480b-a35b-v1:0 | $0.2200 | $1.8000 |
| qwen.qwen3-coder-next | $0.5000 | $1.2000 |
| qwen.qwen3-next-80b-a3b | $0.1500 | $1.2000 |
| qwen.qwen3-vl-235b-a22b | $0.5300 | $2.6600 |
| twelvelabs.pegasus-1-2-v1:0 | $0.0000 | $7.5000 |
| us-gov.anthropic.claude-sonnet-4-5-20250929-v1:0 | $3.3000 | $16.5000 |
| us.amazon.nova-2-lite-v1:0 | $0.3300 | $2.7500 |
| us.amazon.nova-2-pro-preview-20251202-v1:0 | $2.1875 | $17.5000 |
| us.amazon.nova-lite-v1:0 | $0.0600 | $0.2400 |
| us.amazon.nova-micro-v1:0 | $0.0350 | $0.1400 |
| us.amazon.nova-premier-v1:0 | $2.5000 | $12.5000 |
| us.amazon.nova-pro-v1:0 | $0.8000 | $3.2000 |
| us.anthropic.claude-3-5-haiku-20241022-v1:0 | $0.8000 | $4.0000 |
| us.anthropic.claude-3-5-sonnet-20240620-v1:0 | $3.0000 | $15.0000 |
| us.anthropic.claude-3-5-sonnet-20241022-v2:0 | $3.0000 | $15.0000 |
| us.anthropic.claude-3-7-sonnet-20250219-v1:0 | $3.0000 | $15.0000 |
| us.anthropic.claude-3-haiku-20240307-v1:0 | $0.2500 | $1.2500 |
| us.anthropic.claude-3-opus-20240229-v1:0 | $15.0000 | $75.0000 |
| us.anthropic.claude-3-sonnet-20240229-v1:0 | $3.0000 | $15.0000 |
| us.anthropic.claude-haiku-4-5-20251001-v1:0 | $1.1000 | $5.5000 |
| us.anthropic.claude-opus-4-1-20250805-v1:0 | $15.0000 | $75.0000 |
| us.anthropic.claude-opus-4-20250514-v1:0 | $15.0000 | $75.0000 |
| us.anthropic.claude-opus-4-5-20251101-v1:0 | $5.5000 | $27.5000 |
| us.anthropic.claude-opus-4-6-v1 | $5.5000 | $27.5000 |
| us.anthropic.claude-opus-4-7 | $5.5000 | $27.5000 |
| us.anthropic.claude-sonnet-4-20250514-v1:0 | $3.0000 | $15.0000 |
| us.anthropic.claude-sonnet-4-5-20250929-v1:0 | $3.3000 | $16.5000 |
| us.anthropic.claude-sonnet-4-6 | $3.3000 | $16.5000 |
| us.deepseek.r1-v1:0 | $1.3500 | $5.4000 |
| us.deepseek.v3.2 | $0.6200 | $1.8500 |
| us.meta.llama3-1-405b-instruct-v1:0 | $5.3200 | $16.0000 |
| us.meta.llama3-1-70b-instruct-v1:0 | $0.9900 | $0.9900 |
| us.meta.llama3-1-8b-instruct-v1:0 | $0.2200 | $0.2200 |
| us.meta.llama3-2-11b-instruct-v1:0 | $0.3500 | $0.3500 |
| us.meta.llama3-2-1b-instruct-v1:0 | $0.1000 | $0.1000 |
| us.meta.llama3-2-3b-instruct-v1:0 | $0.1500 | $0.1500 |
| us.meta.llama3-2-90b-instruct-v1:0 | $2.0000 | $2.0000 |
| us.meta.llama3-3-70b-instruct-v1:0 | $0.7200 | $0.7200 |
| us.meta.llama4-maverick-17b-instruct-v1:0 | $0.2400 | $0.9700 |
| us.meta.llama4-scout-17b-instruct-v1:0 | $0.1700 | $0.6600 |
| us.mistral.pixtral-large-2502-v1:0 | $2.0000 | $6.0000 |
| us.twelvelabs.pegasus-1-2-v1:0 | $0.0000 | $7.5000 |
| us.writer.palmyra-x4-v1:0 | $2.5000 | $10.0000 |
| us.writer.palmyra-x5-v1:0 | $0.6000 | $6.0000 |
| writer.palmyra-x4-v1:0 | $2.5000 | $10.0000 |
| writer.palmyra-x5-v1:0 | $0.6000 | $6.0000 |
| zai.glm-4.7 | $0.6000 | $2.2000 |
| zai.glm-4.7-flash | $0.0700 | $0.4000 |
| zai.glm-5 | $1.0000 | $3.2000 |

## AWS Bedrock — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| amazon.nova-2-multimodal-embeddings-v1:0 | $0.1350 | $0.0000 |
| amazon.titan-embed-image-v1 | $0.8000 | $0.0000 |
| amazon.titan-embed-text-v1 | $0.1000 | $0.0000 |
| amazon.titan-embed-text-v2:0 | $0.2000 | $0.0000 |
| bedrock/us-gov-east-1/amazon.titan-embed-text-v1 | $0.1000 | $0.0000 |
| bedrock/us-gov-east-1/amazon.titan-embed-text-v2:0 | $0.2000 | $0.0000 |
| bedrock/us-gov-west-1/amazon.titan-embed-text-v1 | $0.1000 | $0.0000 |
| bedrock/us-gov-west-1/amazon.titan-embed-text-v2:0 | $0.2000 | $0.0000 |
| cohere.embed-english-v3 | $0.1000 | $0.0000 |
| cohere.embed-multilingual-v3 | $0.1000 | $0.0000 |
| cohere.embed-v4:0 | $0.1200 | $0.0000 |
| eu.twelvelabs.marengo-embed-2-7-v1:0 | $70.0000 | $0.0000 |
| twelvelabs.marengo-embed-2-7-v1:0 | $70.0000 | $0.0000 |
| us.twelvelabs.marengo-embed-2-7-v1:0 | $70.0000 | $0.0000 |

## AWS Bedrock — image_edit (per 1M images)

| Model | Input | Output |
|-------|-------|--------|
| stability.stable-conservative-upscale-v1:0 | $0.0000 | $400000.0000 |
| stability.stable-creative-upscale-v1:0 | $0.0000 | $600000.0000 |
| stability.stable-fast-upscale-v1:0 | $0.0000 | $30000.0000 |
| stability.stable-image-control-sketch-v1:0 | $0.0000 | $70000.0000 |
| stability.stable-image-control-structure-v1:0 | $0.0000 | $70000.0000 |
| stability.stable-image-erase-object-v1:0 | $0.0000 | $70000.0000 |
| stability.stable-image-inpaint-v1:0 | $0.0000 | $70000.0000 |
| stability.stable-image-remove-background-v1:0 | $0.0000 | $70000.0000 |
| stability.stable-image-search-recolor-v1:0 | $0.0000 | $70000.0000 |
| stability.stable-image-search-replace-v1:0 | $0.0000 | $70000.0000 |
| stability.stable-image-style-guide-v1:0 | $0.0000 | $70000.0000 |
| stability.stable-outpaint-v1:0 | $0.0000 | $60000.0000 |
| stability.stable-style-transfer-v1:0 | $0.0000 | $80000.0000 |

## AWS Bedrock — image_generation (per 1M images)

| Model | Input | Output |
|-------|-------|--------|
| 1024-x-1024/50-steps/bedrock/amazon.nova-canvas-v1:0 | $0.0000 | $60000.0000 |
| 1024-x-1024/50-steps/stability.stable-diffusion-xl-v1 | $0.0000 | $40000.0000 |
| 1024-x-1024/max-steps/stability.stable-diffusion-xl-v1 | $0.0000 | $80000.0000 |
| 512-x-512/50-steps/stability.stable-diffusion-xl-v0 | $0.0000 | $18000.0000 |
| 512-x-512/max-steps/stability.stable-diffusion-xl-v0 | $0.0000 | $36000.0000 |
| amazon.nova-canvas-v1:0 | $0.0000 | $60000.0000 |
| amazon.titan-image-generator-v1 | $0.0000 | $8000.0000 |
| amazon.titan-image-generator-v2 | $0.0000 | $8000.0000 |
| amazon.titan-image-generator-v2:0 | $0.0000 | $8000.0000 |
| max-x-max/50-steps/stability.stable-diffusion-xl-v0 | $0.0000 | $36000.0000 |
| max-x-max/max-steps/stability.stable-diffusion-xl-v0 | $0.0000 | $72000.0000 |
| stability.sd3-5-large-v1:0 | $0.0000 | $80000.0000 |
| stability.sd3-large-v1:0 | $0.0000 | $80000.0000 |
| stability.stable-image-core-v1:0 | $0.0000 | $40000.0000 |
| stability.stable-image-core-v1:1 | $0.0000 | $40000.0000 |
| stability.stable-image-ultra-v1:0 | $0.0000 | $140000.0000 |
| stability.stable-image-ultra-v1:1 | $0.0000 | $140000.0000 |
| us.amazon.nova-canvas-v1:0 | $0.0000 | $60000.0000 |

## AWS Bedrock — rerank (per 1M queries)

| Model | Input | Output |
|-------|-------|--------|
| amazon.rerank-v1:0 | $1000.0000 | $0.0000 |
| cohere.rerank-v3-5:0 | $2000.0000 | $0.0000 |

## Aiml — image_generation (per 1M images)

| Model | Input | Output |
|-------|-------|--------|
| aiml/dall-e-2 | $0.0000 | $26000.0000 |
| aiml/dall-e-3 | $0.0000 | $52000.0000 |
| aiml/flux-pro | $0.0000 | $65000.0000 |
| aiml/flux-pro/v1.1 | $0.0000 | $52000.0000 |
| aiml/flux-pro/v1.1-ultra | $0.0000 | $63000.0000 |
| aiml/flux-realism | $0.0000 | $46000.0000 |
| aiml/flux/dev | $0.0000 | $33000.0000 |
| aiml/flux/kontext-max/text-to-image | $0.0000 | $104000.0000 |
| aiml/flux/kontext-pro/text-to-image | $0.0000 | $52000.0000 |
| aiml/flux/schnell | $0.0000 | $4000.0000 |
| aiml/google/imagen-4.0-ultra-generate-001 | $0.0000 | $78000.0000 |
| aiml/google/nano-banana-pro | $0.0000 | $195000.0000 |

## Aleph Alpha — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| luminous-base-control | $37.5000 | $41.2500 |
| luminous-extended-control | $56.2500 | $61.8750 |
| luminous-supreme-control | $218.7500 | $240.6250 |

## Aleph Alpha — completion (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| luminous-base | $30.0000 | $33.0000 |
| luminous-extended | $45.0000 | $49.5000 |
| luminous-supreme | $175.0000 | $192.5000 |

## Amazon Nova — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| amazon-nova/nova-lite-v1 | $0.0600 | $0.2400 |
| amazon-nova/nova-micro-v1 | $0.0350 | $0.1400 |
| amazon-nova/nova-premier-v1 | $2.5000 | $12.5000 |
| amazon-nova/nova-pro-v1 | $0.8000 | $3.2000 |

## Anthropic — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| claude-3-7-sonnet-20250219 | $3.0000 | $15.0000 |
| claude-3-haiku-20240307 | $0.2500 | $1.2500 |
| claude-3-opus-20240229 | $15.0000 | $75.0000 |
| claude-4-opus-20250514 | $15.0000 | $75.0000 |
| claude-4-sonnet-20250514 | $3.0000 | $15.0000 |
| claude-haiku-4-5 | $1.0000 | $5.0000 |
| claude-haiku-4-5-20251001 | $1.0000 | $5.0000 |
| claude-opus-4-1 | $15.0000 | $75.0000 |
| claude-opus-4-1-20250805 | $15.0000 | $75.0000 |
| claude-opus-4-20250514 | $15.0000 | $75.0000 |
| claude-opus-4-5 | $5.0000 | $25.0000 |
| claude-opus-4-5-20251101 | $5.0000 | $25.0000 |
| claude-opus-4-6 | $5.0000 | $25.0000 |
| claude-opus-4-6-20260205 | $5.0000 | $25.0000 |
| claude-opus-4-7 | $5.0000 | $25.0000 |
| claude-opus-4-7-20260416 | $5.0000 | $25.0000 |
| claude-sonnet-4-20250514 | $3.0000 | $15.0000 |
| claude-sonnet-4-5 | $3.0000 | $15.0000 |
| claude-sonnet-4-5-20250929 | $3.0000 | $15.0000 |
| claude-sonnet-4-6 | $3.0000 | $15.0000 |

## Anyscale — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| anyscale/HuggingFaceH4/zephyr-7b-beta | $0.1500 | $0.1500 |
| anyscale/codellama/CodeLlama-34b-Instruct-hf | $1.0000 | $1.0000 |
| anyscale/codellama/CodeLlama-70b-Instruct-hf | $1.0000 | $1.0000 |
| anyscale/google/gemma-7b-it | $0.1500 | $0.1500 |
| anyscale/meta-llama/Llama-2-13b-chat-hf | $0.2500 | $0.2500 |
| anyscale/meta-llama/Llama-2-70b-chat-hf | $1.0000 | $1.0000 |
| anyscale/meta-llama/Llama-2-7b-chat-hf | $0.1500 | $0.1500 |
| anyscale/meta-llama/Meta-Llama-3-70B-Instruct | $1.0000 | $1.0000 |
| anyscale/meta-llama/Meta-Llama-3-8B-Instruct | $0.1500 | $0.1500 |
| anyscale/mistralai/Mistral-7B-Instruct-v0.1 | $0.1500 | $0.1500 |
| anyscale/mistralai/Mixtral-8x22B-Instruct-v0.1 | $0.9000 | $0.9000 |
| anyscale/mistralai/Mixtral-8x7B-Instruct-v0.1 | $0.1500 | $0.1500 |

## AssemblyAI — audio_transcription (per 1M seconds)

| Model | Input | Output |
|-------|-------|--------|
| assemblyai/best | $33.3300 | $0.0000 |
| assemblyai/nano | $102.7800 | $0.0000 |

## Aws Polly — audio_speech (per 1M characters)

| Model | Input | Output |
|-------|-------|--------|
| aws_polly/generative | $30.0000 | $0.0000 |
| aws_polly/long-form | $100.0000 | $0.0000 |
| aws_polly/neural | $16.0000 | $0.0000 |
| aws_polly/standard | $4.0000 | $0.0000 |

## Azure AI — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| azure_ai/Llama-3.2-11B-Vision-Instruct | $0.3700 | $0.3700 |
| azure_ai/Llama-3.2-90B-Vision-Instruct | $2.0400 | $2.0400 |
| azure_ai/Llama-3.3-70B-Instruct | $0.7100 | $0.7100 |
| azure_ai/Llama-4-Maverick-17B-128E-Instruct-FP8 | $1.4100 | $0.3500 |
| azure_ai/Llama-4-Scout-17B-16E-Instruct | $0.2000 | $0.7800 |
| azure_ai/MAI-DS-R1 | $1.3500 | $5.4000 |
| azure_ai/Meta-Llama-3-70B-Instruct | $1.1000 | $0.3700 |
| azure_ai/Meta-Llama-3.1-405B-Instruct | $5.3300 | $16.0000 |
| azure_ai/Meta-Llama-3.1-70B-Instruct | $2.6800 | $3.5400 |
| azure_ai/Meta-Llama-3.1-8B-Instruct | $0.3000 | $0.6100 |
| azure_ai/Phi-3-medium-128k-instruct | $0.1700 | $0.6800 |
| azure_ai/Phi-3-medium-4k-instruct | $0.1700 | $0.6800 |
| azure_ai/Phi-3-mini-128k-instruct | $0.1300 | $0.5200 |
| azure_ai/Phi-3-mini-4k-instruct | $0.1300 | $0.5200 |
| azure_ai/Phi-3-small-128k-instruct | $0.1500 | $0.6000 |
| azure_ai/Phi-3-small-8k-instruct | $0.1500 | $0.6000 |
| azure_ai/Phi-3.5-MoE-instruct | $0.1600 | $0.6400 |
| azure_ai/Phi-3.5-mini-instruct | $0.1300 | $0.5200 |
| azure_ai/Phi-3.5-vision-instruct | $0.1300 | $0.5200 |
| azure_ai/Phi-4 | $0.1250 | $0.5000 |
| azure_ai/Phi-4-mini-instruct | $0.0750 | $0.3000 |
| azure_ai/Phi-4-mini-reasoning | $0.0800 | $0.3200 |
| azure_ai/Phi-4-multimodal-instruct | $0.0800 | $0.3200 |
| azure_ai/Phi-4-reasoning | $0.1250 | $0.5000 |
| azure_ai/claude-haiku-4-5 | $1.0000 | $5.0000 |
| azure_ai/claude-opus-4-1 | $15.0000 | $75.0000 |
| azure_ai/claude-opus-4-5 | $5.0000 | $25.0000 |
| azure_ai/claude-opus-4-6 | $5.0000 | $25.0000 |
| azure_ai/claude-opus-4-7 | $5.0000 | $25.0000 |
| azure_ai/claude-sonnet-4-5 | $3.0000 | $15.0000 |
| azure_ai/claude-sonnet-4-6 | $3.0000 | $15.0000 |
| azure_ai/deepseek-r1 | $1.3500 | $5.4000 |
| azure_ai/deepseek-v3 | $1.1400 | $4.5600 |
| azure_ai/deepseek-v3-0324 | $1.1400 | $4.5600 |
| azure_ai/deepseek-v3.2 | $0.5800 | $1.6800 |
| azure_ai/deepseek-v3.2-speciale | $0.5800 | $1.6800 |
| azure_ai/global/grok-3 | $3.0000 | $15.0000 |
| azure_ai/global/grok-3-mini | $0.2500 | $1.2700 |
| azure_ai/gpt-oss-120b | $0.1500 | $0.6000 |
| azure_ai/grok-3 | $3.0000 | $15.0000 |
| azure_ai/grok-3-mini | $0.2500 | $1.2700 |
| azure_ai/grok-4 | $3.0000 | $15.0000 |
| azure_ai/grok-4-1-fast-non-reasoning | $0.2000 | $0.5000 |
| azure_ai/grok-4-1-fast-reasoning | $0.2000 | $0.5000 |
| azure_ai/grok-4-fast-non-reasoning | $0.2000 | $0.5000 |
| azure_ai/grok-4-fast-reasoning | $0.2000 | $0.5000 |
| azure_ai/grok-code-fast-1 | $0.2000 | $1.5000 |
| azure_ai/jais-30b-chat | $3200.0000 | $9710.0000 |
| azure_ai/jamba-instruct | $0.5000 | $0.7000 |
| azure_ai/kimi-k2.5 | $0.6000 | $3.0000 |
| azure_ai/ministral-3b | $0.0400 | $0.0400 |
| azure_ai/mistral-large | $4.0000 | $12.0000 |
| azure_ai/mistral-large-2407 | $2.0000 | $6.0000 |
| azure_ai/mistral-large-3 | $0.5000 | $1.5000 |
| azure_ai/mistral-large-latest | $2.0000 | $6.0000 |
| azure_ai/mistral-medium-2505 | $0.4000 | $2.0000 |
| azure_ai/mistral-nemo | $0.1500 | $0.1500 |
| azure_ai/mistral-small | $1.0000 | $3.0000 |
| azure_ai/mistral-small-2503 | $0.1000 | $0.3000 |
| azure_ai/model_router | $0.1400 | $0.0000 |

## Azure AI — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| azure_ai/Cohere-embed-v3-english | $0.1000 | $0.0000 |
| azure_ai/Cohere-embed-v3-multilingual | $0.1000 | $0.0000 |
| azure_ai/embed-v-4-0 | $0.1200 | $0.0000 |

## Azure AI — image_generation (per 1M images)

| Model | Input | Output |
|-------|-------|--------|
| azure_ai/FLUX-1.1-pro | $0.0000 | $40000.0000 |
| azure_ai/FLUX.1-Kontext-pro | $0.0000 | $40000.0000 |
| azure_ai/flux.2-pro | $0.0000 | $40000.0000 |

## Azure AI — ocr (per 1M pages)

| Model | Input | Output |
|-------|-------|--------|
| azure_ai/doc-intelligence/prebuilt-document | $10000.0000 | $0.0000 |
| azure_ai/doc-intelligence/prebuilt-layout | $10000.0000 | $0.0000 |
| azure_ai/doc-intelligence/prebuilt-read | $1500.0000 | $0.0000 |
| azure_ai/mistral-document-ai-2505 | $3000.0000 | $0.0000 |
| azure_ai/mistral-document-ai-2512 | $3000.0000 | $0.0000 |

## Azure AI — rerank (per 1M queries)

| Model | Input | Output |
|-------|-------|--------|
| azure_ai/cohere-rerank-v3-english | $2000.0000 | $0.0000 |
| azure_ai/cohere-rerank-v3-multilingual | $2000.0000 | $0.0000 |
| azure_ai/cohere-rerank-v3.5 | $2000.0000 | $0.0000 |
| azure_ai/cohere-rerank-v4.0-fast | $2000.0000 | $0.0000 |
| azure_ai/cohere-rerank-v4.0-pro | $2500.0000 | $0.0000 |

## Azure OpenAI — audio_speech (per 1M characters)

| Model | Input | Output |
|-------|-------|--------|
| azure/speech/azure-tts | $15.0000 | $0.0000 |
| azure/speech/azure-tts-hd | $30.0000 | $0.0000 |
| azure/tts-1 | $15.0000 | $0.0000 |
| azure/tts-1-hd | $30.0000 | $0.0000 |

## Azure OpenAI — audio_speech (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| azure/gpt-4o-mini-tts | $2.5000 | $250.0000 |

## Azure OpenAI — audio_transcription (per 1M seconds)

| Model | Input | Output |
|-------|-------|--------|
| azure/whisper-1 | $100.0000 | $100.0000 |

## Azure OpenAI — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| azure/command-r-plus | $3.0000 | $15.0000 |
| azure/computer-use-preview | $3.0000 | $12.0000 |
| azure/eu/gpt-4o-2024-08-06 | $2.7500 | $11.0000 |
| azure/eu/gpt-4o-2024-11-20 | $2.7500 | $11.0000 |
| azure/eu/gpt-4o-mini-2024-07-18 | $0.1650 | $0.6600 |
| azure/eu/gpt-4o-mini-realtime-preview-2024-12-17 | $0.6600 | $2.6400 |
| azure/eu/gpt-4o-realtime-preview-2024-10-01 | $5.5000 | $22.0000 |
| azure/eu/gpt-4o-realtime-preview-2024-12-17 | $5.5000 | $22.0000 |
| azure/eu/gpt-5-2025-08-07 | $1.3750 | $11.0000 |
| azure/eu/gpt-5-mini-2025-08-07 | $0.2750 | $2.2000 |
| azure/eu/gpt-5-nano-2025-08-07 | $0.0550 | $0.4400 |
| azure/eu/gpt-5.1 | $1.3800 | $11.0000 |
| azure/eu/gpt-5.1-chat | $1.3800 | $11.0000 |
| azure/eu/o1-2024-12-17 | $16.5000 | $66.0000 |
| azure/eu/o1-mini-2024-09-12 | $1.2100 | $4.8400 |
| azure/eu/o1-preview-2024-09-12 | $16.5000 | $66.0000 |
| azure/eu/o3-mini-2025-01-31 | $1.2100 | $4.8400 |
| azure/global-standard/gpt-4o-2024-08-06 | $2.5000 | $10.0000 |
| azure/global-standard/gpt-4o-2024-11-20 | $2.5000 | $10.0000 |
| azure/global-standard/gpt-4o-mini | $0.1500 | $0.6000 |
| azure/global/gpt-4o-2024-08-06 | $2.5000 | $10.0000 |
| azure/global/gpt-4o-2024-11-20 | $2.5000 | $10.0000 |
| azure/global/gpt-5.1 | $1.2500 | $10.0000 |
| azure/global/gpt-5.1-chat | $1.2500 | $10.0000 |
| azure/gpt-3.5-turbo | $0.5000 | $1.5000 |
| azure/gpt-3.5-turbo-0125 | $0.5000 | $1.5000 |
| azure/gpt-35-turbo | $0.5000 | $1.5000 |
| azure/gpt-35-turbo-0125 | $0.5000 | $1.5000 |
| azure/gpt-35-turbo-1106 | $1.0000 | $2.0000 |
| azure/gpt-35-turbo-16k | $3.0000 | $4.0000 |
| azure/gpt-35-turbo-16k-0613 | $3.0000 | $4.0000 |
| azure/gpt-4 | $30.0000 | $60.0000 |
| azure/gpt-4-0125-preview | $10.0000 | $30.0000 |
| azure/gpt-4-0613 | $30.0000 | $60.0000 |
| azure/gpt-4-1106-preview | $10.0000 | $30.0000 |
| azure/gpt-4-32k | $60.0000 | $120.0000 |
| azure/gpt-4-32k-0613 | $60.0000 | $120.0000 |
| azure/gpt-4-turbo | $10.0000 | $30.0000 |
| azure/gpt-4-turbo-2024-04-09 | $10.0000 | $30.0000 |
| azure/gpt-4-turbo-vision-preview | $10.0000 | $30.0000 |
| azure/gpt-4.1 | $2.0000 | $8.0000 |
| azure/gpt-4.1-2025-04-14 | $2.0000 | $8.0000 |
| azure/gpt-4.1-mini | $0.4000 | $1.6000 |
| azure/gpt-4.1-mini-2025-04-14 | $0.4000 | $1.6000 |
| azure/gpt-4.1-nano | $0.1000 | $0.4000 |
| azure/gpt-4.1-nano-2025-04-14 | $0.1000 | $0.4000 |
| azure/gpt-4.5-preview | $75.0000 | $150.0000 |
| azure/gpt-4o | $2.5000 | $10.0000 |
| azure/gpt-4o-2024-05-13 | $5.0000 | $15.0000 |
| azure/gpt-4o-2024-08-06 | $2.5000 | $10.0000 |
| azure/gpt-4o-2024-11-20 | $2.7500 | $11.0000 |
| azure/gpt-4o-audio-preview-2024-12-17 | $2.5000 | $10.0000 |
| azure/gpt-4o-mini | $0.1650 | $0.6600 |
| azure/gpt-4o-mini-2024-07-18 | $0.1650 | $0.6600 |
| azure/gpt-4o-mini-audio-preview-2024-12-17 | $2.5000 | $10.0000 |
| azure/gpt-4o-mini-realtime-preview-2024-12-17 | $0.6000 | $2.4000 |
| azure/gpt-4o-realtime-preview-2024-10-01 | $5.0000 | $20.0000 |
| azure/gpt-4o-realtime-preview-2024-12-17 | $5.0000 | $20.0000 |
| azure/gpt-5 | $1.2500 | $10.0000 |
| azure/gpt-5-2025-08-07 | $1.2500 | $10.0000 |
| azure/gpt-5-chat | $1.2500 | $10.0000 |
| azure/gpt-5-chat-latest | $1.2500 | $10.0000 |
| azure/gpt-5-mini | $0.2500 | $2.0000 |
| azure/gpt-5-mini-2025-08-07 | $0.2500 | $2.0000 |
| azure/gpt-5-nano | $0.0500 | $0.4000 |
| azure/gpt-5-nano-2025-08-07 | $0.0500 | $0.4000 |
| azure/gpt-5.1 | $1.2500 | $10.0000 |
| azure/gpt-5.1-2025-11-13 | $1.2500 | $10.0000 |
| azure/gpt-5.1-chat | $1.2500 | $10.0000 |
| azure/gpt-5.1-chat-2025-11-13 | $1.2500 | $10.0000 |
| azure/gpt-5.2 | $1.7500 | $14.0000 |
| azure/gpt-5.2-2025-12-11 | $1.7500 | $14.0000 |
| azure/gpt-5.2-chat | $1.7500 | $14.0000 |
| azure/gpt-5.2-chat-2025-12-11 | $1.7500 | $14.0000 |
| azure/gpt-5.3-chat | $1.7500 | $14.0000 |
| azure/gpt-5.4 | $2.5000 | $15.0000 |
| azure/gpt-5.4-2026-03-05 | $2.5000 | $15.0000 |
| azure/gpt-5.4-mini | $0.7500 | $4.5000 |
| azure/gpt-5.4-nano | $0.2000 | $1.2500 |
| azure/gpt-audio-1.5-2026-02-23 | $2.5000 | $10.0000 |
| azure/gpt-audio-2025-08-28 | $2.5000 | $10.0000 |
| azure/gpt-audio-mini-2025-10-06 | $0.6000 | $2.4000 |
| azure/gpt-realtime-1.5-2026-02-23 | $4.0000 | $16.0000 |
| azure/gpt-realtime-2025-08-28 | $4.0000 | $16.0000 |
| azure/gpt-realtime-mini-2025-10-06 | $0.6000 | $2.4000 |
| azure/mistral-large-2402 | $8.0000 | $24.0000 |
| azure/mistral-large-latest | $8.0000 | $24.0000 |
| azure/o1 | $15.0000 | $60.0000 |
| azure/o1-2024-12-17 | $15.0000 | $60.0000 |
| azure/o1-mini | $1.2100 | $4.8400 |
| azure/o1-mini-2024-09-12 | $1.1000 | $4.4000 |
| azure/o1-preview | $15.0000 | $60.0000 |
| azure/o1-preview-2024-09-12 | $15.0000 | $60.0000 |
| azure/o3 | $2.0000 | $8.0000 |
| azure/o3-2025-04-16 | $2.0000 | $8.0000 |
| azure/o3-mini | $1.1000 | $4.4000 |
| azure/o3-mini-2025-01-31 | $1.1000 | $4.4000 |
| azure/o4-mini | $1.1000 | $4.4000 |
| azure/o4-mini-2025-04-16 | $1.1000 | $4.4000 |
| azure/us/gpt-4.1-2025-04-14 | $2.2000 | $8.8000 |
| azure/us/gpt-4.1-mini-2025-04-14 | $0.4400 | $1.7600 |
| azure/us/gpt-4.1-nano-2025-04-14 | $0.1100 | $0.4400 |
| azure/us/gpt-4o-2024-08-06 | $2.7500 | $11.0000 |
| azure/us/gpt-4o-2024-11-20 | $2.7500 | $11.0000 |
| azure/us/gpt-4o-mini-2024-07-18 | $0.1650 | $0.6600 |
| azure/us/gpt-4o-mini-realtime-preview-2024-12-17 | $0.6600 | $2.6400 |
| azure/us/gpt-4o-realtime-preview-2024-10-01 | $5.5000 | $22.0000 |
| azure/us/gpt-4o-realtime-preview-2024-12-17 | $5.5000 | $22.0000 |
| azure/us/gpt-5-2025-08-07 | $1.3750 | $11.0000 |
| azure/us/gpt-5-mini-2025-08-07 | $0.2750 | $2.2000 |
| azure/us/gpt-5-nano-2025-08-07 | $0.0550 | $0.4400 |
| azure/us/gpt-5.1 | $1.3800 | $11.0000 |
| azure/us/gpt-5.1-chat | $1.3800 | $11.0000 |
| azure/us/o1-2024-12-17 | $16.5000 | $66.0000 |
| azure/us/o1-mini-2024-09-12 | $1.2100 | $4.8400 |
| azure/us/o1-preview-2024-09-12 | $16.5000 | $66.0000 |
| azure/us/o3-2025-04-16 | $2.2000 | $8.8000 |
| azure/us/o3-mini-2025-01-31 | $1.2100 | $4.8400 |
| azure/us/o4-mini-2025-04-16 | $1.2100 | $4.8400 |
| computer-use-preview | $3.0000 | $12.0000 |

## Azure OpenAI — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| azure/ada | $0.1000 | $0.0000 |
| azure/text-embedding-3-large | $0.1300 | $0.0000 |
| azure/text-embedding-3-small | $0.0200 | $0.0000 |
| azure/text-embedding-ada-002 | $0.1000 | $0.0000 |

## Azure OpenAI — responses (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| azure/codex-mini | $1.5000 | $6.0000 |
| azure/eu/gpt-5.1-codex | $1.3800 | $11.0000 |
| azure/eu/gpt-5.1-codex-mini | $0.2750 | $2.2000 |
| azure/global/gpt-5.1-codex | $1.2500 | $10.0000 |
| azure/global/gpt-5.1-codex-mini | $0.2500 | $2.0000 |
| azure/gpt-5-codex | $1.2500 | $10.0000 |
| azure/gpt-5-pro | $15.0000 | $120.0000 |
| azure/gpt-5.1-codex | $1.2500 | $10.0000 |
| azure/gpt-5.1-codex-2025-11-13 | $1.2500 | $10.0000 |
| azure/gpt-5.1-codex-max | $1.2500 | $10.0000 |
| azure/gpt-5.1-codex-mini | $0.2500 | $2.0000 |
| azure/gpt-5.1-codex-mini-2025-11-13 | $0.2500 | $2.0000 |
| azure/gpt-5.2-codex | $1.7500 | $14.0000 |
| azure/gpt-5.2-pro | $21.0000 | $168.0000 |
| azure/gpt-5.2-pro-2025-12-11 | $21.0000 | $168.0000 |
| azure/gpt-5.3-codex | $1.7500 | $14.0000 |
| azure/gpt-5.4-pro | $30.0000 | $180.0000 |
| azure/gpt-5.4-pro-2026-03-05 | $30.0000 | $180.0000 |
| azure/o3-deep-research | $10.0000 | $40.0000 |
| azure/o3-pro | $20.0000 | $80.0000 |
| azure/o3-pro-2025-06-10 | $20.0000 | $80.0000 |
| azure/us/gpt-5.1-codex | $1.3800 | $11.0000 |
| azure/us/gpt-5.1-codex-mini | $0.2750 | $2.2000 |

## Azure Text — completion (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| azure/gpt-3.5-turbo-instruct-0914 | $1.5000 | $2.0000 |
| azure/gpt-35-turbo-instruct | $1.5000 | $2.0000 |
| azure/gpt-35-turbo-instruct-0914 | $1.5000 | $2.0000 |

## Baseten — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| baseten/MiniMaxAI/MiniMax-M2.5 | $0.3000 | $1.2000 |
| baseten/deepseek-ai/DeepSeek-V3-0324 | $0.7700 | $0.7700 |
| baseten/deepseek-ai/DeepSeek-V3.1 | $0.5000 | $1.5000 |
| baseten/moonshotai/Kimi-K2-Instruct-0905 | $0.6000 | $2.5000 |
| baseten/moonshotai/Kimi-K2-Thinking | $0.6000 | $2.5000 |
| baseten/moonshotai/Kimi-K2.5 | $0.6000 | $3.0000 |
| baseten/nvidia/Nemotron-120B-A12B | $0.3000 | $0.7500 |
| baseten/openai/gpt-oss-120b | $0.1000 | $0.5000 |
| baseten/zai-org/GLM-4.6 | $0.6000 | $2.2000 |
| baseten/zai-org/GLM-4.7 | $0.6000 | $2.2000 |
| baseten/zai-org/GLM-5 | $0.9500 | $3.1500 |

## Bedrock Mantle — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| bedrock_mantle/openai.gpt-oss-120b | $0.1500 | $0.6000 |
| bedrock_mantle/openai.gpt-oss-20b | $0.0750 | $0.3000 |
| bedrock_mantle/openai.gpt-oss-safeguard-120b | $0.1500 | $0.6000 |
| bedrock_mantle/openai.gpt-oss-safeguard-20b | $0.0750 | $0.3000 |

## Black Forest Labs — image_edit (per 1M images)

| Model | Input | Output |
|-------|-------|--------|
| black_forest_labs/flux-kontext-max | $0.0000 | $80000.0000 |
| black_forest_labs/flux-kontext-pro | $0.0000 | $40000.0000 |
| black_forest_labs/flux-pro-1.0-expand | $0.0000 | $50000.0000 |
| black_forest_labs/flux-pro-1.0-fill | $0.0000 | $50000.0000 |

## Black Forest Labs — image_generation (per 1M images)

| Model | Input | Output |
|-------|-------|--------|
| black_forest_labs/flux-dev | $0.0000 | $25000.0000 |
| black_forest_labs/flux-pro | $0.0000 | $50000.0000 |
| black_forest_labs/flux-pro-1.1 | $0.0000 | $40000.0000 |
| black_forest_labs/flux-pro-1.1-ultra | $0.0000 | $60000.0000 |

## Cerebras — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| cerebras/gpt-oss-120b | $0.3500 | $0.7500 |
| cerebras/llama-3.3-70b | $0.8500 | $1.2000 |
| cerebras/llama3.1-70b | $0.6000 | $0.6000 |
| cerebras/llama3.1-8b | $0.1000 | $0.1000 |
| cerebras/qwen-3-32b | $0.4000 | $0.8000 |
| cerebras/zai-glm-4.6 | $2.2500 | $2.7500 |
| cerebras/zai-glm-4.7 | $2.2500 | $2.7500 |

## Cloudflare — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| cloudflare/@cf/meta/llama-2-7b-chat-fp16 | $1.9230 | $1.9230 |
| cloudflare/@cf/meta/llama-2-7b-chat-int8 | $1.9230 | $1.9230 |
| cloudflare/@cf/mistral/mistral-7b-instruct-v0.1 | $1.9230 | $1.9230 |
| cloudflare/@hf/thebloke/codellama-7b-instruct-awq | $1.9230 | $1.9230 |

## Cohere — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| command-a-03-2025 | $2.5000 | $10.0000 |
| command-light | $0.3000 | $0.6000 |
| command-r | $0.1500 | $0.6000 |
| command-r-08-2024 | $0.1500 | $0.6000 |
| command-r-plus | $2.5000 | $10.0000 |
| command-r-plus-08-2024 | $2.5000 | $10.0000 |
| command-r7b-12-2024 | $0.1500 | $0.0375 |

## Cohere — completion (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| command | $1.0000 | $2.0000 |
| command-nightly | $1.0000 | $2.0000 |

## Cohere — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| cohere/embed-v4.0 | $0.1200 | $0.0000 |
| embed-english-light-v2.0 | $0.1000 | $0.0000 |
| embed-english-light-v3.0 | $0.1000 | $0.0000 |
| embed-english-v2.0 | $0.1000 | $0.0000 |
| embed-english-v3.0 | $0.1000 | $0.0000 |
| embed-multilingual-light-v3.0 | $100.0000 | $0.0000 |
| embed-multilingual-v2.0 | $0.1000 | $0.0000 |
| embed-multilingual-v3.0 | $0.1000 | $0.0000 |

## Cohere — rerank (per 1M queries)

| Model | Input | Output |
|-------|-------|--------|
| rerank-english-v2.0 | $2000.0000 | $0.0000 |
| rerank-english-v3.0 | $2000.0000 | $0.0000 |
| rerank-multilingual-v2.0 | $2000.0000 | $0.0000 |
| rerank-multilingual-v3.0 | $2000.0000 | $0.0000 |
| rerank-v3.5 | $2000.0000 | $0.0000 |

## Dashscope — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| dashscope/qwen-coder | $0.3000 | $1.5000 |
| dashscope/qwen-max | $1.6000 | $6.4000 |
| dashscope/qwen-plus | $0.4000 | $1.2000 |
| dashscope/qwen-plus-2025-01-25 | $0.4000 | $1.2000 |
| dashscope/qwen-plus-2025-04-28 | $0.4000 | $1.2000 |
| dashscope/qwen-plus-2025-07-14 | $0.4000 | $1.2000 |
| dashscope/qwen-turbo | $0.0500 | $0.2000 |
| dashscope/qwen-turbo-2024-11-01 | $0.0500 | $0.2000 |
| dashscope/qwen-turbo-2025-04-28 | $0.0500 | $0.2000 |
| dashscope/qwen-turbo-latest | $0.0500 | $0.2000 |
| dashscope/qwen3-next-80b-a3b-instruct | $0.1500 | $1.2000 |
| dashscope/qwen3-next-80b-a3b-thinking | $0.1500 | $1.2000 |
| dashscope/qwen3-vl-235b-a22b-instruct | $0.4000 | $1.6000 |
| dashscope/qwen3-vl-235b-a22b-thinking | $0.4000 | $4.0000 |
| dashscope/qwen3-vl-32b-instruct | $0.1600 | $0.6400 |
| dashscope/qwen3-vl-32b-thinking | $0.1600 | $2.8700 |
| dashscope/qwq-plus | $0.8000 | $2.4000 |

## Databricks — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| databricks/databricks-claude-3-7-sonnet | $3.0000 | $15.0000 |
| databricks/databricks-claude-haiku-4-5 | $1.0000 | $5.0000 |
| databricks/databricks-claude-opus-4 | $15.0000 | $75.0000 |
| databricks/databricks-claude-opus-4-1 | $15.0000 | $75.0000 |
| databricks/databricks-claude-opus-4-5 | $5.0000 | $25.0000 |
| databricks/databricks-claude-sonnet-4 | $3.0000 | $15.0000 |
| databricks/databricks-claude-sonnet-4-1 | $3.0000 | $15.0000 |
| databricks/databricks-claude-sonnet-4-5 | $3.0000 | $15.0000 |
| databricks/databricks-gemini-2-5-flash | $0.3000 | $2.5000 |
| databricks/databricks-gemini-2-5-pro | $1.2500 | $10.0000 |
| databricks/databricks-gemma-3-12b | $0.1500 | $0.5000 |
| databricks/databricks-gpt-5 | $1.2500 | $10.0000 |
| databricks/databricks-gpt-5-1 | $1.2500 | $10.0000 |
| databricks/databricks-gpt-5-mini | $0.2500 | $2.0000 |
| databricks/databricks-gpt-5-nano | $0.0500 | $0.4000 |
| databricks/databricks-gpt-oss-120b | $0.1500 | $0.6000 |
| databricks/databricks-gpt-oss-20b | $0.0700 | $0.3000 |
| databricks/databricks-llama-2-70b-chat | $0.5000 | $1.5000 |
| databricks/databricks-llama-4-maverick | $0.5000 | $1.5000 |
| databricks/databricks-meta-llama-3-1-405b-instruct | $5.0000 | $15.0000 |
| databricks/databricks-meta-llama-3-1-8b-instruct | $0.1500 | $0.4500 |
| databricks/databricks-meta-llama-3-3-70b-instruct | $0.5000 | $1.5000 |
| databricks/databricks-meta-llama-3-70b-instruct | $1.0000 | $3.0000 |
| databricks/databricks-mixtral-8x7b-instruct | $0.5000 | $1.0000 |
| databricks/databricks-mpt-30b-instruct | $1.0000 | $1.0000 |
| databricks/databricks-mpt-7b-instruct | $0.5000 | $0.0000 |

## Databricks — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| databricks/databricks-bge-large-en | $0.1000 | $0.0000 |
| databricks/databricks-gte-large-en | $0.1300 | $0.0000 |

## Dataforseo — search (per 1M queries)

| Model | Input | Output |
|-------|-------|--------|
| dataforseo/search | $3000.0000 | $0.0000 |

## DeepInfra — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| deepinfra/Gryphe/MythoMax-L2-13b | $0.0800 | $0.0900 |
| deepinfra/NousResearch/Hermes-3-Llama-3.1-405B | $1.0000 | $1.0000 |
| deepinfra/NousResearch/Hermes-3-Llama-3.1-70B | $0.3000 | $0.3000 |
| deepinfra/Qwen/QwQ-32B | $0.1500 | $0.4000 |
| deepinfra/Qwen/Qwen2.5-72B-Instruct | $0.1200 | $0.3900 |
| deepinfra/Qwen/Qwen2.5-7B-Instruct | $0.0400 | $0.1000 |
| deepinfra/Qwen/Qwen2.5-VL-32B-Instruct | $0.2000 | $0.6000 |
| deepinfra/Qwen/Qwen3-14B | $0.0600 | $0.2400 |
| deepinfra/Qwen/Qwen3-235B-A22B | $0.1800 | $0.5400 |
| deepinfra/Qwen/Qwen3-235B-A22B-Instruct-2507 | $0.0900 | $0.6000 |
| deepinfra/Qwen/Qwen3-235B-A22B-Thinking-2507 | $0.3000 | $2.9000 |
| deepinfra/Qwen/Qwen3-30B-A3B | $0.0800 | $0.2900 |
| deepinfra/Qwen/Qwen3-32B | $0.1000 | $0.2800 |
| deepinfra/Qwen/Qwen3-Coder-480B-A35B-Instruct | $0.4000 | $1.6000 |
| deepinfra/Qwen/Qwen3-Coder-480B-A35B-Instruct-Turbo | $0.2900 | $1.2000 |
| deepinfra/Qwen/Qwen3-Next-80B-A3B-Instruct | $0.1400 | $1.4000 |
| deepinfra/Qwen/Qwen3-Next-80B-A3B-Thinking | $0.1400 | $1.4000 |
| deepinfra/Sao10K/L3-8B-Lunaris-v1-Turbo | $0.0400 | $0.0500 |
| deepinfra/Sao10K/L3.1-70B-Euryale-v2.2 | $0.6500 | $0.7500 |
| deepinfra/Sao10K/L3.3-70B-Euryale-v2.3 | $0.6500 | $0.7500 |
| deepinfra/allenai/olmOCR-7B-0725-FP8 | $0.2700 | $1.5000 |
| deepinfra/anthropic/claude-3-7-sonnet-latest | $3.3000 | $16.5000 |
| deepinfra/anthropic/claude-4-opus | $16.5000 | $82.5000 |
| deepinfra/anthropic/claude-4-sonnet | $3.3000 | $16.5000 |
| deepinfra/deepseek-ai/DeepSeek-R1 | $0.7000 | $2.4000 |
| deepinfra/deepseek-ai/DeepSeek-R1-0528 | $0.5000 | $2.1500 |
| deepinfra/deepseek-ai/DeepSeek-R1-0528-Turbo | $1.0000 | $3.0000 |
| deepinfra/deepseek-ai/DeepSeek-R1-Distill-Llama-70B | $0.2000 | $0.6000 |
| deepinfra/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B | $0.2700 | $0.2700 |
| deepinfra/deepseek-ai/DeepSeek-R1-Turbo | $1.0000 | $3.0000 |
| deepinfra/deepseek-ai/DeepSeek-V3 | $0.3800 | $0.8900 |
| deepinfra/deepseek-ai/DeepSeek-V3-0324 | $0.2500 | $0.8800 |
| deepinfra/deepseek-ai/DeepSeek-V3.1 | $0.2700 | $1.0000 |
| deepinfra/deepseek-ai/DeepSeek-V3.1-Terminus | $0.2700 | $1.0000 |
| deepinfra/google/gemini-2.0-flash-001 | $0.1000 | $0.4000 |
| deepinfra/google/gemini-2.5-flash | $0.3000 | $2.5000 |
| deepinfra/google/gemini-2.5-pro | $1.2500 | $10.0000 |
| deepinfra/google/gemma-3-12b-it | $0.0500 | $0.1000 |
| deepinfra/google/gemma-3-27b-it | $0.0900 | $0.1600 |
| deepinfra/google/gemma-3-4b-it | $0.0400 | $0.0800 |
| deepinfra/meta-llama/Llama-3.2-11B-Vision-Instruct | $0.0490 | $0.0490 |
| deepinfra/meta-llama/Llama-3.2-3B-Instruct | $0.0200 | $0.0200 |
| deepinfra/meta-llama/Llama-3.3-70B-Instruct | $0.2300 | $0.4000 |
| deepinfra/meta-llama/Llama-3.3-70B-Instruct-Turbo | $0.1300 | $0.3900 |
| deepinfra/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8 | $0.1500 | $0.6000 |
| deepinfra/meta-llama/Llama-4-Scout-17B-16E-Instruct | $0.0800 | $0.3000 |
| deepinfra/meta-llama/Llama-Guard-3-8B | $0.0550 | $0.0550 |
| deepinfra/meta-llama/Llama-Guard-4-12B | $0.1800 | $0.1800 |
| deepinfra/meta-llama/Meta-Llama-3-8B-Instruct | $0.0300 | $0.0600 |
| deepinfra/meta-llama/Meta-Llama-3.1-70B-Instruct | $0.4000 | $0.4000 |
| deepinfra/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo | $0.1000 | $0.2800 |
| deepinfra/meta-llama/Meta-Llama-3.1-8B-Instruct | $0.0300 | $0.0500 |
| deepinfra/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo | $0.0200 | $0.0300 |
| deepinfra/microsoft/WizardLM-2-8x22B | $0.4800 | $0.4800 |
| deepinfra/microsoft/phi-4 | $0.0700 | $0.1400 |
| deepinfra/mistralai/Mistral-Nemo-Instruct-2407 | $0.0200 | $0.0400 |
| deepinfra/mistralai/Mistral-Small-24B-Instruct-2501 | $0.0500 | $0.0800 |
| deepinfra/mistralai/Mistral-Small-3.2-24B-Instruct-2506 | $0.0750 | $0.2000 |
| deepinfra/mistralai/Mixtral-8x7B-Instruct-v0.1 | $0.4000 | $0.4000 |
| deepinfra/moonshotai/Kimi-K2-Instruct | $0.5000 | $2.0000 |
| deepinfra/moonshotai/Kimi-K2-Instruct-0905 | $0.5000 | $2.0000 |
| deepinfra/nvidia/Llama-3.1-Nemotron-70B-Instruct | $0.6000 | $0.6000 |
| deepinfra/nvidia/Llama-3.3-Nemotron-Super-49B-v1.5 | $0.1000 | $0.4000 |
| deepinfra/nvidia/NVIDIA-Nemotron-Nano-9B-v2 | $0.0400 | $0.1600 |
| deepinfra/openai/gpt-oss-120b | $0.0500 | $0.4500 |
| deepinfra/openai/gpt-oss-20b | $0.0400 | $0.1500 |
| deepinfra/zai-org/GLM-4.5 | $0.4000 | $1.6000 |

## DeepSeek — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| deepseek-chat | $0.2800 | $0.4200 |
| deepseek-reasoner | $0.2800 | $0.4200 |
| deepseek/deepseek-chat | $0.2800 | $0.4200 |
| deepseek/deepseek-coder | $0.1400 | $0.2800 |
| deepseek/deepseek-r1 | $0.5500 | $2.1900 |
| deepseek/deepseek-reasoner | $0.2800 | $0.4200 |
| deepseek/deepseek-v3 | $0.2700 | $1.1000 |
| deepseek/deepseek-v3.2 | $0.2800 | $0.4000 |

## Deepgram — audio_transcription (per 1M seconds)

| Model | Input | Output |
|-------|-------|--------|
| deepgram/base | $208.3300 | $0.0000 |
| deepgram/base-conversationalai | $208.3300 | $0.0000 |
| deepgram/base-finance | $208.3300 | $0.0000 |
| deepgram/base-general | $208.3300 | $0.0000 |
| deepgram/base-meeting | $208.3300 | $0.0000 |
| deepgram/base-phonecall | $208.3300 | $0.0000 |
| deepgram/base-video | $208.3300 | $0.0000 |
| deepgram/base-voicemail | $208.3300 | $0.0000 |
| deepgram/enhanced | $241.6700 | $0.0000 |
| deepgram/enhanced-finance | $241.6700 | $0.0000 |
| deepgram/enhanced-general | $241.6700 | $0.0000 |
| deepgram/enhanced-meeting | $241.6700 | $0.0000 |
| deepgram/enhanced-phonecall | $241.6700 | $0.0000 |
| deepgram/nova | $71.6700 | $0.0000 |
| deepgram/nova-2 | $71.6700 | $0.0000 |
| deepgram/nova-2-atc | $71.6700 | $0.0000 |
| deepgram/nova-2-automotive | $71.6700 | $0.0000 |
| deepgram/nova-2-conversationalai | $71.6700 | $0.0000 |
| deepgram/nova-2-drivethru | $71.6700 | $0.0000 |
| deepgram/nova-2-finance | $71.6700 | $0.0000 |
| deepgram/nova-2-general | $71.6700 | $0.0000 |
| deepgram/nova-2-meeting | $71.6700 | $0.0000 |
| deepgram/nova-2-phonecall | $71.6700 | $0.0000 |
| deepgram/nova-2-video | $71.6700 | $0.0000 |
| deepgram/nova-2-voicemail | $71.6700 | $0.0000 |
| deepgram/nova-3 | $71.6700 | $0.0000 |
| deepgram/nova-3-general | $71.6700 | $0.0000 |
| deepgram/nova-3-medical | $86.6700 | $0.0000 |
| deepgram/nova-general | $71.6700 | $0.0000 |
| deepgram/nova-phonecall | $71.6700 | $0.0000 |
| deepgram/whisper | $100.0000 | $0.0000 |
| deepgram/whisper-base | $100.0000 | $0.0000 |
| deepgram/whisper-large | $100.0000 | $0.0000 |
| deepgram/whisper-medium | $100.0000 | $0.0000 |
| deepgram/whisper-small | $100.0000 | $0.0000 |
| deepgram/whisper-tiny | $100.0000 | $0.0000 |

## Elevenlabs — audio_speech (per 1M characters)

| Model | Input | Output |
|-------|-------|--------|
| elevenlabs/eleven_multilingual_v2 | $180.0000 | $0.0000 |
| elevenlabs/eleven_v3 | $180.0000 | $0.0000 |

## Elevenlabs — audio_transcription (per 1M seconds)

| Model | Input | Output |
|-------|-------|--------|
| elevenlabs/scribe_v1 | $61.1000 | $0.0000 |
| elevenlabs/scribe_v1_experimental | $61.1000 | $0.0000 |

## Fal Ai — image_generation (per 1M images)

| Model | Input | Output |
|-------|-------|--------|
| fal_ai/bria/text-to-image/3.2 | $0.0000 | $39800.0000 |
| fal_ai/fal-ai/bytedance/dreamina/v3.1/text-to-image | $0.0000 | $30000.0000 |
| fal_ai/fal-ai/bytedance/seedream/v3/text-to-image | $0.0000 | $30000.0000 |
| fal_ai/fal-ai/flux-pro/v1.1 | $0.0000 | $40000.0000 |
| fal_ai/fal-ai/flux-pro/v1.1-ultra | $0.0000 | $60000.0000 |
| fal_ai/fal-ai/flux/schnell | $0.0000 | $3000.0000 |
| fal_ai/fal-ai/ideogram/v3 | $0.0000 | $60000.0000 |
| fal_ai/fal-ai/imagen4/preview | $0.0000 | $39800.0000 |
| fal_ai/fal-ai/imagen4/preview/fast | $0.0000 | $20000.0000 |
| fal_ai/fal-ai/imagen4/preview/ultra | $0.0000 | $60000.0000 |
| fal_ai/fal-ai/recraft/v3/text-to-image | $0.0000 | $39800.0000 |
| fal_ai/fal-ai/stable-diffusion-v35-medium | $0.0000 | $39800.0000 |

## Fireworks — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| fireworks_ai/accounts/fireworks/models/chronos-hermes-13b-v2 | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/code-llama-13b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/code-llama-13b-instruct | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/code-llama-13b-python | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/code-llama-34b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/code-llama-34b-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/code-llama-34b-python | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/code-llama-70b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/code-llama-70b-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/code-llama-70b-python | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/code-llama-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/code-llama-7b-instruct | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/code-llama-7b-python | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/code-qwen-1p5-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/codegemma-2b | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/codegemma-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/cogito-671b-v2-p1 | $1.2000 | $1.2000 |
| fireworks_ai/accounts/fireworks/models/cogito-v1-preview-llama-3b | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/cogito-v1-preview-llama-70b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/cogito-v1-preview-llama-8b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/cogito-v1-preview-qwen-14b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/cogito-v1-preview-qwen-32b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/dbrx-instruct | $1.2000 | $1.2000 |
| fireworks_ai/accounts/fireworks/models/deepseek-coder-1b-base | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/deepseek-coder-33b-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/deepseek-coder-7b-base | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/deepseek-coder-7b-base-v1p5 | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/deepseek-coder-7b-instruct-v1p5 | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/deepseek-coder-v2-instruct | $1.2000 | $1.2000 |
| fireworks_ai/accounts/fireworks/models/deepseek-coder-v2-lite-base | $0.5000 | $0.5000 |
| fireworks_ai/accounts/fireworks/models/deepseek-coder-v2-lite-instruct | $0.5000 | $0.5000 |
| fireworks_ai/accounts/fireworks/models/deepseek-prover-v2 | $1.2000 | $1.2000 |
| fireworks_ai/accounts/fireworks/models/deepseek-r1 | $3.0000 | $8.0000 |
| fireworks_ai/accounts/fireworks/models/deepseek-r1-0528 | $3.0000 | $8.0000 |
| fireworks_ai/accounts/fireworks/models/deepseek-r1-0528-distill-qwen3-8b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/deepseek-r1-basic | $0.5500 | $2.1900 |
| fireworks_ai/accounts/fireworks/models/deepseek-r1-distill-llama-70b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/deepseek-r1-distill-llama-8b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/deepseek-r1-distill-qwen-14b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/deepseek-r1-distill-qwen-1p5b | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/deepseek-r1-distill-qwen-32b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/deepseek-r1-distill-qwen-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/deepseek-v2-lite-chat | $0.5000 | $0.5000 |
| fireworks_ai/accounts/fireworks/models/deepseek-v2p5 | $1.2000 | $1.2000 |
| fireworks_ai/accounts/fireworks/models/deepseek-v3 | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/deepseek-v3-0324 | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/deepseek-v3p1 | $0.5600 | $1.6800 |
| fireworks_ai/accounts/fireworks/models/deepseek-v3p1-terminus | $0.5600 | $1.6800 |
| fireworks_ai/accounts/fireworks/models/deepseek-v3p2 | $0.5600 | $1.6800 |
| fireworks_ai/accounts/fireworks/models/devstral-small-2505 | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/dobby-mini-unhinged-plus-llama-3-1-8b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/dobby-unhinged-llama-3-3-70b-new | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/dolphin-2-9-2-qwen2-72b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/dolphin-2p6-mixtral-8x7b | $0.5000 | $0.5000 |
| fireworks_ai/accounts/fireworks/models/ernie-4p5-21b-a3b-pt | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/ernie-4p5-300b-a47b-pt | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/fare-20b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/firefunction-v1 | $0.5000 | $0.5000 |
| fireworks_ai/accounts/fireworks/models/firefunction-v2 | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/firellava-13b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/firesearch-ocr-v6 | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/flux-1-dev | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/flux-1-dev-controlnet-union | $0.0010 | $0.0010 |
| fireworks_ai/accounts/fireworks/models/flux-1-schnell | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/gemma-2b-it | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/gemma-3-27b-it | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/gemma-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/gemma-7b-it | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/gemma2-9b-it | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/glm-4p5 | $0.5500 | $2.1900 |
| fireworks_ai/accounts/fireworks/models/glm-4p5-air | $0.2200 | $0.8800 |
| fireworks_ai/accounts/fireworks/models/glm-4p5v | $1.2000 | $1.2000 |
| fireworks_ai/accounts/fireworks/models/glm-4p6 | $0.5500 | $2.1900 |
| fireworks_ai/accounts/fireworks/models/glm-4p7 | $0.6000 | $2.2000 |
| fireworks_ai/accounts/fireworks/models/gpt-oss-120b | $0.1500 | $0.6000 |
| fireworks_ai/accounts/fireworks/models/gpt-oss-20b | $0.0500 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/gpt-oss-safeguard-120b | $1.2000 | $1.2000 |
| fireworks_ai/accounts/fireworks/models/gpt-oss-safeguard-20b | $0.5000 | $0.5000 |
| fireworks_ai/accounts/fireworks/models/hermes-2-pro-mistral-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/internvl3-38b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/internvl3-78b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/internvl3-8b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/kat-coder | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/kat-dev-32b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/kat-dev-72b-exp | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/kimi-k2-instruct | $0.6000 | $2.5000 |
| fireworks_ai/accounts/fireworks/models/kimi-k2-instruct-0905 | $0.6000 | $2.5000 |
| fireworks_ai/accounts/fireworks/models/kimi-k2-thinking | $0.6000 | $2.5000 |
| fireworks_ai/accounts/fireworks/models/kimi-k2p5 | $0.6000 | $3.0000 |
| fireworks_ai/accounts/fireworks/models/llama-guard-2-8b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/llama-guard-3-1b | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/llama-guard-3-8b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/llama-v2-13b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/llama-v2-13b-chat | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/llama-v2-70b | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/llama-v2-70b-chat | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/llama-v2-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/llama-v2-7b-chat | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/llama-v3-70b-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/llama-v3-70b-instruct-hf | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/llama-v3-8b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/llama-v3-8b-instruct-hf | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/llama-v3p1-405b-instruct | $3.0000 | $3.0000 |
| fireworks_ai/accounts/fireworks/models/llama-v3p1-405b-instruct-long | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/llama-v3p1-70b-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/llama-v3p1-70b-instruct-1b | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/llama-v3p1-8b-instruct | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/llama-v3p1-nemotron-70b-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/llama-v3p2-11b-vision-instruct | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/llama-v3p2-1b | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/llama-v3p2-1b-instruct | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/llama-v3p2-3b | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/llama-v3p2-3b-instruct | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/llama-v3p2-90b-vision-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/llama-v3p3-70b-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/llama4-maverick-instruct-basic | $0.2200 | $0.8800 |
| fireworks_ai/accounts/fireworks/models/llama4-scout-instruct-basic | $0.1500 | $0.6000 |
| fireworks_ai/accounts/fireworks/models/llamaguard-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/llava-yi-34b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/minimax-m1-80k | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/minimax-m2 | $0.3000 | $1.2000 |
| fireworks_ai/accounts/fireworks/models/minimax-m2p1 | $0.3000 | $1.2000 |
| fireworks_ai/accounts/fireworks/models/ministral-3-14b-instruct-2512 | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/ministral-3-3b-instruct-2512 | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/ministral-3-8b-instruct-2512 | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/mistral-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/mistral-7b-instruct-4k | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/mistral-7b-instruct-v0p2 | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/mistral-7b-instruct-v3 | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/mistral-7b-v0p2 | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/mistral-large-3-fp8 | $1.2000 | $1.2000 |
| fireworks_ai/accounts/fireworks/models/mistral-nemo-base-2407 | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/mistral-nemo-instruct-2407 | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/mistral-small-24b-instruct-2501 | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/mixtral-8x22b | $1.2000 | $1.2000 |
| fireworks_ai/accounts/fireworks/models/mixtral-8x22b-instruct | $1.2000 | $1.2000 |
| fireworks_ai/accounts/fireworks/models/mixtral-8x22b-instruct-hf | $1.2000 | $1.2000 |
| fireworks_ai/accounts/fireworks/models/mixtral-8x7b | $0.5000 | $0.5000 |
| fireworks_ai/accounts/fireworks/models/mixtral-8x7b-instruct | $0.5000 | $0.5000 |
| fireworks_ai/accounts/fireworks/models/mixtral-8x7b-instruct-hf | $0.5000 | $0.5000 |
| fireworks_ai/accounts/fireworks/models/mythomax-l2-13b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/nemotron-nano-v2-12b-vl | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/nous-capybara-7b-v1p9 | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/nous-hermes-2-mixtral-8x7b-dpo | $0.5000 | $0.5000 |
| fireworks_ai/accounts/fireworks/models/nous-hermes-2-yi-34b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/nous-hermes-llama2-13b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/nous-hermes-llama2-70b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/nous-hermes-llama2-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/nvidia-nemotron-nano-12b-v2 | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/nvidia-nemotron-nano-9b-v2 | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/openchat-3p5-0106-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/openhermes-2-mistral-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/openhermes-2p5-mistral-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/openorca-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/phi-2-3b | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/phi-3-mini-128k-instruct | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/phi-3-vision-128k-instruct | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/phind-code-llama-34b-python-v1 | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/phind-code-llama-34b-v1 | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/phind-code-llama-34b-v2 | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/pythia-12b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwen-qwq-32b-preview | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen-v2p5-14b-instruct | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwen-v2p5-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwen1p5-72b-chat | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen2-72b-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen2-7b-instruct | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwen2-vl-2b-instruct | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/qwen2-vl-72b-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen2-vl-7b-instruct | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-0p5b-instruct | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-14b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-1p5b-instruct | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-32b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-32b-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-72b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-72b-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-7b-instruct | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-0p5b | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-0p5b-instruct | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-14b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-14b-instruct | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-1p5b | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-1p5b-instruct | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-32b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-32b-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-32b-instruct-128k | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-32b-instruct-32k-rope | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-32b-instruct-64k | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-3b | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-3b-instruct | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-7b-instruct | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-math-72b-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-vl-32b-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-vl-3b-instruct | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-vl-72b-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen2p5-vl-7b-instruct | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwen3-0p6b | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/qwen3-14b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwen3-1p7b | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/qwen3-1p7b-fp8-draft | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/qwen3-1p7b-fp8-draft-131072 | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/qwen3-1p7b-fp8-draft-40960 | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/qwen3-235b-a22b | $0.2200 | $0.8800 |
| fireworks_ai/accounts/fireworks/models/qwen3-235b-a22b-instruct-2507 | $0.2200 | $0.8800 |
| fireworks_ai/accounts/fireworks/models/qwen3-235b-a22b-thinking-2507 | $0.2200 | $0.8800 |
| fireworks_ai/accounts/fireworks/models/qwen3-30b-a3b | $0.1500 | $0.6000 |
| fireworks_ai/accounts/fireworks/models/qwen3-30b-a3b-instruct-2507 | $0.5000 | $0.5000 |
| fireworks_ai/accounts/fireworks/models/qwen3-30b-a3b-thinking-2507 | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen3-32b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen3-4b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwen3-4b-instruct-2507 | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwen3-8b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwen3-coder-30b-a3b-instruct | $0.1500 | $0.6000 |
| fireworks_ai/accounts/fireworks/models/qwen3-coder-480b-a35b-instruct | $0.4500 | $1.8000 |
| fireworks_ai/accounts/fireworks/models/qwen3-coder-480b-instruct-bf16 | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen3-next-80b-a3b-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen3-next-80b-a3b-thinking | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen3-vl-235b-a22b-instruct | $0.2200 | $0.8800 |
| fireworks_ai/accounts/fireworks/models/qwen3-vl-235b-a22b-thinking | $0.2200 | $0.8800 |
| fireworks_ai/accounts/fireworks/models/qwen3-vl-30b-a3b-instruct | $0.1500 | $0.6000 |
| fireworks_ai/accounts/fireworks/models/qwen3-vl-30b-a3b-thinking | $0.1500 | $0.6000 |
| fireworks_ai/accounts/fireworks/models/qwen3-vl-32b-instruct | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/qwen3-vl-8b-instruct | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/qwq-32b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/rolm-ocr | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/snorkel-mistral-7b-pairrm-dpo | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/stablecode-3b | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/starcoder-16b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/starcoder-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/starcoder2-15b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/starcoder2-3b | $0.1000 | $0.1000 |
| fireworks_ai/accounts/fireworks/models/starcoder2-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/toppy-m-7b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/yi-34b | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/yi-34b-200k-capybara | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/yi-34b-chat | $0.9000 | $0.9000 |
| fireworks_ai/accounts/fireworks/models/yi-6b | $0.2000 | $0.2000 |
| fireworks_ai/accounts/fireworks/models/yi-large | $3.0000 | $3.0000 |
| fireworks_ai/accounts/fireworks/models/zephyr-7b-beta | $0.2000 | $0.2000 |
| fireworks_ai/glm-4p7 | $0.6000 | $2.2000 |
| fireworks_ai/kimi-k2p5 | $0.6000 | $3.0000 |
| fireworks_ai/minimax-m2p1 | $0.3000 | $1.2000 |

## Fireworks — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| fireworks_ai/accounts/fireworks/models/ | $0.1000 | $0.0000 |

## Fireworks — unspecified (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| fireworks-ai-4.1b-to-16b | $0.2000 | $0.2000 |
| fireworks-ai-56b-to-176b | $1.2000 | $1.2000 |
| fireworks-ai-above-16b | $0.9000 | $0.9000 |
| fireworks-ai-moe-up-to-56b | $0.5000 | $0.5000 |
| fireworks-ai-up-to-4b | $0.2000 | $0.2000 |

## Fireworks Ai-Embedding-Models — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| fireworks_ai/WhereIsAI/UAE-Large-V1 | $0.0160 | $0.0000 |
| fireworks_ai/nomic-ai/nomic-embed-text-v1 | $0.0080 | $0.0000 |
| fireworks_ai/nomic-ai/nomic-embed-text-v1.5 | $0.0080 | $0.0000 |
| fireworks_ai/thenlper/gte-base | $0.0080 | $0.0000 |
| fireworks_ai/thenlper/gte-large | $0.0160 | $0.0000 |

## Fireworks Ai-Embedding-Models — unspecified (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| fireworks-ai-embedding-150m-to-350m | $0.0160 | $0.0000 |
| fireworks-ai-embedding-up-to-150m | $0.0080 | $0.0000 |

## FriendliAI — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| friendliai/meta-llama-3.1-70b-instruct | $0.6000 | $0.6000 |
| friendliai/meta-llama-3.1-8b-instruct | $0.1000 | $0.1000 |

## Gmi — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| gmi/MiniMaxAI/MiniMax-M2.1 | $0.3000 | $1.2000 |
| gmi/Qwen/Qwen3-VL-235B-A22B-Instruct-FP8 | $0.3000 | $1.4000 |
| gmi/anthropic/claude-opus-4 | $15.0000 | $75.0000 |
| gmi/anthropic/claude-opus-4.5 | $5.0000 | $25.0000 |
| gmi/anthropic/claude-sonnet-4 | $3.0000 | $15.0000 |
| gmi/anthropic/claude-sonnet-4.5 | $3.0000 | $15.0000 |
| gmi/deepseek-ai/DeepSeek-V3-0324 | $0.2800 | $0.8800 |
| gmi/deepseek-ai/DeepSeek-V3.2 | $0.2800 | $0.4000 |
| gmi/google/gemini-3-flash-preview | $0.5000 | $3.0000 |
| gmi/google/gemini-3-pro-preview | $2.0000 | $12.0000 |
| gmi/moonshotai/Kimi-K2-Thinking | $0.8000 | $1.2000 |
| gmi/openai/gpt-4o | $2.5000 | $10.0000 |
| gmi/openai/gpt-4o-mini | $0.1500 | $0.6000 |
| gmi/openai/gpt-5 | $1.2500 | $10.0000 |
| gmi/openai/gpt-5.1 | $1.2500 | $10.0000 |
| gmi/openai/gpt-5.2 | $1.7500 | $14.0000 |
| gmi/zai-org/GLM-4.7-FP8 | $0.4000 | $2.0000 |

## Google — audio_speech (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| gemini-2.5-flash-preview-tts | $0.3000 | $0.0000 |
| gemini/gemini-2.5-flash-preview-tts | $0.3000 | $0.0000 |

## Google — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| gemini-2.5-flash-native-audio-latest | $0.3000 | $2.5000 |
| gemini-2.5-flash-native-audio-preview-09-2025 | $0.3000 | $2.5000 |
| gemini-2.5-flash-native-audio-preview-12-2025 | $0.3000 | $2.5000 |
| gemini-3.1-flash-live-preview | $0.7500 | $4.5000 |
| gemini-exp-1206 | $0.3000 | $2.5000 |
| gemini-flash-latest | $0.3000 | $2.5000 |
| gemini-flash-lite-latest | $0.1000 | $0.4000 |
| gemini-pro-latest | $1.2500 | $10.0000 |
| gemini/gemini-2.0-flash | $0.1000 | $0.4000 |
| gemini/gemini-2.0-flash-001 | $0.1000 | $0.4000 |
| gemini/gemini-2.0-flash-lite | $0.0750 | $0.3000 |
| gemini/gemini-2.0-flash-lite-001 | $0.0750 | $0.3000 |
| gemini/gemini-2.5-computer-use-preview-10-2025 | $1.2500 | $10.0000 |
| gemini/gemini-2.5-flash | $0.3000 | $2.5000 |
| gemini/gemini-2.5-flash-lite | $0.1000 | $0.4000 |
| gemini/gemini-2.5-flash-lite-preview-06-17 | $0.1000 | $0.4000 |
| gemini/gemini-2.5-flash-lite-preview-09-2025 | $0.1000 | $0.4000 |
| gemini/gemini-2.5-flash-native-audio-latest | $0.3000 | $2.5000 |
| gemini/gemini-2.5-flash-native-audio-preview-09-2025 | $0.3000 | $2.5000 |
| gemini/gemini-2.5-flash-native-audio-preview-12-2025 | $0.3000 | $2.5000 |
| gemini/gemini-2.5-flash-preview-09-2025 | $0.3000 | $2.5000 |
| gemini/gemini-2.5-pro | $1.2500 | $10.0000 |
| gemini/gemini-2.5-pro-preview-tts | $1.2500 | $10.0000 |
| gemini/gemini-3-flash-preview | $0.5000 | $3.0000 |
| gemini/gemini-3-pro-preview | $2.0000 | $12.0000 |
| gemini/gemini-3.1-flash-lite-preview | $0.2500 | $1.5000 |
| gemini/gemini-3.1-flash-live-preview | $0.7500 | $4.5000 |
| gemini/gemini-3.1-pro-preview | $2.0000 | $12.0000 |
| gemini/gemini-3.1-pro-preview-customtools | $2.0000 | $12.0000 |
| gemini/gemini-flash-latest | $0.3000 | $2.5000 |
| gemini/gemini-flash-lite-latest | $0.1000 | $0.4000 |
| gemini/gemini-gemma-2-27b-it | $0.3500 | $1.0500 |
| gemini/gemini-gemma-2-9b-it | $0.3500 | $1.0500 |
| gemini/gemini-pro-latest | $1.2500 | $10.0000 |
| gemini/gemini-robotics-er-1.5-preview | $0.3000 | $2.5000 |

## Google — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| gemini/gemini-1.5-flash | $0.0750 | $0.0000 |
| gemini/gemini-embedding-001 | $0.1500 | $0.0000 |
| gemini/gemini-embedding-2-preview | $0.2000 | $0.0000 |

## Google — image_generation (per 1M images)

| Model | Input | Output |
|-------|-------|--------|
| gemini-2.0-flash-exp-image-generation | $0.0000 | $39000.0000 |
| gemini/deep-research-pro-preview-12-2025 | $1100.0000 | $134000.0000 |
| gemini/gemini-2.0-flash-exp-image-generation | $0.0000 | $39000.0000 |
| gemini/gemini-2.5-flash-image | $0.0000 | $39000.0000 |
| gemini/gemini-3-pro-image-preview | $1100.0000 | $134000.0000 |
| gemini/gemini-3.1-flash-image-preview | $0.0000 | $45000.0000 |
| gemini/imagen-3.0-fast-generate-001 | $0.0000 | $20000.0000 |
| gemini/imagen-3.0-generate-001 | $0.0000 | $40000.0000 |
| gemini/imagen-3.0-generate-002 | $0.0000 | $40000.0000 |
| gemini/imagen-4.0-fast-generate-001 | $0.0000 | $20000.0000 |
| gemini/imagen-4.0-generate-001 | $0.0000 | $40000.0000 |
| gemini/imagen-4.0-ultra-generate-001 | $0.0000 | $60000.0000 |

## Google — realtime (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| gemini/gemini-live-2.5-flash-preview-native-audio-09-2025 | $0.3000 | $2.0000 |

## Google — video_generation (per 1M seconds)

| Model | Input | Output |
|-------|-------|--------|
| gemini/veo-2.0-generate-001 | $0.0000 | $350000.0000 |
| gemini/veo-3.1-fast-generate-001 | $0.0000 | $150000.0000 |
| gemini/veo-3.1-fast-generate-preview | $0.0000 | $150000.0000 |
| gemini/veo-3.1-generate-001 | $0.0000 | $400000.0000 |
| gemini/veo-3.1-generate-preview | $0.0000 | $400000.0000 |
| gemini/veo-3.1-lite-generate-preview | $0.0000 | $50000.0000 |

## Google (Vertex AI21) — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| vertex_ai/jamba-1.5 | $0.2000 | $0.4000 |
| vertex_ai/jamba-1.5-large | $2.0000 | $8.0000 |
| vertex_ai/jamba-1.5-large@001 | $2.0000 | $8.0000 |
| vertex_ai/jamba-1.5-mini | $0.2000 | $0.4000 |
| vertex_ai/jamba-1.5-mini@001 | $0.2000 | $0.4000 |

## Google (Vertex Anthropic) — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| vertex_ai/claude-3-5-haiku | $1.0000 | $5.0000 |
| vertex_ai/claude-3-5-haiku@20241022 | $1.0000 | $5.0000 |
| vertex_ai/claude-3-5-sonnet | $3.0000 | $15.0000 |
| vertex_ai/claude-3-5-sonnet@20240620 | $3.0000 | $15.0000 |
| vertex_ai/claude-3-7-sonnet@20250219 | $3.0000 | $15.0000 |
| vertex_ai/claude-3-haiku | $0.2500 | $1.2500 |
| vertex_ai/claude-3-haiku@20240307 | $0.2500 | $1.2500 |
| vertex_ai/claude-3-opus | $15.0000 | $75.0000 |
| vertex_ai/claude-3-opus@20240229 | $15.0000 | $75.0000 |
| vertex_ai/claude-3-sonnet | $3.0000 | $15.0000 |
| vertex_ai/claude-3-sonnet@20240229 | $3.0000 | $15.0000 |
| vertex_ai/claude-haiku-4-5 | $1.0000 | $5.0000 |
| vertex_ai/claude-haiku-4-5@20251001 | $1.0000 | $5.0000 |
| vertex_ai/claude-opus-4 | $15.0000 | $75.0000 |
| vertex_ai/claude-opus-4-1 | $15.0000 | $75.0000 |
| vertex_ai/claude-opus-4-1@20250805 | $15.0000 | $75.0000 |
| vertex_ai/claude-opus-4-5 | $5.0000 | $25.0000 |
| vertex_ai/claude-opus-4-5@20251101 | $5.0000 | $25.0000 |
| vertex_ai/claude-opus-4-6 | $5.0000 | $25.0000 |
| vertex_ai/claude-opus-4-6@default | $5.0000 | $25.0000 |
| vertex_ai/claude-opus-4-7 | $5.0000 | $25.0000 |
| vertex_ai/claude-opus-4-7@default | $5.0000 | $25.0000 |
| vertex_ai/claude-opus-4@20250514 | $15.0000 | $75.0000 |
| vertex_ai/claude-sonnet-4 | $3.0000 | $15.0000 |
| vertex_ai/claude-sonnet-4-5 | $3.0000 | $15.0000 |
| vertex_ai/claude-sonnet-4-5@20250929 | $3.0000 | $15.0000 |
| vertex_ai/claude-sonnet-4-6 | $3.0000 | $15.0000 |
| vertex_ai/claude-sonnet-4-6@default | $3.0000 | $15.0000 |
| vertex_ai/claude-sonnet-4@20250514 | $3.0000 | $15.0000 |

## Google (Vertex Mistral) — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| vertex_ai/codestral-2 | $0.3000 | $0.9000 |
| vertex_ai/codestral-2501 | $0.2000 | $0.6000 |
| vertex_ai/codestral-2@001 | $0.3000 | $0.9000 |
| vertex_ai/codestral@2405 | $0.2000 | $0.6000 |
| vertex_ai/codestral@latest | $0.2000 | $0.6000 |
| vertex_ai/mistral-large-2411 | $2.0000 | $6.0000 |
| vertex_ai/mistral-large@2407 | $2.0000 | $6.0000 |
| vertex_ai/mistral-large@2411-001 | $2.0000 | $6.0000 |
| vertex_ai/mistral-large@latest | $2.0000 | $6.0000 |
| vertex_ai/mistral-medium-3 | $0.4000 | $2.0000 |
| vertex_ai/mistral-medium-3@001 | $0.4000 | $2.0000 |
| vertex_ai/mistral-nemo@2407 | $3.0000 | $3.0000 |
| vertex_ai/mistral-nemo@latest | $0.1500 | $0.1500 |
| vertex_ai/mistral-small-2503 | $1.0000 | $3.0000 |
| vertex_ai/mistral-small-2503@001 | $1.0000 | $3.0000 |
| vertex_ai/mistralai/codestral-2 | $0.3000 | $0.9000 |
| vertex_ai/mistralai/codestral-2@001 | $0.3000 | $0.9000 |
| vertex_ai/mistralai/mistral-medium-3 | $0.4000 | $2.0000 |
| vertex_ai/mistralai/mistral-medium-3@001 | $0.4000 | $2.0000 |

## Google (Vertex) — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| gemini-2.0-flash | $0.1000 | $0.4000 |
| gemini-2.0-flash-001 | $0.1500 | $0.6000 |
| gemini-2.0-flash-lite | $0.0750 | $0.3000 |
| gemini-2.0-flash-lite-001 | $0.0750 | $0.3000 |
| gemini-2.5-computer-use-preview-10-2025 | $1.2500 | $10.0000 |
| gemini-2.5-flash | $0.3000 | $2.5000 |
| gemini-2.5-flash-lite | $0.1000 | $0.4000 |
| gemini-2.5-flash-lite-preview-06-17 | $0.1000 | $0.4000 |
| gemini-2.5-flash-lite-preview-09-2025 | $0.1000 | $0.4000 |
| gemini-2.5-flash-preview-09-2025 | $0.3000 | $2.5000 |
| gemini-2.5-pro | $1.2500 | $10.0000 |
| gemini-2.5-pro-preview-tts | $1.2500 | $10.0000 |
| gemini-3-flash-preview | $0.5000 | $3.0000 |
| gemini-3-pro-preview | $2.0000 | $12.0000 |
| gemini-3.1-flash-lite-preview | $0.2500 | $1.5000 |
| gemini-3.1-pro-preview | $2.0000 | $12.0000 |
| gemini-3.1-pro-preview-customtools | $2.0000 | $12.0000 |
| gemini-robotics-er-1.5-preview | $0.3000 | $2.5000 |
| vertex_ai/gemini-3.1-flash-lite-preview | $0.2500 | $1.5000 |

## Google (Vertex) — completion (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| text-unicorn | $10.0000 | $28.0000 |
| text-unicorn@001 | $10.0000 | $28.0000 |

## Google (Vertex) — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| gemini-embedding-001 | $0.1500 | $0.0000 |
| gemini-embedding-2-preview | $0.2000 | $0.0000 |
| multimodalembedding | $0.8000 | $0.0000 |
| multimodalembedding@001 | $0.8000 | $0.0000 |
| text-embedding-004 | $0.1000 | $0.0000 |
| text-embedding-005 | $0.1000 | $0.0000 |
| text-embedding-large-exp-03-07 | $0.1000 | $0.0000 |
| text-embedding-preview-0409 | $0.0062 | $0.0000 |
| text-multilingual-embedding-002 | $0.1000 | $0.0000 |

## Google (Vertex) — image_generation (per 1M images)

| Model | Input | Output |
|-------|-------|--------|
| deep-research-pro-preview-12-2025 | $1100.0000 | $134000.0000 |
| gemini-2.5-flash-image | $0.0000 | $39000.0000 |
| gemini-3-pro-image-preview | $1100.0000 | $134000.0000 |
| gemini-3.1-flash-image-preview | $560.0000 | $67200.0000 |
| vertex_ai/deep-research-pro-preview-12-2025 | $1100.0000 | $134000.0000 |
| vertex_ai/gemini-2.5-flash-image | $0.0000 | $39000.0000 |
| vertex_ai/gemini-3-pro-image-preview | $1100.0000 | $134000.0000 |
| vertex_ai/gemini-3.1-flash-image-preview | $560.0000 | $67200.0000 |
| vertex_ai/imagegeneration@006 | $0.0000 | $20000.0000 |
| vertex_ai/imagen-3.0-capability-001 | $0.0000 | $40000.0000 |
| vertex_ai/imagen-3.0-fast-generate-001 | $0.0000 | $20000.0000 |
| vertex_ai/imagen-3.0-generate-001 | $0.0000 | $40000.0000 |
| vertex_ai/imagen-3.0-generate-002 | $0.0000 | $40000.0000 |
| vertex_ai/imagen-4.0-fast-generate-001 | $0.0000 | $20000.0000 |
| vertex_ai/imagen-4.0-generate-001 | $0.0000 | $40000.0000 |
| vertex_ai/imagen-4.0-ultra-generate-001 | $0.0000 | $60000.0000 |

## Google (Vertex) — realtime (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| gemini-live-2.5-flash-preview-native-audio-09-2025 | $0.3000 | $2.0000 |

## Google Pse — search (per 1M queries)

| Model | Input | Output |
|-------|-------|--------|
| google_pse/search | $5000.0000 | $0.0000 |

## Gradient Ai — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| gradient_ai/anthropic-claude-3-opus | $15.0000 | $75.0000 |
| gradient_ai/anthropic-claude-3.5-haiku | $0.8000 | $4.0000 |
| gradient_ai/anthropic-claude-3.5-sonnet | $3.0000 | $15.0000 |
| gradient_ai/anthropic-claude-3.7-sonnet | $3.0000 | $15.0000 |
| gradient_ai/deepseek-r1-distill-llama-70b | $0.9900 | $0.9900 |
| gradient_ai/llama3-8b-instruct | $0.2000 | $0.2000 |
| gradient_ai/llama3.3-70b-instruct | $0.6500 | $0.6500 |
| gradient_ai/mistral-nemo-instruct-2407 | $0.3000 | $0.3000 |
| gradient_ai/openai-o3 | $2.0000 | $8.0000 |
| gradient_ai/openai-o3-mini | $1.1000 | $4.4000 |

## Groq — audio_speech (per 1M characters)

| Model | Input | Output |
|-------|-------|--------|
| groq/playai-tts | $50.0000 | $0.0000 |

## Groq — audio_transcription (per 1M seconds)

| Model | Input | Output |
|-------|-------|--------|
| groq/whisper-large-v3 | $30.8300 | $0.0000 |
| groq/whisper-large-v3-turbo | $11.1100 | $0.0000 |

## Groq — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| groq/gemma-7b-it | $0.0500 | $0.0800 |
| groq/llama-3.1-8b-instant | $0.0500 | $0.0800 |
| groq/llama-3.3-70b-versatile | $0.5900 | $0.7900 |
| groq/meta-llama/llama-4-maverick-17b-128e-instruct | $0.2000 | $0.6000 |
| groq/meta-llama/llama-4-scout-17b-16e-instruct | $0.1100 | $0.3400 |
| groq/meta-llama/llama-guard-4-12b | $0.2000 | $0.2000 |
| groq/moonshotai/kimi-k2-instruct-0905 | $1.0000 | $3.0000 |
| groq/openai/gpt-oss-120b | $0.1500 | $0.6000 |
| groq/openai/gpt-oss-20b | $0.0750 | $0.3000 |
| groq/openai/gpt-oss-safeguard-20b | $0.0750 | $0.3000 |
| groq/qwen/qwen3-32b | $0.2900 | $0.5900 |

## Hyperbolic — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| hyperbolic/NousResearch/Hermes-3-Llama-3.1-70B | $0.1200 | $0.3000 |
| hyperbolic/Qwen/QwQ-32B | $0.2000 | $0.2000 |
| hyperbolic/Qwen/Qwen2.5-72B-Instruct | $0.1200 | $0.3000 |
| hyperbolic/Qwen/Qwen2.5-Coder-32B-Instruct | $0.1200 | $0.3000 |
| hyperbolic/Qwen/Qwen3-235B-A22B | $2.0000 | $2.0000 |
| hyperbolic/deepseek-ai/DeepSeek-R1 | $0.4000 | $0.4000 |
| hyperbolic/deepseek-ai/DeepSeek-R1-0528 | $0.2500 | $0.2500 |
| hyperbolic/deepseek-ai/DeepSeek-V3 | $0.2000 | $0.2000 |
| hyperbolic/deepseek-ai/DeepSeek-V3-0324 | $0.4000 | $0.4000 |
| hyperbolic/meta-llama/Llama-3.2-3B-Instruct | $0.1200 | $0.3000 |
| hyperbolic/meta-llama/Llama-3.3-70B-Instruct | $0.1200 | $0.3000 |
| hyperbolic/meta-llama/Meta-Llama-3-70B-Instruct | $0.1200 | $0.3000 |
| hyperbolic/meta-llama/Meta-Llama-3.1-405B-Instruct | $0.1200 | $0.3000 |
| hyperbolic/meta-llama/Meta-Llama-3.1-70B-Instruct | $0.1200 | $0.3000 |
| hyperbolic/meta-llama/Meta-Llama-3.1-8B-Instruct | $0.1200 | $0.3000 |
| hyperbolic/moonshotai/Kimi-K2-Instruct | $2.0000 | $2.0000 |

## IBM watsonx — audio_transcription (per 1M seconds)

| Model | Input | Output |
|-------|-------|--------|
| watsonx/whisper-large-v3-turbo | $100.0000 | $100.0000 |

## IBM watsonx — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| watsonx/bigscience/mt0-xxl-13b | $500.0000 | $2000.0000 |
| watsonx/core42/jais-13b-chat | $500.0000 | $2000.0000 |
| watsonx/google/flan-t5-xl-3b | $0.6000 | $0.6000 |
| watsonx/ibm/granite-13b-chat-v2 | $0.6000 | $0.6000 |
| watsonx/ibm/granite-13b-instruct-v2 | $0.6000 | $0.6000 |
| watsonx/ibm/granite-3-3-8b-instruct | $0.2000 | $0.2000 |
| watsonx/ibm/granite-3-8b-instruct | $0.2000 | $0.2000 |
| watsonx/ibm/granite-4-h-small | $0.0600 | $0.2500 |
| watsonx/ibm/granite-guardian-3-2-2b | $0.1000 | $0.1000 |
| watsonx/ibm/granite-guardian-3-3-8b | $0.2000 | $0.2000 |
| watsonx/ibm/granite-ttm-1024-96-r2 | $0.3800 | $0.3800 |
| watsonx/ibm/granite-ttm-1536-96-r2 | $0.3800 | $0.3800 |
| watsonx/ibm/granite-ttm-512-96-r2 | $0.3800 | $0.3800 |
| watsonx/ibm/granite-vision-3-2-2b | $0.1000 | $0.1000 |
| watsonx/meta-llama/llama-3-2-11b-vision-instruct | $0.3500 | $0.3500 |
| watsonx/meta-llama/llama-3-2-1b-instruct | $0.1000 | $0.1000 |
| watsonx/meta-llama/llama-3-2-3b-instruct | $0.1500 | $0.1500 |
| watsonx/meta-llama/llama-3-2-90b-vision-instruct | $2.0000 | $2.0000 |
| watsonx/meta-llama/llama-3-3-70b-instruct | $0.7100 | $0.7100 |
| watsonx/meta-llama/llama-4-maverick-17b | $0.3500 | $1.4000 |
| watsonx/meta-llama/llama-guard-3-11b-vision | $0.3500 | $0.3500 |
| watsonx/mistralai/mistral-large | $3.0000 | $10.0000 |
| watsonx/mistralai/mistral-medium-2505 | $3.0000 | $10.0000 |
| watsonx/mistralai/mistral-small-2503 | $0.1000 | $0.3000 |
| watsonx/mistralai/mistral-small-3-1-24b-instruct-2503 | $0.1000 | $0.3000 |
| watsonx/mistralai/pixtral-12b-2409 | $0.3500 | $0.3500 |
| watsonx/openai/gpt-oss-120b | $0.1500 | $0.6000 |
| watsonx/sdaia/allam-1-13b-instruct | $1.8000 | $1.8000 |

## Lambda AI — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| lambda_ai/deepseek-llama3.3-70b | $0.2000 | $0.6000 |
| lambda_ai/deepseek-r1-0528 | $0.2000 | $0.6000 |
| lambda_ai/deepseek-r1-671b | $0.8000 | $0.8000 |
| lambda_ai/deepseek-v3-0324 | $0.2000 | $0.6000 |
| lambda_ai/hermes3-405b | $0.8000 | $0.8000 |
| lambda_ai/hermes3-70b | $0.1200 | $0.3000 |
| lambda_ai/hermes3-8b | $0.0250 | $0.0400 |
| lambda_ai/lfm-40b | $0.1000 | $0.2000 |
| lambda_ai/lfm-7b | $0.0250 | $0.0400 |
| lambda_ai/llama-4-maverick-17b-128e-instruct-fp8 | $0.0500 | $0.1000 |
| lambda_ai/llama-4-scout-17b-16e-instruct | $0.0500 | $0.1000 |
| lambda_ai/llama3.1-405b-instruct-fp8 | $0.8000 | $0.8000 |
| lambda_ai/llama3.1-70b-instruct-fp8 | $0.1200 | $0.3000 |
| lambda_ai/llama3.1-8b-instruct | $0.0250 | $0.0400 |
| lambda_ai/llama3.1-nemotron-70b-instruct-fp8 | $0.1200 | $0.3000 |
| lambda_ai/llama3.2-11b-vision-instruct | $0.0150 | $0.0250 |
| lambda_ai/llama3.2-3b-instruct | $0.0150 | $0.0250 |
| lambda_ai/llama3.3-70b-instruct-fp8 | $0.1200 | $0.3000 |
| lambda_ai/qwen25-coder-32b-instruct | $0.0500 | $0.1000 |
| lambda_ai/qwen3-32b-fp8 | $0.0500 | $0.1000 |

## Linkup — search (per 1M queries)

| Model | Input | Output |
|-------|-------|--------|
| linkup/search | $5870.0000 | $0.0000 |
| linkup/search-deep | $58670.0000 | $0.0000 |

## Llamagate — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| llamagate/codellama-7b | $0.0600 | $0.1200 |
| llamagate/deepseek-coder-6.7b | $0.0600 | $0.1200 |
| llamagate/deepseek-r1-7b-qwen | $0.0800 | $0.1500 |
| llamagate/deepseek-r1-8b | $0.1000 | $0.2000 |
| llamagate/dolphin3-8b | $0.0800 | $0.1500 |
| llamagate/gemma3-4b | $0.0300 | $0.0800 |
| llamagate/llama-3.1-8b | $0.0300 | $0.0500 |
| llamagate/llama-3.2-3b | $0.0400 | $0.0800 |
| llamagate/llava-7b | $0.1000 | $0.2000 |
| llamagate/mistral-7b-v0.3 | $0.1000 | $0.1500 |
| llamagate/openthinker-7b | $0.0800 | $0.1500 |
| llamagate/qwen2.5-coder-7b | $0.0600 | $0.1200 |
| llamagate/qwen3-8b | $0.0400 | $0.1400 |
| llamagate/qwen3-vl-8b | $0.1500 | $0.5500 |

## Llamagate — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| llamagate/nomic-embed-text | $0.0200 | $0.0000 |
| llamagate/qwen3-embedding-8b | $0.0200 | $0.0000 |

## Minimax — audio_speech (per 1M characters)

| Model | Input | Output |
|-------|-------|--------|
| minimax/speech-02-hd | $100.0000 | $0.0000 |
| minimax/speech-02-turbo | $60.0000 | $0.0000 |
| minimax/speech-2.6-hd | $100.0000 | $0.0000 |
| minimax/speech-2.6-turbo | $60.0000 | $0.0000 |

## Minimax — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| minimax/MiniMax-M2 | $0.3000 | $1.2000 |
| minimax/MiniMax-M2.1 | $0.3000 | $1.2000 |
| minimax/MiniMax-M2.1-lightning | $0.3000 | $2.4000 |
| minimax/MiniMax-M2.5 | $0.3000 | $1.2000 |
| minimax/MiniMax-M2.5-lightning | $0.3000 | $2.4000 |

## Mistral — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| mistral/codestral-2405 | $1.0000 | $3.0000 |
| mistral/codestral-2508 | $0.3000 | $0.9000 |
| mistral/codestral-latest | $1.0000 | $3.0000 |
| mistral/codestral-mamba-latest | $0.2500 | $0.2500 |
| mistral/devstral-2512 | $0.4000 | $2.0000 |
| mistral/devstral-latest | $0.4000 | $2.0000 |
| mistral/devstral-medium-2507 | $0.4000 | $2.0000 |
| mistral/devstral-medium-latest | $0.4000 | $2.0000 |
| mistral/devstral-small-2505 | $0.1000 | $0.3000 |
| mistral/devstral-small-2507 | $0.1000 | $0.3000 |
| mistral/devstral-small-latest | $0.1000 | $0.3000 |
| mistral/labs-devstral-small-2512 | $0.1000 | $0.3000 |
| mistral/magistral-medium-1-2-2509 | $2.0000 | $5.0000 |
| mistral/magistral-medium-2506 | $2.0000 | $5.0000 |
| mistral/magistral-medium-2509 | $2.0000 | $5.0000 |
| mistral/magistral-medium-latest | $2.0000 | $5.0000 |
| mistral/magistral-small-1-2-2509 | $0.5000 | $1.5000 |
| mistral/magistral-small-2506 | $0.5000 | $1.5000 |
| mistral/magistral-small-latest | $0.5000 | $1.5000 |
| mistral/ministral-3-14b-2512 | $0.2000 | $0.2000 |
| mistral/ministral-3-3b-2512 | $0.1000 | $0.1000 |
| mistral/ministral-3-8b-2512 | $0.1500 | $0.1500 |
| mistral/mistral-large-2402 | $4.0000 | $12.0000 |
| mistral/mistral-large-2407 | $3.0000 | $9.0000 |
| mistral/mistral-large-2411 | $2.0000 | $6.0000 |
| mistral/mistral-large-2512 | $0.5000 | $1.5000 |
| mistral/mistral-large-3 | $0.5000 | $1.5000 |
| mistral/mistral-large-latest | $0.5000 | $1.5000 |
| mistral/mistral-medium | $2.7000 | $8.1000 |
| mistral/mistral-medium-2312 | $2.7000 | $8.1000 |
| mistral/mistral-medium-2505 | $0.4000 | $2.0000 |
| mistral/mistral-medium-3-1-2508 | $0.4000 | $2.0000 |
| mistral/mistral-medium-latest | $0.4000 | $2.0000 |
| mistral/mistral-small | $0.1000 | $0.3000 |
| mistral/mistral-small-3-2-2506 | $0.0600 | $0.1800 |
| mistral/mistral-small-latest | $0.0600 | $0.1800 |
| mistral/mistral-tiny | $0.2500 | $0.2500 |
| mistral/open-codestral-mamba | $0.2500 | $0.2500 |
| mistral/open-mistral-7b | $0.2500 | $0.2500 |
| mistral/open-mistral-nemo | $0.3000 | $0.3000 |
| mistral/open-mistral-nemo-2407 | $0.3000 | $0.3000 |
| mistral/open-mixtral-8x22b | $2.0000 | $6.0000 |
| mistral/open-mixtral-8x7b | $0.7000 | $0.7000 |
| mistral/pixtral-12b-2409 | $0.1500 | $0.1500 |
| mistral/pixtral-large-2411 | $2.0000 | $6.0000 |
| mistral/pixtral-large-latest | $2.0000 | $6.0000 |

## Mistral — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| mistral/codestral-embed | $0.1500 | $0.0000 |
| mistral/codestral-embed-2505 | $0.1500 | $0.0000 |
| mistral/mistral-embed | $0.1000 | $0.0000 |

## Mistral — ocr (per 1M pages)

| Model | Input | Output |
|-------|-------|--------|
| mistral/mistral-ocr-2505-completion | $1000.0000 | $0.0000 |
| mistral/mistral-ocr-latest | $1000.0000 | $0.0000 |

## Moonshot — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| moonshot/kimi-k2-0711-preview | $0.6000 | $2.5000 |
| moonshot/kimi-k2-0905-preview | $0.6000 | $2.5000 |
| moonshot/kimi-k2-thinking | $0.6000 | $2.5000 |
| moonshot/kimi-k2-thinking-turbo | $1.1500 | $8.0000 |
| moonshot/kimi-k2-turbo-preview | $1.1500 | $8.0000 |
| moonshot/kimi-k2.5 | $0.6000 | $3.0000 |
| moonshot/kimi-latest | $2.0000 | $5.0000 |
| moonshot/kimi-latest-128k | $2.0000 | $5.0000 |
| moonshot/kimi-latest-32k | $1.0000 | $3.0000 |
| moonshot/kimi-latest-8k | $0.2000 | $2.0000 |
| moonshot/kimi-thinking-preview | $0.6000 | $2.5000 |
| moonshot/moonshot-v1-128k | $2.0000 | $5.0000 |
| moonshot/moonshot-v1-128k-0430 | $2.0000 | $5.0000 |
| moonshot/moonshot-v1-128k-vision-preview | $2.0000 | $5.0000 |
| moonshot/moonshot-v1-32k | $1.0000 | $3.0000 |
| moonshot/moonshot-v1-32k-0430 | $1.0000 | $3.0000 |
| moonshot/moonshot-v1-32k-vision-preview | $1.0000 | $3.0000 |
| moonshot/moonshot-v1-8k | $0.2000 | $2.0000 |
| moonshot/moonshot-v1-8k-0430 | $0.2000 | $2.0000 |
| moonshot/moonshot-v1-8k-vision-preview | $0.2000 | $2.0000 |
| moonshot/moonshot-v1-auto | $2.0000 | $5.0000 |

## Morph — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| morph/morph-v3-fast | $0.8000 | $1.2000 |
| morph/morph-v3-large | $0.9000 | $1.9000 |

## Nebius — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| nebius/NousResearch/Hermes-3-Llama-3.1-405B | $1.0000 | $3.0000 |
| nebius/Qwen/QwQ-32B | $0.1500 | $0.4500 |
| nebius/Qwen/Qwen2-VL-72B-Instruct | $0.1300 | $0.4000 |
| nebius/Qwen/Qwen2-VL-7B-Instruct | $0.0200 | $0.0600 |
| nebius/Qwen/Qwen2.5-32B-Instruct | $0.0600 | $0.2000 |
| nebius/Qwen/Qwen2.5-72B-Instruct | $0.1300 | $0.4000 |
| nebius/Qwen/Qwen2.5-Coder-7B | $0.0100 | $0.0300 |
| nebius/Qwen/Qwen2.5-VL-72B-Instruct | $0.1300 | $0.4000 |
| nebius/Qwen/Qwen3-14B | $0.0800 | $0.2400 |
| nebius/Qwen/Qwen3-235B-A22B | $0.2000 | $0.6000 |
| nebius/Qwen/Qwen3-30B-A3B | $0.1000 | $0.3000 |
| nebius/Qwen/Qwen3-32B | $0.1000 | $0.3000 |
| nebius/Qwen/Qwen3-4B | $0.0800 | $0.2400 |
| nebius/deepseek-ai/DeepSeek-R1 | $0.8000 | $2.4000 |
| nebius/deepseek-ai/DeepSeek-R1-0528 | $0.8000 | $2.4000 |
| nebius/deepseek-ai/DeepSeek-R1-Distill-Llama-70B | $0.2500 | $0.7500 |
| nebius/deepseek-ai/DeepSeek-V3 | $0.5000 | $1.5000 |
| nebius/deepseek-ai/DeepSeek-V3-0324 | $0.5000 | $1.5000 |
| nebius/google/gemma-3-27b-it | $0.0600 | $0.2000 |
| nebius/meta-llama/Llama-3.3-70B-Instruct | $0.1300 | $0.4000 |
| nebius/meta-llama/Llama-Guard-3-8B | $0.0200 | $0.0600 |
| nebius/meta-llama/Meta-Llama-3.1-405B-Instruct | $1.0000 | $3.0000 |
| nebius/meta-llama/Meta-Llama-3.1-70B-Instruct | $0.1300 | $0.4000 |
| nebius/meta-llama/Meta-Llama-3.1-8B-Instruct | $0.0200 | $0.0600 |
| nebius/mistralai/Mistral-Nemo-Instruct-2407 | $0.0400 | $0.1200 |
| nebius/nvidia/Llama-3.1-Nemotron-Ultra-253B-v1 | $0.6000 | $1.8000 |
| nebius/nvidia/Llama-3.3-Nemotron-Super-49B-v1 | $0.1000 | $0.4000 |

## Nebius — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| nebius/BAAI/bge-en-icl | $0.0100 | $0.0000 |
| nebius/BAAI/bge-multilingual-gemma2 | $0.0100 | $0.0000 |
| nebius/intfloat/e5-mistral-7b-instruct | $0.0100 | $0.0000 |

## Nlp Cloud — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| chatdolphin | $0.5000 | $0.5000 |

## Nlp Cloud — completion (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| dolphin | $0.5000 | $0.5000 |

## Novita — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| novita/Sao10K/L3-8B-Stheno-v3.2 | $0.0500 | $0.0500 |
| novita/baichuan/baichuan-m2-32b | $0.0700 | $0.0700 |
| novita/baidu/ernie-4.5-21B-a3b | $0.0700 | $0.2800 |
| novita/baidu/ernie-4.5-21B-a3b-thinking | $0.0700 | $0.2800 |
| novita/baidu/ernie-4.5-300b-a47b-paddle | $0.2800 | $1.1000 |
| novita/baidu/ernie-4.5-vl-28b-a3b | $0.1400 | $0.5600 |
| novita/baidu/ernie-4.5-vl-28b-a3b-thinking | $0.3900 | $0.3900 |
| novita/baidu/ernie-4.5-vl-424b-a47b | $0.4200 | $1.2500 |
| novita/deepseek/deepseek-ocr | $0.0300 | $0.0300 |
| novita/deepseek/deepseek-prover-v2-671b | $0.7000 | $2.5000 |
| novita/deepseek/deepseek-r1-0528 | $0.7000 | $2.5000 |
| novita/deepseek/deepseek-r1-0528-qwen3-8b | $0.0600 | $0.0900 |
| novita/deepseek/deepseek-r1-distill-llama-70b | $0.8000 | $0.8000 |
| novita/deepseek/deepseek-r1-distill-qwen-14b | $0.1500 | $0.1500 |
| novita/deepseek/deepseek-r1-distill-qwen-32b | $0.3000 | $0.3000 |
| novita/deepseek/deepseek-r1-turbo | $0.7000 | $2.5000 |
| novita/deepseek/deepseek-v3-0324 | $0.2700 | $1.1200 |
| novita/deepseek/deepseek-v3-turbo | $0.4000 | $1.3000 |
| novita/deepseek/deepseek-v3.1 | $0.2700 | $1.0000 |
| novita/deepseek/deepseek-v3.1-terminus | $0.2700 | $1.0000 |
| novita/deepseek/deepseek-v3.2 | $0.2690 | $0.4000 |
| novita/deepseek/deepseek-v3.2-exp | $0.2700 | $0.4100 |
| novita/google/gemma-3-12b-it | $0.0500 | $0.1000 |
| novita/google/gemma-3-27b-it | $0.1190 | $0.2000 |
| novita/gryphe/mythomax-l2-13b | $0.0900 | $0.0900 |
| novita/kwaipilot/kat-coder-pro | $0.3000 | $1.2000 |
| novita/meta-llama/llama-3-70b-instruct | $0.5100 | $0.7400 |
| novita/meta-llama/llama-3-8b-instruct | $0.0400 | $0.0400 |
| novita/meta-llama/llama-3.1-8b-instruct | $0.0200 | $0.0500 |
| novita/meta-llama/llama-3.2-3b-instruct | $0.0300 | $0.0500 |
| novita/meta-llama/llama-3.3-70b-instruct | $0.1350 | $0.4000 |
| novita/meta-llama/llama-4-maverick-17b-128e-instruct-fp8 | $0.2700 | $0.8500 |
| novita/meta-llama/llama-4-scout-17b-16e-instruct | $0.1800 | $0.5900 |
| novita/microsoft/wizardlm-2-8x22b | $0.6200 | $0.6200 |
| novita/minimax/minimax-m2 | $0.3000 | $1.2000 |
| novita/minimax/minimax-m2.1 | $0.3000 | $1.2000 |
| novita/minimaxai/minimax-m1-80k | $0.5500 | $2.2000 |
| novita/mistralai/mistral-nemo | $0.0400 | $0.1700 |
| novita/moonshotai/kimi-k2-0905 | $0.6000 | $2.5000 |
| novita/moonshotai/kimi-k2-instruct | $0.5700 | $2.3000 |
| novita/moonshotai/kimi-k2-thinking | $0.6000 | $2.5000 |
| novita/nousresearch/hermes-2-pro-llama-3-8b | $0.1400 | $0.1400 |
| novita/openai/gpt-oss-120b | $0.0500 | $0.2500 |
| novita/openai/gpt-oss-20b | $0.0400 | $0.1500 |
| novita/paddlepaddle/paddleocr-vl | $0.0200 | $0.0200 |
| novita/qwen/qwen-2.5-72b-instruct | $0.3800 | $0.4000 |
| novita/qwen/qwen-mt-plus | $0.2500 | $0.7500 |
| novita/qwen/qwen2.5-7b-instruct | $0.0700 | $0.0700 |
| novita/qwen/qwen2.5-vl-72b-instruct | $0.8000 | $0.8000 |
| novita/qwen/qwen3-235b-a22b-fp8 | $0.2000 | $0.8000 |
| novita/qwen/qwen3-235b-a22b-instruct-2507 | $0.0900 | $0.5800 |
| novita/qwen/qwen3-235b-a22b-thinking-2507 | $0.3000 | $3.0000 |
| novita/qwen/qwen3-30b-a3b-fp8 | $0.0900 | $0.4500 |
| novita/qwen/qwen3-32b-fp8 | $0.1000 | $0.4500 |
| novita/qwen/qwen3-4b-fp8 | $0.0300 | $0.0300 |
| novita/qwen/qwen3-8b-fp8 | $0.0350 | $0.1380 |
| novita/qwen/qwen3-coder-30b-a3b-instruct | $0.0700 | $0.2700 |
| novita/qwen/qwen3-coder-480b-a35b-instruct | $0.3000 | $1.3000 |
| novita/qwen/qwen3-max | $2.1100 | $8.4500 |
| novita/qwen/qwen3-next-80b-a3b-instruct | $0.1500 | $1.5000 |
| novita/qwen/qwen3-next-80b-a3b-thinking | $0.1500 | $1.5000 |
| novita/qwen/qwen3-omni-30b-a3b-instruct | $0.2500 | $0.9700 |
| novita/qwen/qwen3-omni-30b-a3b-thinking | $0.2500 | $0.9700 |
| novita/qwen/qwen3-vl-235b-a22b-instruct | $0.3000 | $1.5000 |
| novita/qwen/qwen3-vl-235b-a22b-thinking | $0.9800 | $3.9500 |
| novita/qwen/qwen3-vl-30b-a3b-instruct | $0.2000 | $0.7000 |
| novita/qwen/qwen3-vl-30b-a3b-thinking | $0.2000 | $1.0000 |
| novita/qwen/qwen3-vl-8b-instruct | $0.0800 | $0.5000 |
| novita/sao10k/l3-70b-euryale-v2.1 | $1.4800 | $1.4800 |
| novita/sao10k/l3-8b-lunaris | $0.0500 | $0.0500 |
| novita/sao10k/l31-70b-euryale-v2.2 | $1.4800 | $1.4800 |
| novita/skywork/r1v4-lite | $0.2000 | $0.6000 |
| novita/xiaomimimo/mimo-v2-flash | $0.1000 | $0.3000 |
| novita/zai-org/autoglm-phone-9b-multilingual | $0.0350 | $0.1380 |
| novita/zai-org/glm-4.5 | $0.6000 | $2.2000 |
| novita/zai-org/glm-4.5-air | $0.1300 | $0.8500 |
| novita/zai-org/glm-4.5v | $0.6000 | $1.8000 |
| novita/zai-org/glm-4.6 | $0.5500 | $2.2000 |
| novita/zai-org/glm-4.6v | $0.3000 | $0.9000 |
| novita/zai-org/glm-4.7 | $0.6000 | $2.2000 |

## Novita — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| novita/baai/bge-m3 | $0.0100 | $0.0100 |
| novita/qwen/qwen3-embedding-0.6b | $0.0700 | $0.0000 |
| novita/qwen/qwen3-embedding-8b | $0.0700 | $0.0000 |

## Nscale — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| nscale/Qwen/QwQ-32B | $0.1800 | $0.2000 |
| nscale/Qwen/Qwen2.5-Coder-32B-Instruct | $0.0600 | $0.2000 |
| nscale/Qwen/Qwen2.5-Coder-3B-Instruct | $0.0100 | $0.0300 |
| nscale/Qwen/Qwen2.5-Coder-7B-Instruct | $0.0100 | $0.0300 |
| nscale/deepseek-ai/DeepSeek-R1-Distill-Llama-70B | $0.3750 | $0.3750 |
| nscale/deepseek-ai/DeepSeek-R1-Distill-Llama-8B | $0.0250 | $0.0250 |
| nscale/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B | $0.0900 | $0.0900 |
| nscale/deepseek-ai/DeepSeek-R1-Distill-Qwen-14B | $0.0700 | $0.0700 |
| nscale/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B | $0.1500 | $0.1500 |
| nscale/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B | $0.2000 | $0.2000 |
| nscale/meta-llama/Llama-3.1-8B-Instruct | $0.0300 | $0.0300 |
| nscale/meta-llama/Llama-3.3-70B-Instruct | $0.2000 | $0.2000 |
| nscale/meta-llama/Llama-4-Scout-17B-16E-Instruct | $0.0900 | $0.2900 |
| nscale/mistralai/mixtral-8x22b-instruct-v0.1 | $0.6000 | $0.6000 |

## Oci — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| oci/cohere.command-a-03-2025 | $1.5600 | $1.5600 |
| oci/cohere.command-a-reasoning-08-2025 | $1.5600 | $1.5600 |
| oci/cohere.command-a-translate-08-2025 | $0.0900 | $0.0900 |
| oci/cohere.command-a-vision-07-2025 | $1.5600 | $1.5600 |
| oci/cohere.command-latest | $1.5600 | $1.5600 |
| oci/cohere.command-plus-latest | $1.5600 | $1.5600 |
| oci/cohere.command-r-08-2024 | $0.1500 | $0.1500 |
| oci/cohere.command-r-plus-08-2024 | $1.5600 | $1.5600 |
| oci/google.gemini-2.5-flash | $0.1500 | $0.6000 |
| oci/google.gemini-2.5-flash-lite | $0.0750 | $0.3000 |
| oci/google.gemini-2.5-pro | $1.2500 | $10.0000 |
| oci/meta.llama-3.1-405b-instruct | $10.6800 | $10.6800 |
| oci/meta.llama-3.1-70b-instruct | $0.7200 | $0.7200 |
| oci/meta.llama-3.2-11b-vision-instruct | $2.0000 | $2.0000 |
| oci/meta.llama-3.2-90b-vision-instruct | $2.0000 | $2.0000 |
| oci/meta.llama-3.3-70b-instruct | $0.7200 | $0.7200 |
| oci/meta.llama-3.3-70b-instruct-fp8-dynamic | $0.7200 | $0.7200 |
| oci/meta.llama-4-maverick-17b-128e-instruct-fp8 | $0.7200 | $0.7200 |
| oci/meta.llama-4-scout-17b-16e-instruct | $0.7200 | $0.7200 |
| oci/xai.grok-3 | $3.0000 | $15.0000 |
| oci/xai.grok-3-fast | $5.0000 | $25.0000 |
| oci/xai.grok-3-mini | $0.3000 | $0.5000 |
| oci/xai.grok-3-mini-fast | $0.6000 | $4.0000 |
| oci/xai.grok-4 | $3.0000 | $15.0000 |
| oci/xai.grok-4-fast | $5.0000 | $25.0000 |
| oci/xai.grok-4.1-fast | $5.0000 | $25.0000 |
| oci/xai.grok-4.20 | $3.0000 | $15.0000 |
| oci/xai.grok-4.20-multi-agent | $3.0000 | $15.0000 |
| oci/xai.grok-code-fast-1 | $5.0000 | $25.0000 |

## Oci — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| oci/cohere.embed-english-image-v3.0 | $0.1000 | $0.0000 |
| oci/cohere.embed-english-light-image-v3.0 | $0.1000 | $0.0000 |
| oci/cohere.embed-english-light-v3.0 | $0.1000 | $0.0000 |
| oci/cohere.embed-english-v3.0 | $0.1000 | $0.0000 |
| oci/cohere.embed-multilingual-light-image-v3.0 | $0.1000 | $0.0000 |
| oci/cohere.embed-multilingual-light-v3.0 | $0.1000 | $0.0000 |
| oci/cohere.embed-multilingual-v3.0 | $0.1000 | $0.0000 |
| oci/cohere.embed-v4.0 | $0.1200 | $0.0000 |

## OpenAI — audio_speech (per 1M characters)

| Model | Input | Output |
|-------|-------|--------|
| tts-1 | $15.0000 | $0.0000 |
| tts-1-1106 | $15.0000 | $0.0000 |
| tts-1-hd | $30.0000 | $0.0000 |
| tts-1-hd-1106 | $30.0000 | $0.0000 |

## OpenAI — audio_speech (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| gpt-4o-mini-tts | $2.5000 | $250.0000 |
| gpt-4o-mini-tts-2025-03-20 | $2.5000 | $250.0000 |
| gpt-4o-mini-tts-2025-12-15 | $2.5000 | $250.0000 |

## OpenAI — audio_transcription (per 1M seconds)

| Model | Input | Output |
|-------|-------|--------|
| whisper-1 | $100.0000 | $100.0000 |

## OpenAI — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| chatgpt-4o-latest | $5.0000 | $15.0000 |
| gpt-3.5-turbo | $0.5000 | $1.5000 |
| gpt-3.5-turbo-0125 | $0.5000 | $1.5000 |
| gpt-3.5-turbo-1106 | $1.0000 | $2.0000 |
| gpt-3.5-turbo-16k | $3.0000 | $4.0000 |
| gpt-4 | $30.0000 | $60.0000 |
| gpt-4-0125-preview | $10.0000 | $30.0000 |
| gpt-4-0314 | $30.0000 | $60.0000 |
| gpt-4-0613 | $30.0000 | $60.0000 |
| gpt-4-1106-preview | $10.0000 | $30.0000 |
| gpt-4-turbo | $10.0000 | $30.0000 |
| gpt-4-turbo-2024-04-09 | $10.0000 | $30.0000 |
| gpt-4-turbo-preview | $10.0000 | $30.0000 |
| gpt-4.1 | $2.0000 | $8.0000 |
| gpt-4.1-2025-04-14 | $2.0000 | $8.0000 |
| gpt-4.1-mini | $0.4000 | $1.6000 |
| gpt-4.1-mini-2025-04-14 | $0.4000 | $1.6000 |
| gpt-4.1-nano | $0.1000 | $0.4000 |
| gpt-4.1-nano-2025-04-14 | $0.1000 | $0.4000 |
| gpt-4o | $2.5000 | $10.0000 |
| gpt-4o-2024-05-13 | $5.0000 | $15.0000 |
| gpt-4o-2024-08-06 | $2.5000 | $10.0000 |
| gpt-4o-2024-11-20 | $2.5000 | $10.0000 |
| gpt-4o-audio-preview | $2.5000 | $10.0000 |
| gpt-4o-audio-preview-2024-12-17 | $2.5000 | $10.0000 |
| gpt-4o-audio-preview-2025-06-03 | $2.5000 | $10.0000 |
| gpt-4o-mini | $0.1500 | $0.6000 |
| gpt-4o-mini-2024-07-18 | $0.1500 | $0.6000 |
| gpt-4o-mini-audio-preview | $0.1500 | $0.6000 |
| gpt-4o-mini-audio-preview-2024-12-17 | $0.1500 | $0.6000 |
| gpt-4o-mini-realtime-preview | $0.6000 | $2.4000 |
| gpt-4o-mini-realtime-preview-2024-12-17 | $0.6000 | $2.4000 |
| gpt-4o-mini-search-preview | $0.1500 | $0.6000 |
| gpt-4o-mini-search-preview-2025-03-11 | $0.1500 | $0.6000 |
| gpt-4o-realtime-preview | $5.0000 | $20.0000 |
| gpt-4o-realtime-preview-2024-12-17 | $5.0000 | $20.0000 |
| gpt-4o-realtime-preview-2025-06-03 | $5.0000 | $20.0000 |
| gpt-4o-search-preview | $2.5000 | $10.0000 |
| gpt-4o-search-preview-2025-03-11 | $2.5000 | $10.0000 |
| gpt-5 | $1.2500 | $10.0000 |
| gpt-5-2025-08-07 | $1.2500 | $10.0000 |
| gpt-5-chat | $1.2500 | $10.0000 |
| gpt-5-chat-latest | $1.2500 | $10.0000 |
| gpt-5-mini | $0.2500 | $2.0000 |
| gpt-5-mini-2025-08-07 | $0.2500 | $2.0000 |
| gpt-5-nano | $0.0500 | $0.4000 |
| gpt-5-nano-2025-08-07 | $0.0500 | $0.4000 |
| gpt-5-search-api | $1.2500 | $10.0000 |
| gpt-5-search-api-2025-10-14 | $1.2500 | $10.0000 |
| gpt-5.1 | $1.2500 | $10.0000 |
| gpt-5.1-2025-11-13 | $1.2500 | $10.0000 |
| gpt-5.1-chat-latest | $1.2500 | $10.0000 |
| gpt-5.2 | $1.7500 | $14.0000 |
| gpt-5.2-2025-12-11 | $1.7500 | $14.0000 |
| gpt-5.2-chat-latest | $1.7500 | $14.0000 |
| gpt-5.3-chat-latest | $1.7500 | $14.0000 |
| gpt-5.4 | $2.5000 | $15.0000 |
| gpt-5.4-2026-03-05 | $2.5000 | $15.0000 |
| gpt-5.4-mini | $0.7500 | $4.5000 |
| gpt-5.4-nano | $0.2000 | $1.2500 |
| gpt-audio | $2.5000 | $10.0000 |
| gpt-audio-1.5 | $2.5000 | $10.0000 |
| gpt-audio-2025-08-28 | $2.5000 | $10.0000 |
| gpt-audio-mini | $0.6000 | $2.4000 |
| gpt-audio-mini-2025-10-06 | $0.6000 | $2.4000 |
| gpt-audio-mini-2025-12-15 | $0.6000 | $2.4000 |
| gpt-realtime | $4.0000 | $16.0000 |
| gpt-realtime-1.5 | $4.0000 | $16.0000 |
| gpt-realtime-2025-08-28 | $4.0000 | $16.0000 |
| gpt-realtime-mini | $0.6000 | $2.4000 |
| gpt-realtime-mini-2025-10-06 | $0.6000 | $2.4000 |
| gpt-realtime-mini-2025-12-15 | $0.6000 | $2.4000 |
| o1 | $15.0000 | $60.0000 |
| o1-2024-12-17 | $15.0000 | $60.0000 |
| o3 | $2.0000 | $8.0000 |
| o3-2025-04-16 | $2.0000 | $8.0000 |
| o3-mini | $1.1000 | $4.4000 |
| o3-mini-2025-01-31 | $1.1000 | $4.4000 |
| o4-mini | $1.1000 | $4.4000 |
| o4-mini-2025-04-16 | $1.1000 | $4.4000 |

## OpenAI — completion (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| babbage-002 | $0.4000 | $0.4000 |
| davinci-002 | $2.0000 | $2.0000 |
| gpt-3.5-turbo-instruct | $1.5000 | $2.0000 |
| gpt-3.5-turbo-instruct-0914 | $1.5000 | $2.0000 |

## OpenAI — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| text-embedding-3-large | $0.1300 | $0.0000 |
| text-embedding-3-small | $0.0200 | $0.0000 |
| text-embedding-ada-002 | $0.1000 | $0.0000 |
| text-embedding-ada-002-v2 | $0.1000 | $0.0000 |

## OpenAI — image_generation (per 1M images)

| Model | Input | Output |
|-------|-------|--------|
| 1024-x-1024/gpt-image-1.5 | $9000.0000 | $0.0000 |
| 1024-x-1024/gpt-image-1.5-2025-12-16 | $9000.0000 | $0.0000 |
| 1024-x-1536/gpt-image-1.5 | $13000.0000 | $0.0000 |
| 1024-x-1536/gpt-image-1.5-2025-12-16 | $13000.0000 | $0.0000 |
| 1536-x-1024/gpt-image-1.5 | $13000.0000 | $0.0000 |
| 1536-x-1024/gpt-image-1.5-2025-12-16 | $13000.0000 | $0.0000 |
| dall-e-2 | $20000.0000 | $0.0000 |
| dall-e-3 | $40000.0000 | $0.0000 |
| high/1024-x-1024/gpt-image-1 | $167000.0000 | $0.0000 |
| high/1024-x-1024/gpt-image-1.5 | $133000.0000 | $0.0000 |
| high/1024-x-1024/gpt-image-1.5-2025-12-16 | $133000.0000 | $0.0000 |
| high/1024-x-1536/gpt-image-1 | $250000.0000 | $0.0000 |
| high/1024-x-1536/gpt-image-1.5 | $200000.0000 | $0.0000 |
| high/1024-x-1536/gpt-image-1.5-2025-12-16 | $200000.0000 | $0.0000 |
| high/1536-x-1024/gpt-image-1 | $250000.0000 | $0.0000 |
| high/1536-x-1024/gpt-image-1.5 | $200000.0000 | $0.0000 |
| high/1536-x-1024/gpt-image-1.5-2025-12-16 | $200000.0000 | $0.0000 |
| low/1024-x-1024/gpt-image-1 | $11000.0000 | $0.0000 |
| low/1024-x-1024/gpt-image-1-mini | $5000.0000 | $0.0000 |
| low/1024-x-1024/gpt-image-1.5 | $9000.0000 | $0.0000 |
| low/1024-x-1024/gpt-image-1.5-2025-12-16 | $9000.0000 | $0.0000 |
| low/1024-x-1536/gpt-image-1 | $16000.0000 | $0.0000 |
| low/1024-x-1536/gpt-image-1-mini | $6000.0000 | $0.0000 |
| low/1024-x-1536/gpt-image-1.5 | $13000.0000 | $0.0000 |
| low/1024-x-1536/gpt-image-1.5-2025-12-16 | $13000.0000 | $0.0000 |
| low/1536-x-1024/gpt-image-1 | $16000.0000 | $0.0000 |
| low/1536-x-1024/gpt-image-1-mini | $6000.0000 | $0.0000 |
| low/1536-x-1024/gpt-image-1.5 | $13000.0000 | $0.0000 |
| low/1536-x-1024/gpt-image-1.5-2025-12-16 | $13000.0000 | $0.0000 |
| medium/1024-x-1024/gpt-image-1 | $42000.0000 | $0.0000 |
| medium/1024-x-1024/gpt-image-1-mini | $11000.0000 | $0.0000 |
| medium/1024-x-1024/gpt-image-1.5 | $34000.0000 | $0.0000 |
| medium/1024-x-1024/gpt-image-1.5-2025-12-16 | $34000.0000 | $0.0000 |
| medium/1024-x-1536/gpt-image-1 | $63000.0000 | $0.0000 |
| medium/1024-x-1536/gpt-image-1-mini | $15000.0000 | $0.0000 |
| medium/1024-x-1536/gpt-image-1.5 | $50000.0000 | $0.0000 |
| medium/1024-x-1536/gpt-image-1.5-2025-12-16 | $50000.0000 | $0.0000 |
| medium/1536-x-1024/gpt-image-1 | $63000.0000 | $0.0000 |
| medium/1536-x-1024/gpt-image-1-mini | $15000.0000 | $0.0000 |
| medium/1536-x-1024/gpt-image-1.5 | $50000.0000 | $0.0000 |
| medium/1536-x-1024/gpt-image-1.5-2025-12-16 | $50000.0000 | $0.0000 |
| standard/1024-x-1024/gpt-image-1.5 | $9000.0000 | $0.0000 |
| standard/1024-x-1024/gpt-image-1.5-2025-12-16 | $9000.0000 | $0.0000 |
| standard/1024-x-1536/gpt-image-1.5 | $13000.0000 | $0.0000 |
| standard/1024-x-1536/gpt-image-1.5-2025-12-16 | $13000.0000 | $0.0000 |
| standard/1536-x-1024/gpt-image-1.5 | $13000.0000 | $0.0000 |
| standard/1536-x-1024/gpt-image-1.5-2025-12-16 | $13000.0000 | $0.0000 |

## OpenAI — responses (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| codex-mini-latest | $1.5000 | $6.0000 |
| gpt-5-codex | $1.2500 | $10.0000 |
| gpt-5-pro | $15.0000 | $120.0000 |
| gpt-5-pro-2025-10-06 | $15.0000 | $120.0000 |
| gpt-5.1-codex | $1.2500 | $10.0000 |
| gpt-5.1-codex-max | $1.2500 | $10.0000 |
| gpt-5.1-codex-mini | $0.2500 | $2.0000 |
| gpt-5.2-codex | $1.7500 | $14.0000 |
| gpt-5.2-pro | $21.0000 | $168.0000 |
| gpt-5.2-pro-2025-12-11 | $21.0000 | $168.0000 |
| gpt-5.3-codex | $1.7500 | $14.0000 |
| gpt-5.4-pro | $30.0000 | $180.0000 |
| gpt-5.4-pro-2026-03-05 | $30.0000 | $180.0000 |
| o1-pro | $150.0000 | $600.0000 |
| o1-pro-2025-03-19 | $150.0000 | $600.0000 |
| o3-deep-research | $10.0000 | $40.0000 |
| o3-deep-research-2025-06-26 | $10.0000 | $40.0000 |
| o3-pro | $20.0000 | $80.0000 |
| o3-pro-2025-06-10 | $20.0000 | $80.0000 |
| o4-mini-deep-research | $2.0000 | $8.0000 |
| o4-mini-deep-research-2025-06-26 | $2.0000 | $8.0000 |

## OpenRouter — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| openrouter/anthropic/claude-3-haiku | $0.2500 | $1.2500 |
| openrouter/anthropic/claude-3.5-sonnet | $3.0000 | $15.0000 |
| openrouter/anthropic/claude-3.7-sonnet | $3.0000 | $15.0000 |
| openrouter/anthropic/claude-haiku-4.5 | $1.0000 | $5.0000 |
| openrouter/anthropic/claude-opus-4 | $15.0000 | $75.0000 |
| openrouter/anthropic/claude-opus-4.1 | $15.0000 | $75.0000 |
| openrouter/anthropic/claude-opus-4.5 | $5.0000 | $25.0000 |
| openrouter/anthropic/claude-opus-4.6 | $5.0000 | $25.0000 |
| openrouter/anthropic/claude-sonnet-4 | $3.0000 | $15.0000 |
| openrouter/anthropic/claude-sonnet-4.5 | $3.0000 | $15.0000 |
| openrouter/anthropic/claude-sonnet-4.6 | $3.0000 | $15.0000 |
| openrouter/bytedance/ui-tars-1.5-7b | $0.1000 | $0.2000 |
| openrouter/deepseek/deepseek-chat | $0.1400 | $0.2800 |
| openrouter/deepseek/deepseek-chat-v3-0324 | $0.1400 | $0.2800 |
| openrouter/deepseek/deepseek-chat-v3.1 | $0.2000 | $0.8000 |
| openrouter/deepseek/deepseek-r1 | $0.5500 | $2.1900 |
| openrouter/deepseek/deepseek-r1-0528 | $0.5000 | $2.1500 |
| openrouter/deepseek/deepseek-v3.2 | $0.2800 | $0.4000 |
| openrouter/deepseek/deepseek-v3.2-exp | $0.2000 | $0.4000 |
| openrouter/google/gemini-2.0-flash-001 | $0.1000 | $0.4000 |
| openrouter/google/gemini-2.5-flash | $0.3000 | $2.5000 |
| openrouter/google/gemini-2.5-pro | $1.2500 | $10.0000 |
| openrouter/google/gemini-3-flash-preview | $0.5000 | $3.0000 |
| openrouter/google/gemini-3-pro-preview | $2.0000 | $12.0000 |
| openrouter/google/gemini-3.1-flash-lite-preview | $0.2500 | $1.5000 |
| openrouter/google/gemini-3.1-pro-preview | $2.0000 | $12.0000 |
| openrouter/gryphe/mythomax-l2-13b | $1.8750 | $1.8750 |
| openrouter/mancer/weaver | $5.6250 | $5.6250 |
| openrouter/meta-llama/llama-3-70b-instruct | $0.5900 | $0.7900 |
| openrouter/minimax/minimax-m2 | $0.2550 | $1.0200 |
| openrouter/minimax/minimax-m2.1 | $0.2700 | $1.2000 |
| openrouter/minimax/minimax-m2.5 | $0.3000 | $1.1000 |
| openrouter/mistralai/devstral-2512 | $0.1500 | $0.6000 |
| openrouter/mistralai/ministral-14b-2512 | $0.2000 | $0.2000 |
| openrouter/mistralai/ministral-3b-2512 | $0.1000 | $0.1000 |
| openrouter/mistralai/ministral-8b-2512 | $0.1500 | $0.1500 |
| openrouter/mistralai/mistral-7b-instruct | $0.1300 | $0.1300 |
| openrouter/mistralai/mistral-large | $8.0000 | $24.0000 |
| openrouter/mistralai/mistral-large-2512 | $0.5000 | $1.5000 |
| openrouter/mistralai/mistral-small-3.1-24b-instruct | $0.1000 | $0.3000 |
| openrouter/mistralai/mistral-small-3.2-24b-instruct | $0.1000 | $0.3000 |
| openrouter/mistralai/mixtral-8x22b-instruct | $0.6500 | $0.6500 |
| openrouter/moonshotai/kimi-k2.5 | $0.6000 | $3.0000 |
| openrouter/openai/gpt-3.5-turbo | $1.5000 | $2.0000 |
| openrouter/openai/gpt-3.5-turbo-16k | $3.0000 | $4.0000 |
| openrouter/openai/gpt-4 | $30.0000 | $60.0000 |
| openrouter/openai/gpt-4.1 | $2.0000 | $8.0000 |
| openrouter/openai/gpt-4.1-mini | $0.4000 | $1.6000 |
| openrouter/openai/gpt-4.1-nano | $0.1000 | $0.4000 |
| openrouter/openai/gpt-4o | $2.5000 | $10.0000 |
| openrouter/openai/gpt-4o-2024-05-13 | $5.0000 | $15.0000 |
| openrouter/openai/gpt-5 | $1.2500 | $10.0000 |
| openrouter/openai/gpt-5-chat | $1.2500 | $10.0000 |
| openrouter/openai/gpt-5-codex | $1.2500 | $10.0000 |
| openrouter/openai/gpt-5-mini | $0.2500 | $2.0000 |
| openrouter/openai/gpt-5-nano | $0.0500 | $0.4000 |
| openrouter/openai/gpt-5.1-codex-max | $1.2500 | $10.0000 |
| openrouter/openai/gpt-5.2 | $1.7500 | $14.0000 |
| openrouter/openai/gpt-5.2-chat | $1.7500 | $14.0000 |
| openrouter/openai/gpt-5.2-codex | $1.7500 | $14.0000 |
| openrouter/openai/gpt-5.2-pro | $21.0000 | $168.0000 |
| openrouter/openai/gpt-oss-120b | $0.1800 | $0.8000 |
| openrouter/openai/gpt-oss-20b | $0.0200 | $0.1000 |
| openrouter/openai/o1 | $15.0000 | $60.0000 |
| openrouter/openai/o3-mini | $1.1000 | $4.4000 |
| openrouter/openai/o3-mini-high | $1.1000 | $4.4000 |
| openrouter/qwen/qwen-2.5-coder-32b-instruct | $0.1800 | $0.1800 |
| openrouter/qwen/qwen-vl-plus | $0.2100 | $0.6300 |
| openrouter/qwen/qwen3-235b-a22b-2507 | $0.0710 | $0.1000 |
| openrouter/qwen/qwen3-235b-a22b-thinking-2507 | $0.1100 | $0.6000 |
| openrouter/qwen/qwen3-coder | $0.2200 | $0.9500 |
| openrouter/qwen/qwen3-coder-plus | $1.0000 | $5.0000 |
| openrouter/qwen/qwen3.5-122b-a10b | $0.4000 | $2.0000 |
| openrouter/qwen/qwen3.5-27b | $0.3000 | $2.4000 |
| openrouter/qwen/qwen3.5-35b-a3b | $0.2500 | $2.0000 |
| openrouter/qwen/qwen3.5-397b-a17b | $0.6000 | $3.6000 |
| openrouter/qwen/qwen3.5-flash-02-23 | $0.1000 | $0.4000 |
| openrouter/qwen/qwen3.5-plus-02-15 | $0.4000 | $2.4000 |
| openrouter/switchpoint/router | $0.8500 | $3.4000 |
| openrouter/undi95/remm-slerp-l2-13b | $1.8750 | $1.8750 |
| openrouter/x-ai/grok-4 | $3.0000 | $15.0000 |
| openrouter/xiaomi/mimo-v2-flash | $0.0900 | $0.2900 |
| openrouter/z-ai/glm-4.6 | $0.4000 | $1.7500 |
| openrouter/z-ai/glm-4.6:exacto | $0.4500 | $1.9000 |
| openrouter/z-ai/glm-4.7 | $0.4000 | $1.5000 |
| openrouter/z-ai/glm-4.7-flash | $0.0700 | $0.4000 |
| openrouter/z-ai/glm-5 | $0.8000 | $2.5600 |

## Ovhcloud — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| ovhcloud/DeepSeek-R1-Distill-Llama-70B | $0.6700 | $0.6700 |
| ovhcloud/Llama-3.1-8B-Instruct | $0.1000 | $0.1000 |
| ovhcloud/Meta-Llama-3_1-70B-Instruct | $0.6700 | $0.6700 |
| ovhcloud/Meta-Llama-3_3-70B-Instruct | $0.6700 | $0.6700 |
| ovhcloud/Mistral-7B-Instruct-v0.3 | $0.1000 | $0.1000 |
| ovhcloud/Mistral-Nemo-Instruct-2407 | $0.1300 | $0.1300 |
| ovhcloud/Mistral-Small-3.2-24B-Instruct-2506 | $0.0900 | $0.2800 |
| ovhcloud/Mixtral-8x7B-Instruct-v0.1 | $0.6300 | $0.6300 |
| ovhcloud/Qwen2.5-Coder-32B-Instruct | $0.8700 | $0.8700 |
| ovhcloud/Qwen2.5-VL-72B-Instruct | $0.9100 | $0.9100 |
| ovhcloud/Qwen3-32B | $0.0800 | $0.2300 |
| ovhcloud/gpt-oss-120b | $0.0800 | $0.4000 |
| ovhcloud/gpt-oss-20b | $0.0400 | $0.1500 |
| ovhcloud/llava-v1.6-mistral-7b-hf | $0.2900 | $0.2900 |
| ovhcloud/mamba-codestral-7B-v0.1 | $0.1900 | $0.1900 |

## Palm — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| palm/chat-bison | $0.1250 | $0.1250 |
| palm/chat-bison-001 | $0.1250 | $0.1250 |

## Palm — completion (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| palm/text-bison | $0.1250 | $0.1250 |
| palm/text-bison-001 | $0.1250 | $0.1250 |
| palm/text-bison-safety-off | $0.1250 | $0.1250 |
| palm/text-bison-safety-recitation-off | $0.1250 | $0.1250 |

## Parallel Ai — search (per 1M queries)

| Model | Input | Output |
|-------|-------|--------|
| parallel_ai/search | $4000.0000 | $0.0000 |
| parallel_ai/search-pro | $9000.0000 | $0.0000 |

## Perplexity — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| perplexity/codellama-34b-instruct | $0.3500 | $1.4000 |
| perplexity/codellama-70b-instruct | $0.7000 | $2.8000 |
| perplexity/llama-2-70b-chat | $0.7000 | $2.8000 |
| perplexity/llama-3.1-70b-instruct | $1.0000 | $1.0000 |
| perplexity/llama-3.1-8b-instruct | $0.2000 | $0.2000 |
| perplexity/mistral-7b-instruct | $0.0700 | $0.2800 |
| perplexity/mixtral-8x7b-instruct | $0.0700 | $0.2800 |
| perplexity/pplx-70b-chat | $0.7000 | $2.8000 |
| perplexity/pplx-70b-online | $0.0000 | $2.8000 |
| perplexity/pplx-7b-chat | $0.0700 | $0.2800 |
| perplexity/pplx-7b-online | $0.0000 | $0.2800 |
| perplexity/sonar | $1.0000 | $1.0000 |
| perplexity/sonar-deep-research | $2.0000 | $8.0000 |
| perplexity/sonar-medium-chat | $0.6000 | $1.8000 |
| perplexity/sonar-medium-online | $0.0000 | $1.8000 |
| perplexity/sonar-pro | $3.0000 | $15.0000 |
| perplexity/sonar-reasoning | $1.0000 | $5.0000 |
| perplexity/sonar-reasoning-pro | $2.0000 | $8.0000 |
| perplexity/sonar-small-chat | $0.0700 | $0.2800 |
| perplexity/sonar-small-online | $0.0000 | $0.2800 |

## Perplexity — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| perplexity/pplx-embed-v1-0.6b | $0.0040 | $0.0000 |
| perplexity/pplx-embed-v1-4b | $0.0300 | $0.0000 |

## Perplexity — search (per 1M queries)

| Model | Input | Output |
|-------|-------|--------|
| perplexity/search | $5000.0000 | $0.0000 |

## Recraft — image_generation (per 1M images)

| Model | Input | Output |
|-------|-------|--------|
| recraft/recraftv2 | $0.0000 | $22000.0000 |
| recraft/recraftv3 | $0.0000 | $40000.0000 |

## Replicate — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| replicate/anthropic/claude-3.5-haiku | $1.0000 | $5.0000 |
| replicate/anthropic/claude-3.5-sonnet | $3.7500 | $18.7500 |
| replicate/anthropic/claude-3.7-sonnet | $3.0000 | $15.0000 |
| replicate/anthropic/claude-4-sonnet | $3.0000 | $15.0000 |
| replicate/anthropic/claude-4.5-haiku | $1.0000 | $5.0000 |
| replicate/anthropic/claude-4.5-sonnet | $3.0000 | $15.0000 |
| replicate/deepseek-ai/deepseek-r1 | $3.7500 | $10.0000 |
| replicate/deepseek-ai/deepseek-v3 | $1.4500 | $1.4500 |
| replicate/deepseek-ai/deepseek-v3.1 | $0.6720 | $2.0160 |
| replicate/google/gemini-2.5-flash | $2.5000 | $2.5000 |
| replicate/google/gemini-3-pro | $2.0000 | $12.0000 |
| replicate/ibm-granite/granite-3.3-8b-instruct | $0.0300 | $0.2500 |
| replicate/meta/llama-2-13b | $0.1000 | $0.5000 |
| replicate/meta/llama-2-13b-chat | $0.1000 | $0.5000 |
| replicate/meta/llama-2-70b | $0.6500 | $2.7500 |
| replicate/meta/llama-2-70b-chat | $0.6500 | $2.7500 |
| replicate/meta/llama-2-7b | $0.0500 | $0.2500 |
| replicate/meta/llama-2-7b-chat | $0.0500 | $0.2500 |
| replicate/meta/llama-3-70b | $0.6500 | $2.7500 |
| replicate/meta/llama-3-70b-instruct | $0.6500 | $2.7500 |
| replicate/meta/llama-3-8b | $0.0500 | $0.2500 |
| replicate/meta/llama-3-8b-instruct | $0.0500 | $0.2500 |
| replicate/mistralai/mistral-7b-instruct-v0.2 | $0.0500 | $0.2500 |
| replicate/mistralai/mistral-7b-v0.1 | $0.0500 | $0.2500 |
| replicate/mistralai/mixtral-8x7b-instruct-v0.1 | $0.3000 | $1.0000 |
| replicate/openai/gpt-4.1 | $2.0000 | $8.0000 |
| replicate/openai/gpt-4.1-mini | $0.4000 | $1.6000 |
| replicate/openai/gpt-4.1-nano | $0.1000 | $0.4000 |
| replicate/openai/gpt-4o | $2.5000 | $10.0000 |
| replicate/openai/gpt-4o-mini | $0.1500 | $0.6000 |
| replicate/openai/gpt-5 | $1.2500 | $10.0000 |
| replicate/openai/gpt-5-mini | $0.2500 | $2.0000 |
| replicate/openai/gpt-5-nano | $0.0500 | $0.4000 |
| replicate/openai/gpt-oss-120b | $0.1800 | $0.7200 |
| replicate/openai/o1 | $15.0000 | $60.0000 |
| replicate/openai/o1-mini | $1.1000 | $4.4000 |
| replicate/openai/o4-mini | $1.0000 | $4.0000 |
| replicate/qwen/qwen3-235b-a22b-instruct-2507 | $0.2640 | $1.0600 |
| replicate/xai/grok-4 | $7.2000 | $36.0000 |
| replicateopenai/gpt-oss-20b | $0.0900 | $0.3600 |

## Runwayml — audio_speech (per 1M characters)

| Model | Input | Output |
|-------|-------|--------|
| runwayml/eleven_multilingual_v2 | $0.3000 | $0.0000 |

## Runwayml — image_generation (per 1M images)

| Model | Input | Output |
|-------|-------|--------|
| runwayml/gen4_image | $50000.0000 | $50000.0000 |
| runwayml/gen4_image_turbo | $20000.0000 | $20000.0000 |

## SambaNova — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| sambanova/DeepSeek-R1 | $5.0000 | $7.0000 |
| sambanova/DeepSeek-R1-Distill-Llama-70B | $0.7000 | $1.4000 |
| sambanova/DeepSeek-V3-0324 | $3.0000 | $4.5000 |
| sambanova/DeepSeek-V3.1 | $3.0000 | $4.5000 |
| sambanova/Llama-4-Maverick-17B-128E-Instruct | $0.6300 | $1.8000 |
| sambanova/Llama-4-Scout-17B-16E-Instruct | $0.4000 | $0.7000 |
| sambanova/Meta-Llama-3.1-405B-Instruct | $5.0000 | $10.0000 |
| sambanova/Meta-Llama-3.1-8B-Instruct | $0.1000 | $0.2000 |
| sambanova/Meta-Llama-3.2-1B-Instruct | $0.0400 | $0.0800 |
| sambanova/Meta-Llama-3.2-3B-Instruct | $0.0800 | $0.1600 |
| sambanova/Meta-Llama-3.3-70B-Instruct | $0.6000 | $1.2000 |
| sambanova/Meta-Llama-Guard-3-8B | $0.3000 | $0.3000 |
| sambanova/QwQ-32B | $0.5000 | $1.0000 |
| sambanova/Qwen2-Audio-7B-Instruct | $0.5000 | $100.0000 |
| sambanova/Qwen3-32B | $0.4000 | $0.8000 |
| sambanova/gpt-oss-120b | $3.0000 | $4.5000 |

## Serper — search (per 1M queries)

| Model | Input | Output |
|-------|-------|--------|
| serper/search | $1000.0000 | $0.0000 |

## Stability — image_edit (per 1M images)

| Model | Input | Output |
|-------|-------|--------|
| stability/conservative | $0.0000 | $40000.0000 |
| stability/creative | $0.0000 | $60000.0000 |
| stability/erase | $0.0000 | $5000.0000 |
| stability/fast | $0.0000 | $2000.0000 |
| stability/inpaint | $0.0000 | $5000.0000 |
| stability/outpaint | $0.0000 | $4000.0000 |
| stability/remove-background | $0.0000 | $5000.0000 |
| stability/replace-background-and-relight | $0.0000 | $8000.0000 |
| stability/search-and-recolor | $0.0000 | $5000.0000 |
| stability/search-and-replace | $0.0000 | $5000.0000 |
| stability/sketch | $0.0000 | $5000.0000 |
| stability/structure | $0.0000 | $5000.0000 |
| stability/style | $0.0000 | $5000.0000 |
| stability/style-transfer | $0.0000 | $8000.0000 |

## Stability — image_generation (per 1M images)

| Model | Input | Output |
|-------|-------|--------|
| stability/sd3 | $0.0000 | $65000.0000 |
| stability/sd3-large | $0.0000 | $65000.0000 |
| stability/sd3-large-turbo | $0.0000 | $40000.0000 |
| stability/sd3-medium | $0.0000 | $35000.0000 |
| stability/sd3.5-large | $0.0000 | $65000.0000 |
| stability/sd3.5-large-turbo | $0.0000 | $40000.0000 |
| stability/sd3.5-medium | $0.0000 | $35000.0000 |
| stability/stable-image-core | $0.0000 | $30000.0000 |
| stability/stable-image-ultra | $0.0000 | $80000.0000 |

## Tavily — search (per 1M queries)

| Model | Input | Output |
|-------|-------|--------|
| tavily/search | $8000.0000 | $0.0000 |
| tavily/search-advanced | $16000.0000 | $0.0000 |

## Together AI — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| together-ai-21.1b-41b | $0.8000 | $0.8000 |
| together-ai-4.1b-8b | $0.2000 | $0.2000 |
| together-ai-41.1b-80b | $0.9000 | $0.9000 |
| together-ai-8.1b-21b | $0.3000 | $0.3000 |
| together-ai-81.1b-110b | $1.8000 | $1.8000 |
| together-ai-up-to-4b | $0.1000 | $0.1000 |
| together_ai/Qwen/Qwen3-235B-A22B-Instruct-2507-tput | $0.2000 | $6.0000 |
| together_ai/Qwen/Qwen3-235B-A22B-Thinking-2507 | $0.6500 | $3.0000 |
| together_ai/Qwen/Qwen3-235B-A22B-fp8-tput | $0.2000 | $0.6000 |
| together_ai/Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8 | $2.0000 | $2.0000 |
| together_ai/Qwen/Qwen3-Next-80B-A3B-Instruct | $0.1500 | $1.5000 |
| together_ai/Qwen/Qwen3-Next-80B-A3B-Thinking | $0.1500 | $1.5000 |
| together_ai/Qwen/Qwen3.5-397B-A17B | $0.6000 | $3.6000 |
| together_ai/deepseek-ai/DeepSeek-R1 | $3.0000 | $7.0000 |
| together_ai/deepseek-ai/DeepSeek-R1-0528-tput | $0.5500 | $2.1900 |
| together_ai/deepseek-ai/DeepSeek-V3 | $1.2500 | $1.2500 |
| together_ai/deepseek-ai/DeepSeek-V3.1 | $0.6000 | $1.7000 |
| together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo | $0.8800 | $0.8800 |
| together_ai/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8 | $0.2700 | $0.8500 |
| together_ai/meta-llama/Llama-4-Scout-17B-16E-Instruct | $0.1800 | $0.5900 |
| together_ai/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo | $3.5000 | $3.5000 |
| together_ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo | $0.8800 | $0.8800 |
| together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo | $0.1800 | $0.1800 |
| together_ai/mistralai/Mixtral-8x7B-Instruct-v0.1 | $0.6000 | $0.6000 |
| together_ai/moonshotai/Kimi-K2-Instruct | $1.0000 | $3.0000 |
| together_ai/moonshotai/Kimi-K2-Instruct-0905 | $1.0000 | $3.0000 |
| together_ai/moonshotai/Kimi-K2.5 | $0.5000 | $2.8000 |
| together_ai/openai/gpt-oss-120b | $0.1500 | $0.6000 |
| together_ai/openai/gpt-oss-20b | $0.0500 | $0.2000 |
| together_ai/zai-org/GLM-4.5-Air-FP8 | $0.2000 | $1.1000 |
| together_ai/zai-org/GLM-4.6 | $0.6000 | $2.2000 |
| together_ai/zai-org/GLM-4.7 | $0.4500 | $2.0000 |

## Together AI — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| together-ai-embedding-151m-to-350m | $0.0160 | $0.0000 |
| together-ai-embedding-up-to-150m | $0.0080 | $0.0000 |
| together_ai/BAAI/bge-base-en-v1.5 | $0.0080 | $0.0000 |
| together_ai/baai/bge-base-en-v1.5 | $0.0080 | $0.0000 |

## V0 — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| v0/v0-1.0-md | $3.0000 | $15.0000 |
| v0/v0-1.5-lg | $15.0000 | $75.0000 |
| v0/v0-1.5-md | $3.0000 | $15.0000 |

## Vercel Ai Gateway — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| vercel_ai_gateway/alibaba/qwen-3-14b | $0.0800 | $0.2400 |
| vercel_ai_gateway/alibaba/qwen-3-235b | $0.2000 | $0.6000 |
| vercel_ai_gateway/alibaba/qwen-3-30b | $0.1000 | $0.3000 |
| vercel_ai_gateway/alibaba/qwen-3-32b | $0.1000 | $0.3000 |
| vercel_ai_gateway/alibaba/qwen3-coder | $0.4000 | $1.6000 |
| vercel_ai_gateway/amazon/nova-lite | $0.0600 | $0.2400 |
| vercel_ai_gateway/amazon/nova-micro | $0.0350 | $0.1400 |
| vercel_ai_gateway/amazon/nova-pro | $0.8000 | $3.2000 |
| vercel_ai_gateway/amazon/titan-embed-text-v2 | $0.0200 | $0.0000 |
| vercel_ai_gateway/anthropic/claude-3-5-sonnet | $3.0000 | $15.0000 |
| vercel_ai_gateway/anthropic/claude-3-5-sonnet-20241022 | $3.0000 | $15.0000 |
| vercel_ai_gateway/anthropic/claude-3-7-sonnet | $3.0000 | $15.0000 |
| vercel_ai_gateway/anthropic/claude-3-haiku | $0.2500 | $1.2500 |
| vercel_ai_gateway/anthropic/claude-3-opus | $15.0000 | $75.0000 |
| vercel_ai_gateway/anthropic/claude-3.5-haiku | $0.8000 | $4.0000 |
| vercel_ai_gateway/anthropic/claude-3.5-sonnet | $3.0000 | $15.0000 |
| vercel_ai_gateway/anthropic/claude-3.7-sonnet | $3.0000 | $15.0000 |
| vercel_ai_gateway/anthropic/claude-4-opus | $15.0000 | $75.0000 |
| vercel_ai_gateway/anthropic/claude-4-sonnet | $3.0000 | $15.0000 |
| vercel_ai_gateway/anthropic/claude-haiku-4.5 | $1.0000 | $5.0000 |
| vercel_ai_gateway/anthropic/claude-opus-4 | $15.0000 | $75.0000 |
| vercel_ai_gateway/anthropic/claude-opus-4.1 | $15.0000 | $75.0000 |
| vercel_ai_gateway/anthropic/claude-opus-4.5 | $5.0000 | $25.0000 |
| vercel_ai_gateway/anthropic/claude-opus-4.6 | $5.0000 | $25.0000 |
| vercel_ai_gateway/anthropic/claude-sonnet-4 | $3.0000 | $15.0000 |
| vercel_ai_gateway/anthropic/claude-sonnet-4.5 | $3.0000 | $15.0000 |
| vercel_ai_gateway/cohere/command-a | $2.5000 | $10.0000 |
| vercel_ai_gateway/cohere/command-r | $0.1500 | $0.6000 |
| vercel_ai_gateway/cohere/command-r-plus | $2.5000 | $10.0000 |
| vercel_ai_gateway/cohere/embed-v4.0 | $0.1200 | $0.0000 |
| vercel_ai_gateway/deepseek/deepseek-r1 | $0.5500 | $2.1900 |
| vercel_ai_gateway/deepseek/deepseek-r1-distill-llama-70b | $0.7500 | $0.9900 |
| vercel_ai_gateway/deepseek/deepseek-v3 | $0.9000 | $0.9000 |
| vercel_ai_gateway/google/gemini-2.0-flash | $0.1500 | $0.6000 |
| vercel_ai_gateway/google/gemini-2.0-flash-lite | $0.0750 | $0.3000 |
| vercel_ai_gateway/google/gemini-2.5-flash | $0.3000 | $2.5000 |
| vercel_ai_gateway/google/gemini-2.5-pro | $2.5000 | $10.0000 |
| vercel_ai_gateway/google/gemma-2-9b | $0.2000 | $0.2000 |
| vercel_ai_gateway/inception/mercury-coder-small | $0.2500 | $1.0000 |
| vercel_ai_gateway/meta/llama-3-70b | $0.5900 | $0.7900 |
| vercel_ai_gateway/meta/llama-3-8b | $0.0500 | $0.0800 |
| vercel_ai_gateway/meta/llama-3.1-70b | $0.7200 | $0.7200 |
| vercel_ai_gateway/meta/llama-3.1-8b | $0.0500 | $0.0800 |
| vercel_ai_gateway/meta/llama-3.2-11b | $0.1600 | $0.1600 |
| vercel_ai_gateway/meta/llama-3.2-1b | $0.1000 | $0.1000 |
| vercel_ai_gateway/meta/llama-3.2-3b | $0.1500 | $0.1500 |
| vercel_ai_gateway/meta/llama-3.2-90b | $0.7200 | $0.7200 |
| vercel_ai_gateway/meta/llama-3.3-70b | $0.7200 | $0.7200 |
| vercel_ai_gateway/meta/llama-4-maverick | $0.2000 | $0.6000 |
| vercel_ai_gateway/meta/llama-4-scout | $0.1000 | $0.3000 |
| vercel_ai_gateway/mistral/codestral | $0.3000 | $0.9000 |
| vercel_ai_gateway/mistral/codestral-embed | $0.1500 | $0.0000 |
| vercel_ai_gateway/mistral/devstral-small | $0.0700 | $0.2800 |
| vercel_ai_gateway/mistral/magistral-medium | $2.0000 | $5.0000 |
| vercel_ai_gateway/mistral/magistral-small | $0.5000 | $1.5000 |
| vercel_ai_gateway/mistral/ministral-3b | $0.0400 | $0.0400 |
| vercel_ai_gateway/mistral/ministral-8b | $0.1000 | $0.1000 |
| vercel_ai_gateway/mistral/mistral-embed | $0.1000 | $0.0000 |
| vercel_ai_gateway/mistral/mistral-large | $2.0000 | $6.0000 |
| vercel_ai_gateway/mistral/mistral-saba-24b | $0.7900 | $0.7900 |
| vercel_ai_gateway/mistral/mistral-small | $0.1000 | $0.3000 |
| vercel_ai_gateway/mistral/mixtral-8x22b-instruct | $1.2000 | $1.2000 |
| vercel_ai_gateway/mistral/pixtral-12b | $0.1500 | $0.1500 |
| vercel_ai_gateway/mistral/pixtral-large | $2.0000 | $6.0000 |
| vercel_ai_gateway/moonshotai/kimi-k2 | $0.5500 | $2.2000 |
| vercel_ai_gateway/morph/morph-v3-fast | $0.8000 | $1.2000 |
| vercel_ai_gateway/morph/morph-v3-large | $0.9000 | $1.9000 |
| vercel_ai_gateway/openai/gpt-3.5-turbo | $0.5000 | $1.5000 |
| vercel_ai_gateway/openai/gpt-3.5-turbo-instruct | $1.5000 | $2.0000 |
| vercel_ai_gateway/openai/gpt-4-turbo | $10.0000 | $30.0000 |
| vercel_ai_gateway/openai/gpt-4.1 | $2.0000 | $8.0000 |
| vercel_ai_gateway/openai/gpt-4.1-mini | $0.4000 | $1.6000 |
| vercel_ai_gateway/openai/gpt-4.1-nano | $0.1000 | $0.4000 |
| vercel_ai_gateway/openai/gpt-4o | $2.5000 | $10.0000 |
| vercel_ai_gateway/openai/gpt-4o-mini | $0.1500 | $0.6000 |
| vercel_ai_gateway/openai/o1 | $15.0000 | $60.0000 |
| vercel_ai_gateway/openai/o3 | $2.0000 | $8.0000 |
| vercel_ai_gateway/openai/o3-mini | $1.1000 | $4.4000 |
| vercel_ai_gateway/openai/o4-mini | $1.1000 | $4.4000 |
| vercel_ai_gateway/perplexity/sonar | $1.0000 | $1.0000 |
| vercel_ai_gateway/perplexity/sonar-pro | $3.0000 | $15.0000 |
| vercel_ai_gateway/perplexity/sonar-reasoning | $1.0000 | $5.0000 |
| vercel_ai_gateway/perplexity/sonar-reasoning-pro | $2.0000 | $8.0000 |
| vercel_ai_gateway/vercel/v0-1.0-md | $3.0000 | $15.0000 |
| vercel_ai_gateway/vercel/v0-1.5-md | $3.0000 | $15.0000 |
| vercel_ai_gateway/xai/grok-2 | $2.0000 | $10.0000 |
| vercel_ai_gateway/xai/grok-2-vision | $2.0000 | $10.0000 |
| vercel_ai_gateway/xai/grok-3 | $3.0000 | $15.0000 |
| vercel_ai_gateway/xai/grok-3-fast | $5.0000 | $25.0000 |
| vercel_ai_gateway/xai/grok-3-mini | $0.3000 | $0.5000 |
| vercel_ai_gateway/xai/grok-3-mini-fast | $0.6000 | $4.0000 |
| vercel_ai_gateway/xai/grok-4 | $3.0000 | $15.0000 |
| vercel_ai_gateway/zai/glm-4.5 | $0.6000 | $2.2000 |
| vercel_ai_gateway/zai/glm-4.5-air | $0.2000 | $1.1000 |
| vercel_ai_gateway/zai/glm-4.6 | $0.4500 | $1.8000 |

## Vercel Ai Gateway — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| vercel_ai_gateway/google/gemini-embedding-001 | $0.1500 | $0.0000 |
| vercel_ai_gateway/google/text-embedding-005 | $0.0250 | $0.0000 |
| vercel_ai_gateway/google/text-multilingual-embedding-002 | $0.0250 | $0.0000 |
| vercel_ai_gateway/openai/text-embedding-3-large | $0.1300 | $0.0000 |
| vercel_ai_gateway/openai/text-embedding-3-small | $0.0200 | $0.0000 |
| vercel_ai_gateway/openai/text-embedding-ada-002 | $0.1000 | $0.0000 |

## Vertex Ai — audio_speech (per 1M characters)

| Model | Input | Output |
|-------|-------|--------|
| vertex_ai/chirp | $30.0000 | $0.0000 |

## Vertex Ai — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| vertex_ai/gemini-3-flash-preview | $0.5000 | $3.0000 |
| vertex_ai/gemini-3-pro-preview | $2.0000 | $12.0000 |
| vertex_ai/gemini-3.1-pro-preview | $2.0000 | $12.0000 |
| vertex_ai/gemini-3.1-pro-preview-customtools | $2.0000 | $12.0000 |

## Vertex Ai — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| vertex_ai/gemini-embedding-2-preview | $0.2000 | $0.0000 |

## Vertex Ai — ocr (per 1M pages)

| Model | Input | Output |
|-------|-------|--------|
| vertex_ai/deepseek-ai/deepseek-ocr-maas | $300.0000 | $0.0000 |
| vertex_ai/mistral-ocr-2505 | $500.0000 | $0.0000 |

## Vertex Ai — vector_store (per 1M queries)

| Model | Input | Output |
|-------|-------|--------|
| vertex_ai/search_api | $1500.0000 | $0.0000 |

## Vertex Ai-Deepseek Models — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| vertex_ai/deepseek-ai/deepseek-r1-0528-maas | $1.3500 | $5.4000 |
| vertex_ai/deepseek-ai/deepseek-v3.1-maas | $1.3500 | $5.4000 |
| vertex_ai/deepseek-ai/deepseek-v3.2-maas | $0.5600 | $1.6800 |

## Vertex Ai-Llama Models — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| vertex_ai/meta/llama-3.1-405b-instruct-maas | $5.0000 | $16.0000 |
| vertex_ai/meta/llama-4-maverick-17b-128e-instruct-maas | $0.3500 | $1.1500 |
| vertex_ai/meta/llama-4-maverick-17b-16e-instruct-maas | $0.3500 | $1.1500 |
| vertex_ai/meta/llama-4-scout-17b-128e-instruct-maas | $0.2500 | $0.7000 |
| vertex_ai/meta/llama-4-scout-17b-16e-instruct-maas | $0.2500 | $0.7000 |

## Vertex Ai-Minimax Models — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| vertex_ai/minimaxai/minimax-m2-maas | $0.3000 | $1.2000 |

## Vertex Ai-Moonshot Models — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| vertex_ai/moonshotai/kimi-k2-thinking-maas | $0.6000 | $2.5000 |

## Vertex Ai-Openai Models — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| vertex_ai/openai/gpt-oss-120b-maas | $0.1500 | $0.6000 |
| vertex_ai/openai/gpt-oss-20b-maas | $0.0750 | $0.3000 |

## Vertex Ai-Qwen Models — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| vertex_ai/qwen/qwen3-235b-a22b-instruct-2507-maas | $0.2500 | $1.0000 |
| vertex_ai/qwen/qwen3-coder-480b-a35b-instruct-maas | $1.0000 | $4.0000 |
| vertex_ai/qwen/qwen3-next-80b-a3b-instruct-maas | $0.1500 | $1.2000 |
| vertex_ai/qwen/qwen3-next-80b-a3b-thinking-maas | $0.1500 | $1.2000 |

## Vertex Ai-Video-Models — video_generation (per 1M seconds)

| Model | Input | Output |
|-------|-------|--------|
| vertex_ai/veo-2.0-generate-001 | $0.0000 | $350000.0000 |
| vertex_ai/veo-3.0-fast-generate-001 | $0.0000 | $150000.0000 |
| vertex_ai/veo-3.0-generate-001 | $0.0000 | $400000.0000 |
| vertex_ai/veo-3.1-fast-generate-001 | $0.0000 | $150000.0000 |
| vertex_ai/veo-3.1-fast-generate-preview | $0.0000 | $150000.0000 |
| vertex_ai/veo-3.1-generate-001 | $0.0000 | $400000.0000 |
| vertex_ai/veo-3.1-generate-preview | $0.0000 | $400000.0000 |

## Vertex Ai-Zai Models — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| vertex_ai/zai-org/glm-4.7-maas | $0.6000 | $2.2000 |
| vertex_ai/zai-org/glm-5-maas | $1.0000 | $3.2000 |

## Voyage — embedding (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| voyage/voyage-2 | $0.1000 | $0.0000 |
| voyage/voyage-3 | $0.0600 | $0.0000 |
| voyage/voyage-3-large | $0.1800 | $0.0000 |
| voyage/voyage-3-lite | $0.0200 | $0.0000 |
| voyage/voyage-3.5 | $0.0600 | $0.0000 |
| voyage/voyage-3.5-lite | $0.0200 | $0.0000 |
| voyage/voyage-code-2 | $0.1200 | $0.0000 |
| voyage/voyage-code-3 | $0.1800 | $0.0000 |
| voyage/voyage-context-3 | $0.1800 | $0.0000 |
| voyage/voyage-finance-2 | $0.1200 | $0.0000 |
| voyage/voyage-large-2 | $0.1200 | $0.0000 |
| voyage/voyage-law-2 | $0.1200 | $0.0000 |
| voyage/voyage-lite-01 | $0.1000 | $0.0000 |
| voyage/voyage-lite-02-instruct | $0.1000 | $0.0000 |
| voyage/voyage-multimodal-3 | $0.1200 | $0.0000 |

## Wandb — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| wandb/MiniMaxAI/MiniMax-M2.5 | $0.3000 | $1.2000 |
| wandb/Qwen/Qwen3-235B-A22B-Instruct-2507 | $10000.0000 | $10000.0000 |
| wandb/Qwen/Qwen3-235B-A22B-Thinking-2507 | $10000.0000 | $10000.0000 |
| wandb/Qwen/Qwen3-Coder-480B-A35B-Instruct | $100000.0000 | $150000.0000 |
| wandb/deepseek-ai/DeepSeek-R1-0528 | $135000.0000 | $540000.0000 |
| wandb/deepseek-ai/DeepSeek-V3-0324 | $114000.0000 | $275000.0000 |
| wandb/deepseek-ai/DeepSeek-V3.1 | $55000.0000 | $165000.0000 |
| wandb/meta-llama/Llama-3.1-8B-Instruct | $22000.0000 | $22000.0000 |
| wandb/meta-llama/Llama-3.3-70B-Instruct | $71000.0000 | $71000.0000 |
| wandb/meta-llama/Llama-4-Scout-17B-16E-Instruct | $17000.0000 | $66000.0000 |
| wandb/microsoft/Phi-4-mini-instruct | $8000.0000 | $35000.0000 |
| wandb/moonshotai/Kimi-K2-Instruct | $0.6000 | $2.5000 |
| wandb/moonshotai/Kimi-K2.5 | $0.6000 | $3.0000 |
| wandb/openai/gpt-oss-120b | $15000.0000 | $60000.0000 |
| wandb/openai/gpt-oss-20b | $5000.0000 | $20000.0000 |
| wandb/zai-org/GLM-4.5 | $55000.0000 | $200000.0000 |

## Zai — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| zai/glm-4-32b-0414-128k | $0.1000 | $0.1000 |
| zai/glm-4.5 | $0.6000 | $2.2000 |
| zai/glm-4.5-air | $0.2000 | $1.1000 |
| zai/glm-4.5-airx | $1.1000 | $4.5000 |
| zai/glm-4.5-x | $2.2000 | $8.9000 |
| zai/glm-4.5v | $0.6000 | $1.8000 |
| zai/glm-4.6 | $0.6000 | $2.2000 |
| zai/glm-4.7 | $0.6000 | $2.2000 |
| zai/glm-5 | $1.0000 | $3.2000 |
| zai/glm-5-code | $1.2000 | $5.0000 |

## xAI — chat (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| xai/grok-2 | $2.0000 | $10.0000 |
| xai/grok-2-1212 | $2.0000 | $10.0000 |
| xai/grok-2-latest | $2.0000 | $10.0000 |
| xai/grok-2-vision | $2.0000 | $10.0000 |
| xai/grok-2-vision-1212 | $2.0000 | $10.0000 |
| xai/grok-2-vision-latest | $2.0000 | $10.0000 |
| xai/grok-3 | $3.0000 | $15.0000 |
| xai/grok-3-beta | $3.0000 | $15.0000 |
| xai/grok-3-fast-beta | $5.0000 | $25.0000 |
| xai/grok-3-fast-latest | $5.0000 | $25.0000 |
| xai/grok-3-latest | $3.0000 | $15.0000 |
| xai/grok-3-mini | $0.3000 | $0.5000 |
| xai/grok-3-mini-beta | $0.3000 | $0.5000 |
| xai/grok-3-mini-fast | $0.6000 | $4.0000 |
| xai/grok-3-mini-fast-beta | $0.6000 | $4.0000 |
| xai/grok-3-mini-fast-latest | $0.6000 | $4.0000 |
| xai/grok-3-mini-latest | $0.3000 | $0.5000 |
| xai/grok-4 | $3.0000 | $15.0000 |
| xai/grok-4-0709 | $3.0000 | $15.0000 |
| xai/grok-4-1-fast | $0.2000 | $0.5000 |
| xai/grok-4-1-fast-non-reasoning | $0.2000 | $0.5000 |
| xai/grok-4-1-fast-non-reasoning-latest | $0.2000 | $0.5000 |
| xai/grok-4-1-fast-reasoning | $0.2000 | $0.5000 |
| xai/grok-4-1-fast-reasoning-latest | $0.2000 | $0.5000 |
| xai/grok-4-fast-non-reasoning | $0.2000 | $0.5000 |
| xai/grok-4-fast-reasoning | $0.2000 | $0.5000 |
| xai/grok-4-latest | $3.0000 | $15.0000 |
| xai/grok-4.20-0309-reasoning | $2.0000 | $6.0000 |
| xai/grok-4.20-beta-0309-non-reasoning | $2.0000 | $6.0000 |
| xai/grok-4.20-beta-0309-reasoning | $2.0000 | $6.0000 |
| xai/grok-4.20-multi-agent-beta-0309 | $2.0000 | $6.0000 |
| xai/grok-beta | $5.0000 | $15.0000 |
| xai/grok-code-fast | $0.2000 | $1.5000 |
| xai/grok-code-fast-1 | $0.2000 | $1.5000 |
| xai/grok-code-fast-1-0825 | $0.2000 | $1.5000 |
| xai/grok-vision-beta | $5.0000 | $15.0000 |

## OpenRouter — chat (per 1M tokens)

OpenRouter-routed pricing. Reflects what you'd pay routing through OpenRouter (may include markup vs direct-provider).

| Model | Input | Output |
|-------|-------|--------|
| openrouter/ai21/jamba-large-1.7 | $2.0000 | $8.0000 |
| openrouter/aion-labs/aion-1.0 | $4.0000 | $8.0000 |
| openrouter/aion-labs/aion-1.0-mini | $0.7000 | $1.4000 |
| openrouter/aion-labs/aion-2.0 | $0.8000 | $1.6000 |
| openrouter/aion-labs/aion-rp-llama-3.1-8b | $0.8000 | $1.6000 |
| openrouter/alfredpros/codellama-7b-instruct-solidity | $0.8000 | $1.2000 |
| openrouter/alibaba/tongyi-deepresearch-30b-a3b | $0.0900 | $0.4500 |
| openrouter/allenai/olmo-3-32b-think | $0.1500 | $0.5000 |
| openrouter/allenai/olmo-3.1-32b-instruct | $0.2000 | $0.6000 |
| openrouter/alpindale/goliath-120b | $3.7500 | $7.5000 |
| openrouter/amazon/nova-2-lite-v1 | $0.3000 | $2.5000 |
| openrouter/amazon/nova-lite-v1 | $0.0600 | $0.2400 |
| openrouter/amazon/nova-micro-v1 | $0.0350 | $0.1400 |
| openrouter/amazon/nova-premier-v1 | $2.5000 | $12.5000 |
| openrouter/amazon/nova-pro-v1 | $0.8000 | $3.2000 |
| openrouter/anthracite-org/magnum-v4-72b | $3.0000 | $5.0000 |
| openrouter/anthropic/claude-3-haiku | $0.2500 | $1.2500 |
| openrouter/anthropic/claude-3.5-haiku | $0.8000 | $4.0000 |
| openrouter/anthropic/claude-3.7-sonnet | $3.0000 | $15.0000 |
| openrouter/anthropic/claude-3.7-sonnet:thinking | $3.0000 | $15.0000 |
| openrouter/anthropic/claude-haiku-4.5 | $1.0000 | $5.0000 |
| openrouter/anthropic/claude-opus-4 | $15.0000 | $75.0000 |
| openrouter/anthropic/claude-opus-4.1 | $15.0000 | $75.0000 |
| openrouter/anthropic/claude-opus-4.5 | $5.0000 | $25.0000 |
| openrouter/anthropic/claude-opus-4.6 | $5.0000 | $25.0000 |
| openrouter/anthropic/claude-opus-4.6-fast | $30.0000 | $150.0000 |
| openrouter/anthropic/claude-opus-4.7 | $5.0000 | $25.0000 |
| openrouter/anthropic/claude-sonnet-4 | $3.0000 | $15.0000 |
| openrouter/anthropic/claude-sonnet-4.5 | $3.0000 | $15.0000 |
| openrouter/anthropic/claude-sonnet-4.6 | $3.0000 | $15.0000 |
| openrouter/arcee-ai/coder-large | $0.5000 | $0.8000 |
| openrouter/arcee-ai/maestro-reasoning | $0.9000 | $3.3000 |
| openrouter/arcee-ai/spotlight | $0.1800 | $0.1800 |
| openrouter/arcee-ai/trinity-large-thinking | $0.2200 | $0.8500 |
| openrouter/arcee-ai/trinity-mini | $0.0450 | $0.1500 |
| openrouter/arcee-ai/virtuoso-large | $0.7500 | $1.2000 |
| openrouter/baidu/ernie-4.5-21b-a3b | $0.0700 | $0.2800 |
| openrouter/baidu/ernie-4.5-21b-a3b-thinking | $0.0700 | $0.2800 |
| openrouter/baidu/ernie-4.5-300b-a47b | $0.2800 | $1.1000 |
| openrouter/baidu/ernie-4.5-vl-28b-a3b | $0.1400 | $0.5600 |
| openrouter/baidu/ernie-4.5-vl-424b-a47b | $0.4200 | $1.2500 |
| openrouter/bytedance-seed/seed-1.6 | $0.2500 | $2.0000 |
| openrouter/bytedance-seed/seed-1.6-flash | $0.0750 | $0.3000 |
| openrouter/bytedance-seed/seed-2.0-lite | $0.2500 | $2.0000 |
| openrouter/bytedance-seed/seed-2.0-mini | $0.1000 | $0.4000 |
| openrouter/bytedance/ui-tars-1.5-7b | $0.1000 | $0.2000 |
| openrouter/cohere/command-a | $2.5000 | $10.0000 |
| openrouter/cohere/command-r-08-2024 | $0.1500 | $0.6000 |
| openrouter/cohere/command-r-plus-08-2024 | $2.5000 | $10.0000 |
| openrouter/cohere/command-r7b-12-2024 | $0.0375 | $0.1500 |
| openrouter/deepcogito/cogito-v2.1-671b | $1.2500 | $1.2500 |
| openrouter/deepseek/deepseek-chat | $0.3200 | $0.8900 |
| openrouter/deepseek/deepseek-chat-v3-0324 | $0.2000 | $0.7700 |
| openrouter/deepseek/deepseek-chat-v3.1 | $0.1500 | $0.7500 |
| openrouter/deepseek/deepseek-r1 | $0.7000 | $2.5000 |
| openrouter/deepseek/deepseek-r1-0528 | $0.5000 | $2.1500 |
| openrouter/deepseek/deepseek-r1-distill-llama-70b | $0.7000 | $0.8000 |
| openrouter/deepseek/deepseek-r1-distill-qwen-32b | $0.2900 | $0.2900 |
| openrouter/deepseek/deepseek-v3.1-terminus | $0.2100 | $0.7900 |
| openrouter/deepseek/deepseek-v3.2 | $0.2520 | $0.3780 |
| openrouter/deepseek/deepseek-v3.2-exp | $0.2700 | $0.4100 |
| openrouter/deepseek/deepseek-v3.2-speciale | $0.4000 | $1.2000 |
| openrouter/essentialai/rnj-1-instruct | $0.1500 | $0.1500 |
| openrouter/google/gemini-2.0-flash-001 | $0.1000 | $0.4000 |
| openrouter/google/gemini-2.0-flash-lite-001 | $0.0750 | $0.3000 |
| openrouter/google/gemini-2.5-flash | $0.3000 | $2.5000 |
| openrouter/google/gemini-2.5-flash-image | $0.3000 | $2.5000 |
| openrouter/google/gemini-2.5-flash-lite | $0.1000 | $0.4000 |
| openrouter/google/gemini-2.5-flash-lite-preview-09-2025 | $0.1000 | $0.4000 |
| openrouter/google/gemini-2.5-pro | $1.2500 | $10.0000 |
| openrouter/google/gemini-2.5-pro-preview | $1.2500 | $10.0000 |
| openrouter/google/gemini-2.5-pro-preview-05-06 | $1.2500 | $10.0000 |
| openrouter/google/gemini-3-flash-preview | $0.5000 | $3.0000 |
| openrouter/google/gemini-3-pro-image-preview | $2.0000 | $12.0000 |
| openrouter/google/gemini-3.1-flash-image-preview | $0.5000 | $3.0000 |
| openrouter/google/gemini-3.1-flash-lite-preview | $0.2500 | $1.5000 |
| openrouter/google/gemini-3.1-pro-preview | $2.0000 | $12.0000 |
| openrouter/google/gemini-3.1-pro-preview-customtools | $2.0000 | $12.0000 |
| openrouter/google/gemma-2-27b-it | $0.6500 | $0.6500 |
| openrouter/google/gemma-3-12b-it | $0.0400 | $0.1300 |
| openrouter/google/gemma-3-27b-it | $0.0800 | $0.1600 |
| openrouter/google/gemma-3-4b-it | $0.0400 | $0.0800 |
| openrouter/google/gemma-3n-e4b-it | $0.0600 | $0.1200 |
| openrouter/google/gemma-4-26b-a4b-it | $0.0800 | $0.3500 |
| openrouter/google/gemma-4-31b-it | $0.1300 | $0.3800 |
| openrouter/gryphe/mythomax-l2-13b | $0.0600 | $0.0600 |
| openrouter/ibm-granite/granite-4.0-h-micro | $0.0170 | $0.1100 |
| openrouter/inception/mercury-2 | $0.2500 | $0.7500 |
| openrouter/inflection/inflection-3-pi | $2.5000 | $10.0000 |
| openrouter/inflection/inflection-3-productivity | $2.5000 | $10.0000 |
| openrouter/kwaipilot/kat-coder-pro-v2 | $0.3000 | $1.2000 |
| openrouter/liquid/lfm-2-24b-a2b | $0.0300 | $0.1200 |
| openrouter/mancer/weaver | $0.7500 | $1.0000 |
| openrouter/meta-llama/llama-3-70b-instruct | $0.5100 | $0.7400 |
| openrouter/meta-llama/llama-3-8b-instruct | $0.0300 | $0.0400 |
| openrouter/meta-llama/llama-3.1-70b-instruct | $0.4000 | $0.4000 |
| openrouter/meta-llama/llama-3.1-8b-instruct | $0.0200 | $0.0500 |
| openrouter/meta-llama/llama-3.2-11b-vision-instruct | $0.2450 | $0.2450 |
| openrouter/meta-llama/llama-3.2-1b-instruct | $0.0270 | $0.2000 |
| openrouter/meta-llama/llama-3.2-3b-instruct | $0.0510 | $0.3400 |
| openrouter/meta-llama/llama-3.3-70b-instruct | $0.1200 | $0.3800 |
| openrouter/meta-llama/llama-4-maverick | $0.1500 | $0.6000 |
| openrouter/meta-llama/llama-4-scout | $0.0800 | $0.3000 |
| openrouter/meta-llama/llama-guard-3-8b | $0.4800 | $0.0300 |
| openrouter/meta-llama/llama-guard-4-12b | $0.1800 | $0.1800 |
| openrouter/microsoft/phi-4 | $0.0650 | $0.1400 |
| openrouter/microsoft/wizardlm-2-8x22b | $0.6200 | $0.6200 |
| openrouter/minimax/minimax-01 | $0.2000 | $1.1000 |
| openrouter/minimax/minimax-m1 | $0.4000 | $2.2000 |
| openrouter/minimax/minimax-m2 | $0.2550 | $1.0000 |
| openrouter/minimax/minimax-m2-her | $0.3000 | $1.2000 |
| openrouter/minimax/minimax-m2.1 | $0.2900 | $0.9500 |
| openrouter/minimax/minimax-m2.5 | $0.1500 | $1.2000 |
| openrouter/minimax/minimax-m2.7 | $0.3000 | $1.2000 |
| openrouter/mistralai/codestral-2508 | $0.3000 | $0.9000 |
| openrouter/mistralai/devstral-2512 | $0.4000 | $2.0000 |
| openrouter/mistralai/devstral-medium | $0.4000 | $2.0000 |
| openrouter/mistralai/devstral-small | $0.1000 | $0.3000 |
| openrouter/mistralai/ministral-14b-2512 | $0.2000 | $0.2000 |
| openrouter/mistralai/ministral-3b-2512 | $0.1000 | $0.1000 |
| openrouter/mistralai/ministral-8b-2512 | $0.1500 | $0.1500 |
| openrouter/mistralai/mistral-7b-instruct-v0.1 | $0.1100 | $0.1900 |
| openrouter/mistralai/mistral-large | $2.0000 | $6.0000 |
| openrouter/mistralai/mistral-large-2407 | $2.0000 | $6.0000 |
| openrouter/mistralai/mistral-large-2411 | $2.0000 | $6.0000 |
| openrouter/mistralai/mistral-large-2512 | $0.5000 | $1.5000 |
| openrouter/mistralai/mistral-medium-3 | $0.4000 | $2.0000 |
| openrouter/mistralai/mistral-medium-3.1 | $0.4000 | $2.0000 |
| openrouter/mistralai/mistral-nemo | $0.0200 | $0.0400 |
| openrouter/mistralai/mistral-saba | $0.2000 | $0.6000 |
| openrouter/mistralai/mistral-small-24b-instruct-2501 | $0.0500 | $0.0800 |
| openrouter/mistralai/mistral-small-2603 | $0.1500 | $0.6000 |
| openrouter/mistralai/mistral-small-3.1-24b-instruct | $0.3500 | $0.5600 |
| openrouter/mistralai/mistral-small-3.2-24b-instruct | $0.0750 | $0.2000 |
| openrouter/mistralai/mistral-small-creative | $0.1000 | $0.3000 |
| openrouter/mistralai/mixtral-8x22b-instruct | $2.0000 | $6.0000 |
| openrouter/mistralai/mixtral-8x7b-instruct | $0.5400 | $0.5400 |
| openrouter/mistralai/pixtral-large-2411 | $2.0000 | $6.0000 |
| openrouter/mistralai/voxtral-small-24b-2507 | $0.1000 | $0.3000 |
| openrouter/moonshotai/kimi-k2 | $0.5700 | $2.3000 |
| openrouter/moonshotai/kimi-k2-0905 | $0.4000 | $2.0000 |
| openrouter/moonshotai/kimi-k2-thinking | $0.6000 | $2.5000 |
| openrouter/moonshotai/kimi-k2.5 | $0.4400 | $2.0000 |
| openrouter/moonshotai/kimi-k2.6 | $0.6000 | $2.8000 |
| openrouter/morph/morph-v3-fast | $0.8000 | $1.2000 |
| openrouter/morph/morph-v3-large | $0.9000 | $1.9000 |
| openrouter/nex-agi/deepseek-v3.1-nex-n1 | $0.1350 | $0.5000 |
| openrouter/nousresearch/hermes-2-pro-llama-3-8b | $0.1400 | $0.1400 |
| openrouter/nousresearch/hermes-3-llama-3.1-405b | $1.0000 | $1.0000 |
| openrouter/nousresearch/hermes-3-llama-3.1-70b | $0.3000 | $0.3000 |
| openrouter/nousresearch/hermes-4-405b | $1.0000 | $3.0000 |
| openrouter/nousresearch/hermes-4-70b | $0.1300 | $0.4000 |
| openrouter/nvidia/llama-3.1-nemotron-70b-instruct | $1.2000 | $1.2000 |
| openrouter/nvidia/llama-3.3-nemotron-super-49b-v1.5 | $0.1000 | $0.4000 |
| openrouter/nvidia/nemotron-3-nano-30b-a3b | $0.0500 | $0.2000 |
| openrouter/nvidia/nemotron-3-super-120b-a12b | $0.0900 | $0.4500 |
| openrouter/nvidia/nemotron-nano-12b-v2-vl | $0.2000 | $0.6000 |
| openrouter/nvidia/nemotron-nano-9b-v2 | $0.0400 | $0.1600 |
| openrouter/openai/gpt-3.5-turbo | $0.5000 | $1.5000 |
| openrouter/openai/gpt-3.5-turbo-0613 | $1.0000 | $2.0000 |
| openrouter/openai/gpt-3.5-turbo-16k | $3.0000 | $4.0000 |
| openrouter/openai/gpt-3.5-turbo-instruct | $1.5000 | $2.0000 |
| openrouter/openai/gpt-4 | $30.0000 | $60.0000 |
| openrouter/openai/gpt-4-0314 | $30.0000 | $60.0000 |
| openrouter/openai/gpt-4-1106-preview | $10.0000 | $30.0000 |
| openrouter/openai/gpt-4-turbo | $10.0000 | $30.0000 |
| openrouter/openai/gpt-4-turbo-preview | $10.0000 | $30.0000 |
| openrouter/openai/gpt-4.1 | $2.0000 | $8.0000 |
| openrouter/openai/gpt-4.1-mini | $0.4000 | $1.6000 |
| openrouter/openai/gpt-4.1-nano | $0.1000 | $0.4000 |
| openrouter/openai/gpt-4o | $2.5000 | $10.0000 |
| openrouter/openai/gpt-4o-2024-05-13 | $5.0000 | $15.0000 |
| openrouter/openai/gpt-4o-2024-08-06 | $2.5000 | $10.0000 |
| openrouter/openai/gpt-4o-2024-11-20 | $2.5000 | $10.0000 |
| openrouter/openai/gpt-4o-audio-preview | $2.5000 | $10.0000 |
| openrouter/openai/gpt-4o-mini | $0.1500 | $0.6000 |
| openrouter/openai/gpt-4o-mini-2024-07-18 | $0.1500 | $0.6000 |
| openrouter/openai/gpt-4o-mini-search-preview | $0.1500 | $0.6000 |
| openrouter/openai/gpt-4o-search-preview | $2.5000 | $10.0000 |
| openrouter/openai/gpt-5 | $1.2500 | $10.0000 |
| openrouter/openai/gpt-5-chat | $1.2500 | $10.0000 |
| openrouter/openai/gpt-5-codex | $1.2500 | $10.0000 |
| openrouter/openai/gpt-5-image | $10.0000 | $10.0000 |
| openrouter/openai/gpt-5-image-mini | $2.5000 | $2.0000 |
| openrouter/openai/gpt-5-mini | $0.2500 | $2.0000 |
| openrouter/openai/gpt-5-nano | $0.0500 | $0.4000 |
| openrouter/openai/gpt-5-pro | $15.0000 | $120.0000 |
| openrouter/openai/gpt-5.1 | $1.2500 | $10.0000 |
| openrouter/openai/gpt-5.1-chat | $1.2500 | $10.0000 |
| openrouter/openai/gpt-5.1-codex | $1.2500 | $10.0000 |
| openrouter/openai/gpt-5.1-codex-max | $1.2500 | $10.0000 |
| openrouter/openai/gpt-5.1-codex-mini | $0.2500 | $2.0000 |
| openrouter/openai/gpt-5.2 | $1.7500 | $14.0000 |
| openrouter/openai/gpt-5.2-chat | $1.7500 | $14.0000 |
| openrouter/openai/gpt-5.2-codex | $1.7500 | $14.0000 |
| openrouter/openai/gpt-5.2-pro | $21.0000 | $168.0000 |
| openrouter/openai/gpt-5.3-chat | $1.7500 | $14.0000 |
| openrouter/openai/gpt-5.3-codex | $1.7500 | $14.0000 |
| openrouter/openai/gpt-5.4 | $2.5000 | $15.0000 |
| openrouter/openai/gpt-5.4-mini | $0.7500 | $4.5000 |
| openrouter/openai/gpt-5.4-nano | $0.2000 | $1.2500 |
| openrouter/openai/gpt-5.4-pro | $30.0000 | $180.0000 |
| openrouter/openai/gpt-audio | $2.5000 | $10.0000 |
| openrouter/openai/gpt-audio-mini | $0.6000 | $2.4000 |
| openrouter/openai/gpt-oss-120b | $0.0390 | $0.1900 |
| openrouter/openai/gpt-oss-20b | $0.0300 | $0.1400 |
| openrouter/openai/gpt-oss-safeguard-20b | $0.0750 | $0.3000 |
| openrouter/openai/o1 | $15.0000 | $60.0000 |
| openrouter/openai/o1-pro | $150.0000 | $600.0000 |
| openrouter/openai/o3 | $2.0000 | $8.0000 |
| openrouter/openai/o3-deep-research | $10.0000 | $40.0000 |
| openrouter/openai/o3-mini | $1.1000 | $4.4000 |
| openrouter/openai/o3-mini-high | $1.1000 | $4.4000 |
| openrouter/openai/o3-pro | $20.0000 | $80.0000 |
| openrouter/openai/o4-mini | $1.1000 | $4.4000 |
| openrouter/openai/o4-mini-deep-research | $2.0000 | $8.0000 |
| openrouter/openai/o4-mini-high | $1.1000 | $4.4000 |
| openrouter/perplexity/sonar | $1.0000 | $1.0000 |
| openrouter/perplexity/sonar-deep-research | $2.0000 | $8.0000 |
| openrouter/perplexity/sonar-pro | $3.0000 | $15.0000 |
| openrouter/perplexity/sonar-pro-search | $3.0000 | $15.0000 |
| openrouter/perplexity/sonar-reasoning-pro | $2.0000 | $8.0000 |
| openrouter/prime-intellect/intellect-3 | $0.2000 | $1.1000 |
| openrouter/qwen/qwen-2.5-72b-instruct | $0.1200 | $0.3900 |
| openrouter/qwen/qwen-2.5-7b-instruct | $0.0400 | $0.1000 |
| openrouter/qwen/qwen-2.5-coder-32b-instruct | $0.6600 | $1.0000 |
| openrouter/qwen/qwen-max | $1.0400 | $4.1600 |
| openrouter/qwen/qwen-plus | $0.2600 | $0.7800 |
| openrouter/qwen/qwen-plus-2025-07-28 | $0.2600 | $0.7800 |
| openrouter/qwen/qwen-plus-2025-07-28:thinking | $0.2600 | $0.7800 |
| openrouter/qwen/qwen-turbo | $0.0325 | $0.1300 |
| openrouter/qwen/qwen-vl-max | $0.5200 | $2.0800 |
| openrouter/qwen/qwen-vl-plus | $0.1365 | $0.4095 |
| openrouter/qwen/qwen2.5-vl-72b-instruct | $0.2500 | $0.7500 |
| openrouter/qwen/qwen3-14b | $0.0600 | $0.2400 |
| openrouter/qwen/qwen3-235b-a22b | $0.4550 | $1.8200 |
| openrouter/qwen/qwen3-235b-a22b-2507 | $0.0710 | $0.1000 |
| openrouter/qwen/qwen3-235b-a22b-thinking-2507 | $0.1300 | $0.6000 |
| openrouter/qwen/qwen3-30b-a3b | $0.0800 | $0.2800 |
| openrouter/qwen/qwen3-30b-a3b-instruct-2507 | $0.0900 | $0.3000 |
| openrouter/qwen/qwen3-30b-a3b-thinking-2507 | $0.0800 | $0.4000 |
| openrouter/qwen/qwen3-32b | $0.0800 | $0.2400 |
| openrouter/qwen/qwen3-8b | $0.0500 | $0.4000 |
| openrouter/qwen/qwen3-coder | $0.2200 | $1.0000 |
| openrouter/qwen/qwen3-coder-30b-a3b-instruct | $0.0700 | $0.2700 |
| openrouter/qwen/qwen3-coder-flash | $0.1950 | $0.9750 |
| openrouter/qwen/qwen3-coder-next | $0.1500 | $0.8000 |
| openrouter/qwen/qwen3-coder-plus | $0.6500 | $3.2500 |
| openrouter/qwen/qwen3-max | $0.7800 | $3.9000 |
| openrouter/qwen/qwen3-max-thinking | $0.7800 | $3.9000 |
| openrouter/qwen/qwen3-next-80b-a3b-instruct | $0.0900 | $1.1000 |
| openrouter/qwen/qwen3-next-80b-a3b-thinking | $0.0975 | $0.7800 |
| openrouter/qwen/qwen3-vl-235b-a22b-instruct | $0.2000 | $0.8800 |
| openrouter/qwen/qwen3-vl-235b-a22b-thinking | $0.2600 | $2.6000 |
| openrouter/qwen/qwen3-vl-30b-a3b-instruct | $0.1300 | $0.5200 |
| openrouter/qwen/qwen3-vl-30b-a3b-thinking | $0.1300 | $1.5600 |
| openrouter/qwen/qwen3-vl-32b-instruct | $0.1040 | $0.4160 |
| openrouter/qwen/qwen3-vl-8b-instruct | $0.0800 | $0.5000 |
| openrouter/qwen/qwen3-vl-8b-thinking | $0.1170 | $1.3650 |
| openrouter/qwen/qwen3.5-122b-a10b | $0.2600 | $2.0800 |
| openrouter/qwen/qwen3.5-27b | $0.1950 | $1.5600 |
| openrouter/qwen/qwen3.5-35b-a3b | $0.1625 | $1.3000 |
| openrouter/qwen/qwen3.5-397b-a17b | $0.3900 | $2.3400 |
| openrouter/qwen/qwen3.5-9b | $0.1000 | $0.1500 |
| openrouter/qwen/qwen3.5-flash-02-23 | $0.0650 | $0.2600 |
| openrouter/qwen/qwen3.5-plus-02-15 | $0.2600 | $1.5600 |
| openrouter/qwen/qwen3.6-plus | $0.3250 | $1.9500 |
| openrouter/qwen/qwq-32b | $0.1500 | $0.5800 |
| openrouter/rekaai/reka-edge | $0.1000 | $0.1000 |
| openrouter/rekaai/reka-flash-3 | $0.1000 | $0.2000 |
| openrouter/relace/relace-apply-3 | $0.8500 | $1.2500 |
| openrouter/relace/relace-search | $1.0000 | $3.0000 |
| openrouter/sao10k/l3-euryale-70b | $1.4800 | $1.4800 |
| openrouter/sao10k/l3-lunaris-8b | $0.0400 | $0.0500 |
| openrouter/sao10k/l3.1-70b-hanami-x1 | $3.0000 | $3.0000 |
| openrouter/sao10k/l3.1-euryale-70b | $0.8500 | $0.8500 |
| openrouter/sao10k/l3.3-euryale-70b | $0.6500 | $0.7500 |
| openrouter/stepfun/step-3.5-flash | $0.1000 | $0.3000 |
| openrouter/switchpoint/router | $0.8500 | $3.4000 |
| openrouter/tencent/hunyuan-a13b-instruct | $0.1400 | $0.5700 |
| openrouter/thedrummer/cydonia-24b-v4.1 | $0.3000 | $0.5000 |
| openrouter/thedrummer/rocinante-12b | $0.1700 | $0.4300 |
| openrouter/thedrummer/skyfall-36b-v2 | $0.5500 | $0.8000 |
| openrouter/thedrummer/unslopnemo-12b | $0.4000 | $0.4000 |
| openrouter/tngtech/deepseek-r1t2-chimera | $0.3000 | $1.1000 |
| openrouter/undi95/remm-slerp-l2-13b | $0.4500 | $0.6500 |
| openrouter/upstage/solar-pro-3 | $0.1500 | $0.6000 |
| openrouter/writer/palmyra-x5 | $0.6000 | $6.0000 |
| openrouter/x-ai/grok-3 | $3.0000 | $15.0000 |
| openrouter/x-ai/grok-3-beta | $3.0000 | $15.0000 |
| openrouter/x-ai/grok-3-mini | $0.3000 | $0.5000 |
| openrouter/x-ai/grok-3-mini-beta | $0.3000 | $0.5000 |
| openrouter/x-ai/grok-4 | $3.0000 | $15.0000 |
| openrouter/x-ai/grok-4-fast | $0.2000 | $0.5000 |
| openrouter/x-ai/grok-4.1-fast | $0.2000 | $0.5000 |
| openrouter/x-ai/grok-4.20 | $2.0000 | $6.0000 |
| openrouter/x-ai/grok-4.20-multi-agent | $2.0000 | $6.0000 |
| openrouter/x-ai/grok-code-fast-1 | $0.2000 | $1.5000 |
| openrouter/xiaomi/mimo-v2-flash | $0.0900 | $0.2900 |
| openrouter/xiaomi/mimo-v2-omni | $0.4000 | $2.0000 |
| openrouter/xiaomi/mimo-v2-pro | $1.0000 | $3.0000 |
| openrouter/z-ai/glm-4-32b | $0.1000 | $0.1000 |
| openrouter/z-ai/glm-4.5 | $0.6000 | $2.2000 |
| openrouter/z-ai/glm-4.5-air | $0.1300 | $0.8500 |
| openrouter/z-ai/glm-4.5v | $0.6000 | $1.8000 |
| openrouter/z-ai/glm-4.6 | $0.3900 | $1.9000 |
| openrouter/z-ai/glm-4.6v | $0.3000 | $0.9000 |
| openrouter/z-ai/glm-4.7 | $0.3800 | $1.7400 |
| openrouter/z-ai/glm-4.7-flash | $0.0600 | $0.4000 |
| openrouter/z-ai/glm-5 | $0.7200 | $2.3000 |
| openrouter/z-ai/glm-5-turbo | $1.2000 | $4.0000 |
| openrouter/z-ai/glm-5.1 | $0.6980 | $4.4000 |
| openrouter/z-ai/glm-5v-turbo | $1.2000 | $4.0000 |

## Token Estimation Rules of Thumb

- 1 token ~ 4 characters (English)
- 1 token ~ 0.75 words (English)
- 1 page of text ~ 500 tokens
- 1 line of code ~ 10-20 tokens
- JSON/structured output uses ~30% more tokens than plain text
