# Examples

Four files. `client.py` is imported by the other three, so run them from this
directory.

```bash
pip install httpx
export ORACLE_X_URL=http://localhost:8000     # default; set for a remote instance
export ORACLE_X_TOKEN=...                     # only for 03_chat_job.py

python client.py                              # connectivity + upstream health
python 01_asset_workup.py ETHUSDT             # one asset, four views, one round trip
python 02_news_thesis.py                      # headline → analysis → precedent
python 03_chat_job.py "What should I watch this week?"
```

| File | Pattern it demonstrates |
|---|---|
| `client.py` | Base URL and token from the environment; 404 / 401 / 503 given distinct meanings. |
| `01_asset_workup.py` | Independent endpoints issued concurrently; a 404 recorded as an absence rather than dropped. |
| `02_news_thesis.py` | Check the cache before starting a job; job polling with a deadline. |
| `03_chat_job.py` | Provider check before spending a turn; step reporting while the job runs. |

The response-shape handling is deliberately tolerant — several routes do not
declare a response model, so the examples reach for a couple of plausible field
names rather than asserting one. Read one real payload before building anything
that depends on an exact key.
