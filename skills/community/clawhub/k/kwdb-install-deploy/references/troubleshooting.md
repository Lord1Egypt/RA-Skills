# KaiwuDB Common Issues and Solutions

## Installation Issues

### 1. Environment Check Failure

**Problem**: Script prompts environment check failure

**Solution**:
- Check if system requirements are met (memory, disk space)
- Ensure the user running the script has sufficient permissions
- Check if network connection is normal

### 2. Dependency Installation Failure

**Problem**: Error occurs during dependency installation

**Solution**:
- Check if system package manager is working normally (yum/apt)
- Try manually updating package manager:
  - CentOS: `sudo yum update -y`
  - Ubuntu: `sudo apt-get update -y`
- If network is slow, consider using domestic mirror sources

### 3. Installation Package Download Failure

**Problem**: Unable to download KaiwuDB installation package

**Solution**:
- Check network connection
- Try manually downloading the installation package and placing it in the scripts/ directory
- Contact technical support to obtain download link

## Runtime Issues

### 1. Database Cannot Start

**Problem**: No response after executing start command

**Solution**:
- Check data directory permissions: `ls -ld /var/lib/kwdb`
- Check log files: `cat /var/log/kwdb/kwdb.log`
- Check if configuration file is correct

### 2. Unable to Connect to Database

**Problem**: Cannot connect to database using psql command

**Solution**:
- Check if kwdb process is running: `ps aux | grep kwdb`
- Check if firewall allows port 5432 access
- Check if listen_addresses configuration is set to '*'
- Check if pg_hba.conf file allows connections

### 3. Database Running Slowly

**Problem**: Long query response time

**Solution**:
- Check system resource usage: `top`
- Check slow query log: `/var/log/kwdb/slow_query.log`
- Optimize query statements
- Adjust configuration file parameters

## Performance Issues

### 1. High Memory Usage

**Problem**: Database process occupies too much memory

**Solution**:
- Adjust shared_buffers parameter
- Check for memory leaks
- Increase system memory

### 2. High Disk I/O

**Problem**: Slow disk write speed

**Solution**:
- Check if disk space is sufficient
- Consider using SSD disk
- Adjust checkpoint-related parameters
- Optimize queries to reduce disk I/O

## Backup and Recovery

### 1. Backup Database

```bash
/opt/kwdb/current/bin/pg_dump -h localhost -p 5432 -U $USER -d kwdb_db > backup.sql
```

### 2. Restore Database

```bash
/opt/kwdb/current/bin/psql -h localhost -p 5432 -U $USER -d kwdb_db < backup.sql
```

## Contact Support

If you encounter issues that cannot be resolved, please contact technical support:
- Email: support@kaiwudb.com
- Phone: 400-xxx-xxxx
