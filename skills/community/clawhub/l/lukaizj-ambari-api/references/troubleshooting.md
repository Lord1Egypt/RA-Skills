# Troubleshooting

## Common Issues

### Connection Refused

**Symptom:** `Connection refused` or `Network is unreachable`

**Solutions:**
1. Verify Ambari server is running: `ambari-server status`
2. Check port 8080 is open: `telnet ambari-host 8080`
3. Verify URL format includes protocol: `https://` or `http://`

### Authentication Failed

**Symptom:** 401 Unauthorized

**Solutions:**
1. Verify username/password is correct
2. Check if LDAP/AD integration requires different credentials
3. Try default credentials: `admin/admin`
4. Check if account is locked after failed attempts

### SSL Certificate Errors

**Symptom:** `SSL: CERTIFICATE_VERIFY_FAILED`

**Solutions:**
1. The script disables SSL verification by default
2. For production, add proper certificates:
   ```bash
   export REQUESTS_CA_BUNDLE=/path/to/ca-bundle.crt
   ```

### Service Operation Timeout

**Symptom:** Operation takes too long or hangs

**Solutions:**
1. Check request status manually:
   ```bash
   python ambari_api.py --config prod --cluster mycluster
   # Check Ambari UI for request progress
   ```
2. Check Ambari agent logs on affected host: `/var/log/ambari-agent/ambari-agent.log`
3. Check service-specific logs (e.g., HDFS logs in `/var/log/hadoop/`)

### Component Not Found

**Symptom:** 404 error when accessing component

**Solutions:**
1. Verify component name is correct (case-sensitive)
2. Use exact component name from list:
   ```bash
   python ambari_api.py components --config prod --cluster mycluster --host node01
   ```
3. Common naming: `DATANODE`, `NAMENODE`, `NODEMANAGER`, `RESOURCEMANAGER`

### Service State Stuck

**Symptom:** Service shows `STARTING` or `STOPPING` but never completes

**Solutions:**
1. Check Ambari Server logs: `/var/log/ambari-server/ambari-server.log`
2. Check for stuck commands in Ambari UI
3. Abort stuck request and retry
4. Restart Ambari agent on affected host:
   ```bash
   ambari-agent restart
   ```

## Version-Specific Issues

### Ambari 2.7.5

**Issue:** Blueprint import may fail with large clusters

**Solution:** Split blueprint into smaller chunks or use API directly

### Ambari 3.0.0

**Issue:** Some API endpoints changed

**Solution:** Use updated endpoint patterns:
- Mpacks: `/api/v1/mpacks`
- Upgrades: `/api/v1/stacks/HDP/versions/3.1/repositories`

## Debug Mode

Enable verbose output for troubleshooting:

```bash
# Add to script or use Python directly
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Log Locations

| Component | Log Path |
|-----------|----------|
| Ambari Server | `/var/log/ambari-server/ambari-server.log` |
| Ambari Agent | `/var/log/ambari-agent/ambari-agent.log` |
| HDFS | `/var/log/hadoop/hdfs/` |
| YARN | `/var/log/hadoop-yarn/` |
| Hive | `/var/log/hive/` |
| ZooKeeper | `/var/log/zookeeper/` |

## Best Practices

1. **Always verify service status** after operations
2. **Use component-level operations** for rolling restarts
3. **Check dependencies** before stopping services (e.g., stop YARN before HDFS is not recommended)
4. **Monitor Ambari UI** for long-running operations
5. **Keep configuration files secure** - they contain passwords in plain text