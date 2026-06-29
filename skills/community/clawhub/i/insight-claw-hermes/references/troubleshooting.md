# Insight Claw Troubleshooting

Use this reference after the main no-notification validation path fails or produces incomplete results.

## Missing LLM Configuration

A missing LLM credential blocks real structured analysis. Use Hermes secret handling, the user's existing environment, or a user-approved local `.env` merge for `AIHUBMIX_KEY` or `OPENAI_API_KEY`. Never display, transmit, upload, or commit raw secret values.

## Dependency Installation Fails

Confirm Python 3.11+ is available, the virtual environment is active or explicitly addressed through `.venv/bin/python`, and dependencies are installed from `requirements.txt`.

The setup flow compares default PyPI with the Tsinghua mirror before dependency installation using `pip download --no-cache-dir --no-deps`, because `pip index versions` only checks metadata and does not measure wheel download speed. If package access is slow or failing, rerun that download probe, then retry with `-i https://pypi.tuna.tsinghua.edu.cn/simple` only for the current install command when the mirror is faster or default PyPI fails. Do not write global pip configuration.

## Data Provider Gaps

Some 行情数据 sources may fail or be rate-limited. Treat this as possible degradation chain behavior until every configured provider has failed.

## Optional Enhancement Gaps

Missing search intelligence, chip distribution, or 同花顺专业数据模式 credentials can reduce context but should not be described as a full setup failure when the core analysis path still runs.

## Notification Failures

Notification failures should be isolated from report generation. First verify local analysis reports and batch summaries under `reports/YYYY-MM-DD/`, then retry Telegram or Feishu configuration.

## Empty or Incomplete Reports

Check `run_meta.json` for success and failure counts. Then inspect single-stock JSON files before rerunning the whole batch.

## Security

Do not upload `.env`, generated reports, notification payloads, or raw model inputs without explicit user approval.
