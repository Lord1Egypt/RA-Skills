# MySQL setup and acceptance (v0.9.8+)

> 本指南适用于 0.9.8。使用 PyPI 安装同版本 CLI 与 MySQL extra，手工导入 Skill 时使用对应的 0.9.8 Release 产物，并确认运行服务已重启到同一版本。

Use an isolated project home and a dedicated MySQL 8.4+ test database. The
registry and business data both support MySQL; HTML remains in local files or
the configured object storage. Settings, audit and service state stay local.

## Install in the agent's actual environment

Run OS, Python and executable-path probes first. Create a project virtual
environment with Python 3.9+ and install the exact version:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade 'html-golive[mysql]==0.9.8'
.venv/bin/golive --version
.venv/bin/golive skill install --target .codebuddy/skills
.venv/bin/golive skill status
```

These are macOS/Linux paths. On Windows use `.venv\Scripts\python.exe` and
`.venv\Scripts\golive.exe` (and create the environment with `py -3` if needed).
Every subsequent `golive` command must use this same virtual environment.
Do not silently use another globally installed CLI.

WorkBuddy project skills live in `.codebuddy/skills/<skill-name>/SKILL.md`.
Open this directory as a WorkBuddy project and reload/reopen its task so the
skill is actually loaded. Verify the loaded name is `html-golive` and its
version is `0.9.8`. For other agents, use their documented skills directory
with `--target`; the target is the **parent** of `html-golive`, not the skill
folder itself. `--force` backs up an old installed copy before replacing it.

## Database and credentials

Use an existing authorized test DSN if available. Otherwise, when Docker is
available, provision an isolated `mysql:8.4` container with a dedicated database
and app user, a new volume, and a free port bound to `127.0.0.1`. Supply random
passwords through a private local env file or secret manager. Never reuse or
clear an existing database/container. If there is no Docker or test database,
ask for the host/port/database/user and the local credential-file location;
do not substitute SQLite.

Set `GOLIVE_MYSQL_DSN` in the environment of **every CLI invocation and the
background server**. Shape only (replace placeholders locally):

```text
mysql://user:URL_ENCODED_PASSWORD@127.0.0.1:3307/database
```

Keep the DSN out of HTML, git, screenshots and shared logs. URL-encode reserved
characters in credentials. Remote connections verify certificates and hostnames;
use `?ssl_ca=/absolute/path/ca.pem` for a custom CA. The app user needs DDL and
CRUD grants on this dedicated database. MySQL is not installed by the pip extra.

## Configure and initialize

Use a new project directory, set `GOLIVE_HOME` to its absolute `runtime` path,
and set `GOLIVE_CONFIG` to the absolute path of this `golive.yaml`:

```yaml
server:
  host: 127.0.0.1
  port: 8788
storage:
  backend: local
registry:
  backend: mysql
  mysql:
    dsn_env: GOLIVE_MYSQL_DSN
data:
  backend: mysql
  templates_table: golive_templates
```

If 8788 is occupied, choose a free port and use it consistently. In the same
environment (with the DSN already loaded), run:

```bash
golive db init
golive context
golive serve start --host 127.0.0.1 --port 8788
golive doctor --port 8788 --json
golive verify --json
```

Use `db init` for the configured MySQL tables; the general `init` quickstart is
not needed here. Confirm `registry.backend` and `data.backend` are both mysql,
CLI/skill/running-service versions are all 0.9.8, doctor reports MySQL, and
verify returns `ok: true` with exit code 0. A running service retains its
startup environment: after changing the DSN, stop/start it with that env loaded.

## Prove the entire path

1. Choose a unique model code such as `workbuddy_mysql_097_<timestamp>`.
2. Exercise `golive data create/list/get/update/upsert/delete` with Chinese,
   emoji and nested JSON. Capture IDs from `data list` JSON. Updating/upserting
   the same name/user must retain its ID; deletion must remove the record.
3. Generate the note page from SKILL.md's page skeleton, publish it with
   `--data-model <model>` and a unique `--slug`, and serve it through golive.
4. In a **real browser**, create, read, update, upsert, sort, paginate and
   delete using `window.TemplateAPI`. Write arguments are `name` and `content`;
   read results use `templateId` and `templateContent` (JSON string). Wait for
   `templateapi:ready`. Reload the page and restart only this test service;
   retained notes must still exist.
5. Check `/admin` data management and the MySQL connection test. The connection
   probe must pass read/write and leave no extra row after rollback.
6. Independently query the MySQL server and this model's rows. For example,
   run the following using the same virtualenv and DSN, replacing the model:

```python
import json
from golive.backends._mysql import mysql_connect

with mysql_connect() as db:
    server = db.execute('SELECT VERSION() AS version, DATABASE() AS database_name').fetchone()
    rows = db.execute('SELECT id, name, content FROM golive_templates WHERE model_code=%s',
                      ('YOUR_UNIQUE_TEST_MODEL',)).fetchall()
print(json.dumps({'server': server, 'test_rows': rows}, ensure_ascii=False, default=str))
```

Do not run this acceptance in production: `verify` creates/removes a probe page
and row, while manual acceptance intentionally leaves synthetic notes for the
user to inspect. Do not run repository-wide tests against the user's database;
some old test suites clear fixed tables.

## Report and handoff

Return the actual CLI/skill/server/MySQL versions, executable path, effective
backend names, test model, real page/admin URLs, pass/fail checklist and SQL
proof. Redact credentials. State separately what was tested through CLI, SQL
and browser. If browser tooling is unavailable, mark browser acceptance as
pending; a successful HTTP request is not browser execution.

Leave the isolated page, service and test database available for user review.
Provide `golive serve stop` and the exact scoped container/volume cleanup
commands, but do not remove them before review. Report any skipped/failed step
with the original error (secrets removed); never claim a fallback backend passed.


## 源码后续改进（尚未发布）

新代码支持 `golive context --json` 自动选择配置/服务端口并展示来源，后台默认测试当前后端。
`golive data sort --id <id> --sort-index 100 --json` 调整排序，
`golive data list --page-no 2 --page-size 10` 检查分页，写入支持 `--json`。
安装源码的 `[verify]` 扩展后，使用 `golive verify --full --json --report-dir <新目录>`，
或加 `--browser-channel chrome`，执行真实浏览器、SQL 证据、后台回滚及重启持久化验收。
每项都会标注 passed/failed/skipped；基础 verify 的 ok:true 只代表基础覆盖。
隔离数据库脚本位于源码 `scripts/mysql_sandbox.py`，详细边界、凭证与清理说明见
[完整验收说明](https://github.com/Songhonglei/html-golive/blob/main/docs/acceptance.md)。
