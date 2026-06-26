# Archetype: Magento (or LAMP-style web stack)

For web stacks running Apache/Nginx + MariaDB/MySQL + PHP-FPM + Redis + (optionally) OpenSearch/Elasticsearch.

## When to use this archetype

- Magento 2 production server
- Generic LAMP/LEMP stack with multiple components
- E-commerce or CMS app where you want to verify "the storefront is up AND the search index is healthy AND background indexers are caught up"

## YAML

```yaml
- name: web-stack
  address: 192.0.2.70
  auth: ssh-pass
  user: admin
  password_env: HEARTH_PASS_WEB
  services: [ssh, apache2, mariadb, opensearch, php-fpm, redis-server, fail2ban]
  device_timeout: 25   # indexer:status can take 5-10 seconds
  apps:
    - name: storefront
      type: http
      url: https://shop.example.com/
      resolve: shop.example.com:443:192.0.2.70   # bypass DNS if needed
      expect_code: 200
      verify_tls: false   # self-signed or non-public-CA cert
    - name: opensearch-cluster
      type: command
      command: 'curl -s --max-time 3 http://127.0.0.1:9200/_cluster/health | jq -r .status'
      expect_match: '^(green|yellow)$'
    - name: magento-indexers
      type: command
      command: 'cd /var/www/html/magento && php bin/magento indexer:status | grep -c "Ready" || echo 0'
      expect_match: '^14$'   # adjust to your indexer count
```

## What the 5 layers will show

```
=== 192.0.2.70 web-stack ===
  L1 ping:    OK
  L2 uptime:  2 weeks, 6 hours, load: 0.25 0.26 0.16
  L3 mem:     used 2.8Gi / 15Gi, 12Gi avail | disk: / 2% used, 772G free
  L4 svc:     ssh=active apache2=active mariadb=active opensearch=active php-fpm=active redis-server=active fail2ban=active
  L5 app:     storefront=HTTP 200 | opensearch-cluster=OK (green) | magento-indexers=OK (14)
```

## Why three L5 probes for one stack?

Each catches a different failure class:

| L5 probe | Catches |
|----------|---------|
| `storefront=HTTP 200` | "Apache is running but the site returns 500" — most user-visible failure |
| `opensearch-cluster=green` | Search index unhealthy. Catalog browse will work, search won't |
| `magento-indexers=14` | Background catalog data is stale. Front-end shows wrong prices/stock |

`L4 svc:` confirms the *daemons* are running. `L5 app:` confirms they're actually *doing what you need*.

## Tweaks

- **WordPress instead of Magento**: replace the indexer probe with something WordPress-specific, e.g. a `/wp-json/wp/v2/posts` HTTP probe.
- **Drupal**: probe `/user/login` for a 200, `/admin/reports/status` for content.
- **Redis health**: add a command probe `redis-cli ping`, expect `PONG`.
- **MariaDB connection test**: `mysqladmin -u <readonly_user> -p<password> ping` — but you'd need to handle the password carefully (env var, not in YAML).
- **Ports bound only to localhost**: that's why the `opensearch-cluster` probe uses `curl http://127.0.0.1:9200` — it executes ON the device via SSH, so localhost from there reaches OpenSearch.

## Self-signed cert + custom hostname

The `--resolve` trick is essential when the bridgehead's DNS doesn't know about your storefront hostname:

```yaml
url: https://shop.example.com/
resolve: shop.example.com:443:192.0.2.70
verify_tls: false
```

This forces curl to connect to the IP but send the right SNI, so Apache's vhost matches and you get the real storefront, not the default site.