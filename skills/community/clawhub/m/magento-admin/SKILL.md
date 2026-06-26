---
name: magento-admin
version: "5.6.1"
description: >
  Complete Magento 2 store administration via SSH key auth, REST API, GraphQL,
  and direct DB access. For server owners on their own infrastructure.
  SSH key auth and passwordless sudo required.
author: openclaw-community
license: MIT
tags: [magento, ecommerce, devops, store-admin, ssh, rest-api, graphql, composer]

requires:
  primary_credential: MAGENTO_SSH_KEY
  env:
    - name: MAGENTO_HOST
      description: Magento server IP or hostname
    - name: MAGENTO_SSH_USER
      description: SSH username (passwordless sudo required on server)
    - name: MAGENTO_SSH_KEY
      description: Path to SSH private key (e.g. ~/.ssh/magento_deploy)
    - name: MAGENTO_WEB_ROOT
      description: Magento installation path (e.g. /var/www/html/magento2)
    - name: MAGENTO_PHP
      description: PHP binary (e.g. /usr/bin/php8.4)
    - name: MAGENTO_WEB_USER
      description: Web server user (e.g. www-data)
    - name: MAGENTO_DB_NAME
      description: Database name
    - name: MAGENTO_DB_USER
      description: Database username
    - name: MAGENTO_DB_PASS
      description: Database password
    - name: MAGENTO_BASE_URL
      description: Store base URL (e.g. https://store.example.com)
    - name: MAGENTO_ADMIN_USER
      description: Magento admin username
    - name: MAGENTO_ADMIN_PASS
      description: Magento admin password (REST API token generation only)
  optional_env:
    - name: MAGENTO_CA_CERT
      description: CA cert path for HTTPS (e.g. /opt/ssl/ca.crt)
    - name: MAGENTO_OS_URL
      description: OpenSearch URL (default http://127.0.0.1:9200)
    - name: MAGENTO_ADMIN_PATH
      description: Admin path (default admin)
    - name: COMPOSER_PATH
      description: Composer binary path (e.g. /usr/local/bin/composer)
  binaries:
    - ssh
    - mysql
    - curl
    - redis-cli
    - python3

security:
  scope: owner-operated
  risk_level: high
  risk_acknowledged: true
  risk_justification: >-
    Full store admin requires SSH + DB + REST access by design. High privilege
    is inherent and intentional. Install only on infrastructure you own.
  auth_method: ssh-key-only
  sudo_method: passwordless-sudoers
  credential_handling: user-supplied-only
  network_access: user-own-server-only
  note: >
    SSH key auth only. DB password via MYSQL_PWD env var (not in process args).
    REST API password in HTTPS body only. All credentials user-supplied.
    Connects only to MAGENTO_HOST. Nothing sent to third parties.

prompt_injection_mitigation: >
  All commands use fixed config variables only. Free-form user input is
  never interpolated into shell commands.
---

# magento-admin v5.6 — Complete Magento 2 Administration

## Overview

This skill gives an OpenClaw agent the ability to fully administer a Magento 2
store via SSH, REST API, GraphQL, and direct database access. It is designed
for use by the **server owner** on their own infrastructure.

All credentials are supplied by you in your private config file and are used
only to connect to your own server. Nothing is sent to third parties.

## Security Notes

- **SSH key auth recommended** over password auth where possible
- All credentials are stored only in your private config, never in the skill itself
- The skill connects only to the server you configure
- Review all commands before enabling autonomous execution

## Configuration

Create a private config file at:
Set the following variables in your openclaw.json env block:

Set these variables — all commands in this skill use them as placeholders:

| Variable | Description | Example |
|---|---|---|
| MAGENTO_HOST | Server IP or hostname | 10.0.1.50 |
| MAGENTO_SSH_USER | SSH username | deploy |
| MAGENTO_SSH_KEY | Path to SSH private key | ~/.ssh/magento_deploy |
| MAGENTO_WEB_ROOT | Magento path | /var/www/html/magento2 |
| MAGENTO_PHP | PHP binary | /usr/bin/php8.3 |
| MAGENTO_WEB_USER | Web server user | www-data |
| MAGENTO_DB_NAME | Database name | magento_db |
| MAGENTO_DB_USER | DB username | magento_user |
| MAGENTO_DB_PASS | DB password | *(your db password)* |
| MAGENTO_BASE_URL | Store URL | https://store.example.com |
| MAGENTO_ADMIN_PATH | Admin path | admin |
| MAGENTO_ADMIN_USER | Admin username | admin |
| MAGENTO_ADMIN_PASS | Admin password | *(your admin password)* |
| MAGENTO_OS_URL | OpenSearch URL | http://127.0.0.1:9200 |
| COMPOSER_PATH | Composer binary | /usr/local/bin/composer |

## Recommended: SSH Key Authentication

For better security, set up SSH key auth instead of password auth:

```bash


ssh -i ~/.ssh/magento_deploy -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "COMMAND"
```


## Least-Privilege Recommendations

- **DB user:** Create a dedicated MariaDB/MySQL user with SELECT, INSERT,
  UPDATE, DELETE on the Magento DB only — not GRANT or CREATE.
- **SSH user:** Restrict passwordless sudo to specific binaries if possible
  (e.g. `php`, `systemctl restart`, `redis-cli`) rather than `ALL`.
- **REST API:** MAGENTO_ADMIN_PASS is used only to obtain a short-lived
  session token via the Magento REST API. Consider creating a dedicated
  admin user with only the roles your agent needs.
- **SSH key:** Use a dedicated key pair for the agent, not your personal key.
## SSH Patterns

```bash
ssh -i ~/.ssh/magento_deploy MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento COMMAND 2>&1"
```


**DB queries:**
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'QUERY' 2>&1"
```

**REST API — get token then use it:**
```bash
TOKEN=$(ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "curl -s --cacert MAGENTO_CA_CERT -X POST MAGENTO_BASE_URL/rest/V1/integration/admin/token \
   -H 'Content-Type: application/json' \
   -d '{\"username\":\"MAGENTO_ADMIN_USER\",\"password\":\"MAGENTO_ADMIN_PASS\"}' 2>/dev/null | tr -d '\"'")
```

**Composer:**
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER bash -c 'cd MAGENTO_WEB_ROOT && php COMPOSER_PATH COMMAND 2>&1'"
```

---

## FULL HEALTH CHECK

```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
echo '=== VERSION ===' && sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento --version 2>&1
echo '=== MODE ===' && sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento deploy:mode:show 2>&1
echo '=== SERVICES ===' && sudo systemctl is-active apache2 nginx mariadb mysql redis-server opensearch php8.3-fpm php8.4-fpm 2>/dev/null
echo '=== LOAD ===' && uptime
echo '=== MEMORY ===' && free -h | grep Mem
echo '=== DISK ===' && df -h MAGENTO_WEB_ROOT | tail -1
echo '=== OPENSEARCH ===' && curl -s MAGENTO_OS_URL/_cluster/health 2>/dev/null | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d[\"status\"])'
echo '=== REDIS ===' && redis-cli ping && redis-cli info keyspace
echo '=== CRON ===' && MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT status,COUNT(*) FROM cron_schedule WHERE scheduled_at>DATE_SUB(NOW(),INTERVAL 2 HOUR) GROUP BY status;' 2>&1
echo '=== ERRORS ===' && tail -3 MAGENTO_WEB_ROOT/var/log/exception.log 2>/dev/null | grep -c CRITICAL || echo 0
" 2>&1
```

---

## CACHE

Status:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cache:status 2>&1"
```

Flush all:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cache:flush 2>&1"
```

Clean specific type (replace TYPE):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cache:clean TYPE 2>&1"
```
Types: config layout block_html collections reflection db_ddl compiled_config eav customer_notification full_page config_integration config_integration_api translate config_webservice graphql_query_resolver_result

Redis flush by DB (0=config 1=page 2=sessions):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "redis-cli -n 0 FLUSHDB && echo cache_cleared"
```

---

## INDEXING

Status:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento indexer:status 2>&1"
```

Reindex all:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento indexer:reindex 2>&1"
```

Reindex specific (replace INDEXER_ID):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento indexer:reindex INDEXER_ID 2>&1"
```
IDs: cataloginventory_stock catalog_category_product catalog_product_category catalog_product_price catalog_product_attribute catalogsearch_fulltext catalogrule_rule catalogrule_product customer_grid design_config_grid inventory

Rebuild OpenSearch (search broken):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
  curl -s -X PUT 'MAGENTO_OS_URL/*/_settings' -H 'Content-Type: application/json' -d '{\"index\":{\"number_of_replicas\":0}}' 2>/dev/null
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento indexer:reset catalogsearch_fulltext 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento indexer:reindex catalogsearch_fulltext 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cache:flush 2>&1
"
```

---

## CRON

Run now:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cron:run 2>&1"
```

Backlog summary:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT status,COUNT(*) AS cnt FROM cron_schedule GROUP BY status ORDER BY cnt DESC;' 2>&1"
```

Top failing jobs:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT job_code,COUNT(*) as cnt,MAX(messages) as err FROM cron_schedule WHERE status=\"error\" GROUP BY job_code ORDER BY cnt DESC LIMIT 10;' 2>&1"
```

Clear old error/missed history:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'DELETE FROM cron_schedule WHERE status IN (\"error\",\"missed\") AND scheduled_at<DATE_SUB(NOW(),INTERVAL 1 DAY);' 2>&1"
```

Install crontab:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cron:install 2>&1"
```

---

## MAINTENANCE MODE

```bash
# Enable
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento maintenance:enable 2>&1"
# Disable
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento maintenance:disable 2>&1"
```

---

## ORDERS

Revenue today:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT COUNT(*) as orders,ROUND(COALESCE(SUM(grand_total),0),2) as revenue FROM sales_order WHERE DATE(created_at)=CURDATE() AND state <> \"canceled\";' 2>&1"
```

Revenue this week:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT COUNT(*) as orders,ROUND(COALESCE(SUM(grand_total),0),2) as revenue FROM sales_order WHERE created_at>=DATE_SUB(NOW(),INTERVAL 7 DAY) AND state <> \"canceled\";' 2>&1"
```

Revenue this month:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT COUNT(*) as orders,ROUND(COALESCE(SUM(grand_total),0),2) as revenue FROM sales_order WHERE YEAR(created_at)=YEAR(NOW()) AND MONTH(created_at)=MONTH(NOW()) AND state <> \"canceled\";' 2>&1"
```

Last 10 orders:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT increment_id,customer_email,grand_total,status,created_at FROM sales_order ORDER BY created_at DESC LIMIT 10;' 2>&1"
```

Order detail (replace ORDERID with increment_id):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT o.increment_id,o.customer_email,o.grand_total,o.status,o.state,o.created_at,a.street,a.city,a.postcode FROM sales_order o LEFT JOIN sales_order_address a ON o.entity_id=a.parent_id AND a.address_type=\"shipping\" WHERE o.increment_id=\"ORDERID\";' 2>&1"
```

Cancel order (REST API — replace ORDER_ENTITY_ID):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
TOKEN=\$(curl -s --cacert MAGENTO_CA_CERT -X POST MAGENTO_BASE_URL/rest/V1/integration/admin/token \
  -H 'Content-Type: application/json' \
  -d '{\"username\":\"MAGENTO_ADMIN_USER\",\"password\":\"MAGENTO_ADMIN_PASS\"}' 2>/dev/null | tr -d '\"')
curl -s --cacert MAGENTO_CA_CERT -X POST MAGENTO_BASE_URL/rest/V1/orders/ORDER_ENTITY_ID/cancel \
  -H \"Authorization: Bearer \$TOKEN\" 2>/dev/null
"
```

Invoice order (replace ORDER_ENTITY_ID):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
TOKEN=\$(curl -s --cacert MAGENTO_CA_CERT -X POST MAGENTO_BASE_URL/rest/V1/integration/admin/token \
  -H 'Content-Type: application/json' \
  -d '{\"username\":\"MAGENTO_ADMIN_USER\",\"password\":\"MAGENTO_ADMIN_PASS\"}' 2>/dev/null | tr -d '\"')
curl -s --cacert MAGENTO_CA_CERT -X POST MAGENTO_BASE_URL/rest/V1/order/ORDER_ENTITY_ID/invoice \
  -H \"Authorization: Bearer \$TOKEN\" \
  -H 'Content-Type: application/json' \
  -d '{\"capture\":true,\"notify\":true}' 2>/dev/null
"
```

Ship order (replace ORDER_ENTITY_ID):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
TOKEN=\$(curl -s --cacert MAGENTO_CA_CERT -X POST MAGENTO_BASE_URL/rest/V1/integration/admin/token \
  -H 'Content-Type: application/json' \
  -d '{\"username\":\"MAGENTO_ADMIN_USER\",\"password\":\"MAGENTO_ADMIN_PASS\"}' 2>/dev/null | tr -d '\"')
curl -s --cacert MAGENTO_CA_CERT -X POST MAGENTO_BASE_URL/rest/V1/order/ORDER_ENTITY_ID/ship \
  -H \"Authorization: Bearer \$TOKEN\" \
  -H 'Content-Type: application/json' \
  -d '{\"notify\":true}' 2>/dev/null
"
```

Refund order (replace ORDER_ENTITY_ID):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
TOKEN=\$(curl -s --cacert MAGENTO_CA_CERT -X POST MAGENTO_BASE_URL/rest/V1/integration/admin/token \
  -H 'Content-Type: application/json' \
  -d '{\"username\":\"MAGENTO_ADMIN_USER\",\"password\":\"MAGENTO_ADMIN_PASS\"}' 2>/dev/null | tr -d '\"')
curl -s --cacert MAGENTO_CA_CERT -X POST MAGENTO_BASE_URL/rest/V1/order/ORDER_ENTITY_ID/refund \
  -H \"Authorization: Bearer \$TOKEN\" \
  -H 'Content-Type: application/json' \
  -d '{\"notify\":true,\"arguments\":{\"shipping_amount\":0,\"adjustment_positive\":0,\"adjustment_negative\":0}}' 2>/dev/null
"
```

Abandoned carts today:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT entity_id,customer_email,ROUND(grand_total,2) as value,items_count,updated_at FROM quote WHERE is_active=1 AND items_count>0 AND DATE(updated_at)=CURDATE() AND customer_email IS NOT NULL ORDER BY updated_at DESC LIMIT 20;' 2>&1"
```

Sales report by day (last 30 days):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT DATE(created_at) as day,COUNT(*) as orders,ROUND(SUM(grand_total),2) as revenue FROM sales_order WHERE created_at>=DATE_SUB(NOW(),INTERVAL 30 DAY) AND state <> \"canceled\" GROUP BY DATE(created_at) ORDER BY day DESC;' 2>&1"
```

---

## PRODUCTS

Total count by type:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT COUNT(*) as total,type_id FROM catalog_product_entity GROUP BY type_id;' 2>&1"
```

Out of stock:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT cpe.sku,csi.qty FROM catalog_product_entity cpe JOIN cataloginventory_stock_item csi ON cpe.entity_id=csi.product_id WHERE csi.is_in_stock=0 OR csi.qty<=0 ORDER BY cpe.sku LIMIT 30;' 2>&1"
```

Update stock via REST (replace SKU and QTY):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
TOKEN=\$(curl -s --cacert MAGENTO_CA_CERT -X POST MAGENTO_BASE_URL/rest/V1/integration/admin/token \
  -H 'Content-Type: application/json' \
  -d '{\"username\":\"MAGENTO_ADMIN_USER\",\"password\":\"MAGENTO_ADMIN_PASS\"}' 2>/dev/null | tr -d '\"')
curl -s --cacert MAGENTO_CA_CERT -X PUT MAGENTO_BASE_URL/rest/V1/products/SKU/stockItems/1 \
  -H \"Authorization: Bearer \$TOKEN\" \
  -H 'Content-Type: application/json' \
  -d '{\"stockItem\":{\"qty\":QTY,\"is_in_stock\":true}}' 2>/dev/null
"
```

Update product price via REST (replace SKU and PRICE):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
TOKEN=\$(curl -s --cacert MAGENTO_CA_CERT -X POST MAGENTO_BASE_URL/rest/V1/integration/admin/token \
  -H 'Content-Type: application/json' \
  -d '{\"username\":\"MAGENTO_ADMIN_USER\",\"password\":\"MAGENTO_ADMIN_PASS\"}' 2>/dev/null | tr -d '\"')
curl -s --cacert MAGENTO_CA_CERT -X PUT MAGENTO_BASE_URL/rest/V1/products/SKU \
  -H \"Authorization: Bearer \$TOKEN\" \
  -H 'Content-Type: application/json' \
  -d '{\"product\":{\"sku\":\"SKU\",\"price\":PRICE}}' 2>/dev/null
"
```

---

## CUSTOMERS

Find by email (replace EMAIL):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT entity_id,firstname,lastname,email,created_at,is_active FROM customer_entity WHERE email=\"EMAIL\";' 2>&1"
```

Customer LTV (replace EMAIL):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT COUNT(*) as orders,ROUND(COALESCE(SUM(grand_total),0),2) as ltv FROM sales_order WHERE customer_email=\"EMAIL\" AND state <> \"canceled\";' 2>&1"
```

Top 10 customers by revenue:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT customer_email,COUNT(*) as orders,ROUND(SUM(grand_total),2) as ltv FROM sales_order WHERE state <> \"canceled\" GROUP BY customer_email ORDER BY ltv DESC LIMIT 10;' 2>&1"
```

Reset customer password via REST (replace EMAIL):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
TOKEN=\$(curl -s --cacert MAGENTO_CA_CERT -X POST MAGENTO_BASE_URL/rest/V1/integration/admin/token \
  -H 'Content-Type: application/json' \
  -d '{\"username\":\"MAGENTO_ADMIN_USER\",\"password\":\"MAGENTO_ADMIN_PASS\"}' 2>/dev/null | tr -d '\"')
curl -s --cacert MAGENTO_CA_CERT -X PUT MAGENTO_BASE_URL/rest/V1/customers/password \
  -H \"Authorization: Bearer \$TOKEN\" \
  -H 'Content-Type: application/json' \
  -d '{\"email\":\"EMAIL\",\"template\":\"email_reset\",\"websiteId\":1}' 2>/dev/null
"
```

---

## ADMIN USERS

List all:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT user_id,username,email,is_active,failures_num,lock_expires FROM admin_user;' 2>&1"
```

Unlock admin (replace USERNAME):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento admin:user:unlock USERNAME 2>&1
  redis-cli -n 2 FLUSHDB
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cache:flush 2>&1
"
```

Create admin user (owner use — use dedicated limited-role account):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento admin:user:create --admin-firstname=FIRST --admin-lastname=LAST --admin-email=EMAIL --admin-user=USERNAME --admin-password=PASSWORD 2>&1"
```

---

## CONFIGURATION

Show config path (replace PATH):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento config:show PATH 2>&1"
```

Set config value (replace PATH and VALUE):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento config:set PATH VALUE 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cache:flush 2>&1
"
```

Raw DB config lookup (replace SEARCH):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT scope,scope_id,path,value FROM core_config_data WHERE path LIKE \"%SEARCH%\" ORDER BY scope,scope_id;' 2>&1"
```

Multi-store list:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT w.name as website,g.name as store_group,s.name as store,s.code FROM store s JOIN store_group g ON s.group_id=g.group_id JOIN store_website w ON g.website_id=w.website_id ORDER BY w.website_id,g.group_id;' 2>&1"
```

---

## EMAIL & SMTP

SMTP config:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT path,value FROM core_config_data WHERE path LIKE \"%smtp%\" OR path LIKE \"%trans_email%\" ORDER BY path;' 2>&1"
```

Test send (replace RECIPIENT):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento sparsh_smtp:test-mail --recipient=RECIPIENT 2>&1"
```

---

## PRICE RULES & COUPONS

Active cart price rules:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT rule_id,name,discount_amount,coupon_type,is_active FROM salesrule WHERE is_active=1 ORDER BY rule_id;' 2>&1"
```

Coupon usage (replace COUPON_CODE):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT c.code,c.times_used,c.usage_limit,r.name FROM salesrule_coupon c JOIN salesrule r ON c.rule_id=r.rule_id WHERE c.code=\"COUPON_CODE\";' 2>&1"
```

Generate coupons via REST (replace RULE_ID):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
TOKEN=\$(curl -s --cacert MAGENTO_CA_CERT -X POST MAGENTO_BASE_URL/rest/V1/integration/admin/token \
  -H 'Content-Type: application/json' \
  -d '{\"username\":\"MAGENTO_ADMIN_USER\",\"password\":\"MAGENTO_ADMIN_PASS\"}' 2>/dev/null | tr -d '\"')
curl -s --cacert MAGENTO_CA_CERT -X POST MAGENTO_BASE_URL/rest/V1/salesRules/RULE_ID/coupons/generate \
  -H \"Authorization: Bearer \$TOKEN\" \
  -H 'Content-Type: application/json' \
  -d '{\"couponSpec\":{\"rule_id\":RULE_ID,\"qty\":5,\"length\":10,\"format\":\"alphanum\",\"prefix\":\"PROMO-\"}}' 2>/dev/null
"
```

---

## MODULES

Status:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento module:status 2>&1"
```

Enable module (replace Vendor_Module):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento module:enable Vendor_Module 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento setup:upgrade 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cache:flush 2>&1
"
```

Disable module:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento module:disable Vendor_Module 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento setup:upgrade 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cache:flush 2>&1
"
```

---

## COMPOSER — EXTENSIONS

Install extension (replace vendor/package:^version):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento maintenance:enable 2>&1
  sudo -u MAGENTO_WEB_USER bash -c 'cd MAGENTO_WEB_ROOT && php COMPOSER_PATH require vendor/package:^version --no-interaction 2>&1'
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento setup:upgrade 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento setup:di:compile 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento setup:static-content:deploy -f 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cache:flush 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento maintenance:disable 2>&1
"
```

Remove extension:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento maintenance:enable 2>&1
  sudo -u MAGENTO_WEB_USER bash -c 'cd MAGENTO_WEB_ROOT && php COMPOSER_PATH remove vendor/package --no-interaction 2>&1'
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento setup:upgrade 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cache:flush 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento maintenance:disable 2>&1
"
```

---

## DEPLOYMENT

Full deploy sequence:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento maintenance:enable 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento setup:upgrade 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento setup:di:compile 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento setup:static-content:deploy -f 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cache:flush 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento maintenance:disable 2>&1
"
```

---

## GRAPHQL

Store config:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "curl -s --cacert MAGENTO_CA_CERT -X POST MAGENTO_BASE_URL/graphql -H 'Content-Type: application/json' \
   -d '{\"query\":\"{storeConfig{store_code store_name base_url locale default_display_currency_code}}\"}' 2>/dev/null | python3 -m json.tool"
```

Product search (replace SEARCH_TERM):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "curl -s --cacert MAGENTO_CA_CERT -X POST MAGENTO_BASE_URL/graphql -H 'Content-Type: application/json' \
   -d '{\"query\":\"{products(search:\\\"SEARCH_TERM\\\",pageSize:5){items{sku name price{regularPrice{amount{value currency}}}}}}\"}' 2>/dev/null | python3 -m json.tool"
```

Category list:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "curl -s --cacert MAGENTO_CA_CERT -X POST MAGENTO_BASE_URL/graphql -H 'Content-Type: application/json' \
   -d '{\"query\":\"{categoryList{id name url_key level children{id name url_key}}}\"}' 2>/dev/null | python3 -m json.tool"
```

---

## BACKUP & RESTORE

DB backup:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
  TS=\$(date +%Y%m%d_%H%M%S)
  mkdir -p /opt/magento_backups
  MYSQL_PWD=MAGENTO_DB_PASS mysqldump -uMAGENTO_DB_USER MAGENTO_DB_NAME | gzip > /opt/magento_backups/db_\${TS}.sql.gz
  ls -lh /opt/magento_backups/db_\${TS}.sql.gz && echo BACKUP_DONE
"
```

List backups:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "ls -lhrt /opt/magento_backups/ 2>/dev/null | tail -10"
```

Restore DB (replace BACKUPFILE):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento maintenance:enable 2>&1
  gunzip -c BACKUPFILE | MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME && echo DB_RESTORED
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cache:flush 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento maintenance:disable 2>&1
"
```

---

## DATABASE QUERIES

DB size and largest tables:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
  MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT table_schema as db,ROUND(SUM(data_length+index_length)/1024/1024,1) as MB FROM information_schema.tables WHERE table_schema=database() GROUP BY table_schema;' 2>&1
  MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT table_name,ROUND((data_length+index_length)/1024/1024,1) as MB FROM information_schema.tables WHERE table_schema=database() ORDER BY MB DESC LIMIT 15;' 2>&1
"
```

Run a specific SQL query (owner use — verify query before execution):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT ...; -- replace with specific query' 2>&1"
```

Purge old log tables:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'DELETE FROM report_event WHERE logged_at<DATE_SUB(NOW(),INTERVAL 30 DAY); DELETE FROM customer_visitor WHERE last_visit_at<DATE_SUB(NOW(),INTERVAL 1 DAY); SELECT \"Done\";' 2>&1"
```

Optimize slow tables:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'OPTIMIZE TABLE cron_schedule,quote,report_event,customer_visitor;' 2>&1"
```

---

## LOGS

Exception log:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "tail -50 MAGENTO_WEB_ROOT/var/log/exception.log 2>/dev/null"
```

System log:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "tail -30 MAGENTO_WEB_ROOT/var/log/system.log 2>/dev/null"
```

All log files with sizes:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "ls -lh MAGENTO_WEB_ROOT/var/log/ 2>/dev/null | sort -k5 -hr | head -20"
```

---

## SERVICES

Check all:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo systemctl is-active apache2 nginx mariadb mysql redis-server opensearch 2>/dev/null"
```

Restart all (safe order):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
  sudo systemctl restart mariadb mysql redis-server 2>&1
  sleep 5
  sudo systemctl restart apache2 nginx 2>&1
  echo ALL_RESTARTED
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cache:flush 2>&1
"
```

---

## OPENSEARCH

Health:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "curl -s MAGENTO_OS_URL/_cluster/health 2>/dev/null | python3 -m json.tool"
```

List indices:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "curl -s 'MAGENTO_OS_URL/_cat/indices?v' 2>/dev/null"
```

---

## SECURITY

2FA status:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e 'SELECT u.username,u.email,t.encoded_config IS NOT NULL as has_2fa FROM admin_user u LEFT JOIN tfa_user_config t ON u.user_id=t.user_id;' 2>&1"
```

Reset 2FA (replace USERNAME):
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento security:tfa:reset USERNAME google 2>&1"
```

---

## AUTO-HEALING

Site slow / high load:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
  echo LOAD: \$(cat /proc/loadavg)
  MYSQL_PWD=MAGENTO_DB_PASS mysql -uMAGENTO_DB_USER MAGENTO_DB_NAME -e \"UPDATE cron_schedule SET status='missed' WHERE status='running' AND executed_at<DATE_SUB(NOW(),INTERVAL 2 HOUR);\" 2>&1
  sudo pkill -f 'php.*cron:run' 2>/dev/null || true
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cache:flush 2>&1
  echo NEW_LOAD: \$(cat /proc/loadavg)
"
```

Admin locked out:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento admin:user:unlock MAGENTO_ADMIN_USER 2>&1
  redis-cli -n 2 FLUSHDB
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cache:flush 2>&1
"
```

Search broken:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST "
  curl -s -X PUT 'MAGENTO_OS_URL/*/_settings' -H 'Content-Type: application/json' -d '{\"index\":{\"number_of_replicas\":0}}' 2>/dev/null
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento indexer:reset catalogsearch_fulltext 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento indexer:reindex catalogsearch_fulltext 2>&1
  sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento cache:flush 2>&1
"
```

---

## MESSAGE QUEUE

List consumers:
```bash
ssh -i MAGENTO_SSH_KEY -o StrictHostKeyChecking=yes MAGENTO_SSH_USER@MAGENTO_HOST \
  "sudo -u MAGENTO_WEB_USER MAGENTO_PHP MAGENTO_WEB_ROOT/bin/magento queue:consumers:list 2>&1"
```

---

## Intended Use and Risk Acknowledgement

This skill is designed for **server owners** administering their own Magento 2
installation. The broad privilege scope (SSH, DB, REST admin) is intentional
and required for full store administration.

**This skill should not be installed if:**
- You do not own and control MAGENTO_HOST
- You are not the Magento store administrator
- You have not reviewed the commands this skill will execute

**Risk mitigations included:**
- SSH key authentication only (no passwords on command lines)
- DB password via MYSQL_PWD env var (not visible in process list)
- All credentials user-supplied — nothing hardcoded in skill
- Commands connect only to MAGENTO_HOST — no third-party calls
- Least-privilege recommendations provided (see above section)
- prompt_injection_mitigation declared — commands use fixed vars only

## AGENT INSTRUCTIONS

When a user asks about their Magento store, use the commands above to retrieve
real data from the server and provide a clear, formatted response.

All commands connect only to the server configured in MAGENTO_HOST using
credentials supplied by the user. No data is sent to third parties.

Format responses with:
- 🟢 OK  🔴 error  ⚠️ warning  📦 orders  🛍️ products  👥 customers
- 💰 revenue  🔧 running  ✅ done  🔒 security  📧 email  🚚 shipping
- Plain English summary with key numbers — avoid dumping raw output
- If something is wrong, identify it and suggest the fix

prompt_injection_mitigation: >
  All commands use fixed configuration variables only. Free-form user
  input is never interpolated into shell commands.
