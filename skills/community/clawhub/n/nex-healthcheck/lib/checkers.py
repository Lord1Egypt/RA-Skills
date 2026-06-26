"""
Nex HealthCheck - Health check implementations
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import socket
import ssl
import subprocess
import time
import urllib.request
import urllib.error
from pathlib import Path
from config import CheckType, StatusLevel, DEFAULT_TIMEOUTS, SSL_CERT_WARNING_DAYS, SSL_CERT_CRITICAL_DAYS


def check_http(url, expected_status=200, timeout=10):
    """HTTP GET check. Returns response time and status code."""
    try:
        start = time.time()
        req = urllib.request.Request(url, headers={"User-Agent": "nex-healthcheck/1.0"})
        try:
            response = urllib.request.urlopen(req, timeout=timeout)
            status_code = response.getcode()
            response_time_ms = int((time.time() - start) * 1000)

            if status_code == expected_status:
                return {
                    "status": StatusLevel.OK.value,
                    "response_time_ms": response_time_ms,
                    "status_code": status_code,
                    "message": f"HTTP {status_code} OK"
                }
            else:
                return {
                    "status": StatusLevel.CRITICAL.value,
                    "response_time_ms": response_time_ms,
                    "status_code": status_code,
                    "message": f"HTTP {status_code}, expected {expected_status}"
                }
        except urllib.error.HTTPError as e:
            response_time_ms = int((time.time() - start) * 1000)
            return {
                "status": StatusLevel.CRITICAL.value,
                "response_time_ms": response_time_ms,
                "status_code": e.code,
                "message": f"HTTP {e.code}"
            }
    except Exception as e:
        response_time_ms = int((time.time() - start) * 1000)
        return {
            "status": StatusLevel.CRITICAL.value,
            "response_time_ms": response_time_ms,
            "message": f"Connection failed: {str(e)}"
        }


def check_tcp(host, port, timeout=5):
    """TCP socket connection test."""
    try:
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, int(port)))
        sock.close()
        response_time_ms = int((time.time() - start) * 1000)

        if result == 0:
            return {
                "status": StatusLevel.OK.value,
                "response_time_ms": response_time_ms,
                "message": f"Port {port} open"
            }
        else:
            return {
                "status": StatusLevel.CRITICAL.value,
                "response_time_ms": response_time_ms,
                "message": f"Port {port} closed or unreachable"
            }
    except Exception as e:
        return {
            "status": StatusLevel.CRITICAL.value,
            "message": f"Connection error: {str(e)}"
        }


def check_dns(domain, expected_ip=None, nameserver=None):
    """DNS resolution check using dig or nslookup."""
    try:
        start = time.time()
        # Try dig first
        cmd = ["dig", "+short"]
        if nameserver:
            cmd.extend(["@" + nameserver])
        cmd.append(domain)

        try:
            output = subprocess.check_output(cmd, timeout=5, text=True).strip()
        except FileNotFoundError:
            # Fall back to nslookup
            cmd = ["nslookup", domain]
            if nameserver:
                cmd.append(nameserver)
            output = subprocess.check_output(cmd, timeout=5, text=True).strip()

        response_time_ms = int((time.time() - start) * 1000)

        if output:
            if expected_ip and expected_ip not in output:
                return {
                    "status": StatusLevel.CRITICAL.value,
                    "response_time_ms": response_time_ms,
                    "message": f"Resolved but expected IP {expected_ip} not found",
                    "details": {"resolved": output}
                }
            return {
                "status": StatusLevel.OK.value,
                "response_time_ms": response_time_ms,
                "message": "Resolves correctly",
                "details": {"resolved": output}
            }
        else:
            return {
                "status": StatusLevel.CRITICAL.value,
                "response_time_ms": response_time_ms,
                "message": "No DNS records found"
            }
    except subprocess.TimeoutExpired:
        return {
            "status": StatusLevel.CRITICAL.value,
            "message": "DNS lookup timeout"
        }
    except FileNotFoundError:
        return {
            "status": StatusLevel.UNKNOWN.value,
            "message": "dig and nslookup not found. Install bind-utils or dnsutils."
        }
    except Exception as e:
        return {
            "status": StatusLevel.CRITICAL.value,
            "message": f"DNS error: {str(e)}"
        }


def check_ssl_cert(host, port=443):
    """Check SSL certificate expiry."""
    try:
        start = time.time()
        context = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()

        response_time_ms = int((time.time() - start) * 1000)

        if not cert:
            return {
                "status": StatusLevel.UNKNOWN.value,
                "message": "Could not retrieve certificate"
            }

        # Parse expiry date
        import ssl as ssl_module
        cert_bin = ssock.getpeercert(binary_form=True)
        if cert_bin:
            der_cert = cert_bin
        else:
            return {
                "status": StatusLevel.UNKNOWN.value,
                "message": "Could not get certificate binary"
            }

        # Extract expiry from cert dict
        not_after = cert.get("notAfter")
        if not_after:
            import datetime
            expiry_dt = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
            now = datetime.datetime.utcnow()
            days_left = (expiry_dt - now).days

            subject = dict(x[0] for x in cert.get("subject", []))
            issuer = dict(x[0] for x in cert.get("issuer", []))

            if days_left < SSL_CERT_CRITICAL_DAYS:
                status = StatusLevel.CRITICAL.value
            elif days_left < SSL_CERT_WARNING_DAYS:
                status = StatusLevel.WARNING.value
            else:
                status = StatusLevel.OK.value

            return {
                "status": status,
                "response_time_ms": response_time_ms,
                "message": f"Expires in {days_left} days",
                "details": {
                    "days_until_expiry": days_left,
                    "expiry_date": not_after,
                    "subject": subject.get("commonName", ""),
                    "issuer": issuer.get("commonName", "")
                }
            }
        else:
            return {
                "status": StatusLevel.UNKNOWN.value,
                "message": "Could not parse certificate expiry"
            }
    except socket.timeout:
        return {
            "status": StatusLevel.CRITICAL.value,
            "message": f"Connection timeout to {host}:{port}"
        }
    except Exception as e:
        return {
            "status": StatusLevel.CRITICAL.value,
            "message": f"SSL error: {str(e)}"
        }


def check_docker_container(container_name, host=None, ssh_user=None):
    """Check Docker container status. Locally or via SSH."""
    cmd = f"docker inspect --format='{{{{.State.Status}}}}' {container_name}"
    try:
        if host and ssh_user:
            output, code = _run_ssh_command(host, ssh_user, cmd)
        else:
            output = subprocess.check_output(cmd, shell=True, timeout=10, text=True).strip()
            code = 0

        if code == 0 and output in ["running", "paused"]:
            status = "running" if output == "running" else "paused"
            return {
                "status": StatusLevel.OK.value if output == "running" else StatusLevel.WARNING.value,
                "message": f"Status: {status}",
                "details": {"state": output}
            }
        else:
            return {
                "status": StatusLevel.CRITICAL.value,
                "message": f"Container not running or not found",
                "details": {"state": output if output else "unknown"}
            }
    except Exception as e:
        return {
            "status": StatusLevel.CRITICAL.value,
            "message": f"Docker check failed: {str(e)}"
        }


def check_systemd_service(service_name, host=None, ssh_user=None):
    """Check systemd service status. Locally or via SSH."""
    cmd = f"systemctl is-active {service_name}"
    try:
        if host and ssh_user:
            output, code = _run_ssh_command(host, ssh_user, cmd)
            is_active = code == 0
        else:
            output = subprocess.check_output(cmd, shell=True, timeout=5, text=True).strip()
            is_active = True

        if is_active:
            return {
                "status": StatusLevel.OK.value,
                "message": f"Active (running)"
            }
        else:
            return {
                "status": StatusLevel.CRITICAL.value,
                "message": f"Service not active",
                "details": {"state": output}
            }
    except Exception as e:
        return {
            "status": StatusLevel.CRITICAL.value,
            "message": f"Systemd check failed: {str(e)}"
        }


def check_ssh_command(host, user, command, expected_output=None):
    """Run arbitrary command via SSH."""
    try:
        start = time.time()
        output, code = _run_ssh_command(host, user, command)
        response_time_ms = int((time.time() - start) * 1000)

        if code != 0:
            return {
                "status": StatusLevel.CRITICAL.value,
                "response_time_ms": response_time_ms,
                "message": f"Command failed with exit code {code}",
                "details": {"output": output}
            }

        if expected_output and expected_output not in output:
            return {
                "status": StatusLevel.CRITICAL.value,
                "response_time_ms": response_time_ms,
                "message": f"Output mismatch. Expected: {expected_output}",
                "details": {"output": output}
            }

        return {
            "status": StatusLevel.OK.value,
            "response_time_ms": response_time_ms,
            "message": "Command executed successfully"
        }
    except Exception as e:
        return {
            "status": StatusLevel.CRITICAL.value,
            "message": f"SSH command failed: {str(e)}"
        }


def check_ping(host, count=3):
    """ICMP ping check."""
    try:
        start = time.time()
        cmd = ["ping", "-c", str(count), "-W", "5", host]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=20, text=True)
        response_time_ms = int((time.time() - start) * 1000)

        # Parse packet loss
        lines = output.split("\n")
        for line in lines:
            if "packet loss" in line:
                # Extract percentage
                parts = line.split()
                for i, part in enumerate(parts):
                    if "%" in part:
                        try:
                            loss_pct = float(part.rstrip("%"))
                            if loss_pct == 0:
                                return {
                                    "status": StatusLevel.OK.value,
                                    "response_time_ms": response_time_ms,
                                    "message": f"Host reachable, 0% packet loss"
                                }
                            else:
                                return {
                                    "status": StatusLevel.WARNING.value,
                                    "response_time_ms": response_time_ms,
                                    "message": f"Host reachable, {loss_pct}% packet loss"
                                }
                        except ValueError:
                            pass

        return {
            "status": StatusLevel.OK.value,
            "response_time_ms": response_time_ms,
            "message": "Host reachable"
        }
    except subprocess.CalledProcessError:
        response_time_ms = int((time.time() - start) * 1000)
        return {
            "status": StatusLevel.CRITICAL.value,
            "response_time_ms": response_time_ms,
            "message": "Host unreachable"
        }
    except Exception as e:
        return {
            "status": StatusLevel.CRITICAL.value,
            "message": f"Ping failed: {str(e)}"
        }


def check_disk(path="/", host=None, ssh_user=None):
    """Check disk usage via df command."""
    cmd = f"df {path} | tail -1"
    try:
        if host and ssh_user:
            output, code = _run_ssh_command(host, ssh_user, cmd)
        else:
            output = subprocess.check_output(cmd, shell=True, timeout=10, text=True).strip()
            code = 0

        if code != 0 or not output:
            return {
                "status": StatusLevel.CRITICAL.value,
                "message": f"Could not read disk usage for {path}"
            }

        # Parse df output: filesystem blocks used available use% mounted
        parts = output.split()
        if len(parts) >= 5:
            try:
                used_pct = int(parts[4].rstrip("%"))
                available_kb = int(parts[3])
                available_gb = available_kb / 1024 / 1024

                if used_pct >= 90:
                    status = StatusLevel.CRITICAL.value
                elif used_pct >= 80:
                    status = StatusLevel.WARNING.value
                else:
                    status = StatusLevel.OK.value

                return {
                    "status": status,
                    "message": f"{used_pct}% used ({available_gb:.1f} GB free)",
                    "details": {
                        "used_percent": used_pct,
                        "free_gb": available_gb
                    }
                }
            except ValueError:
                pass

        return {
            "status": StatusLevel.UNKNOWN.value,
            "message": "Could not parse disk usage output"
        }
    except Exception as e:
        return {
            "status": StatusLevel.CRITICAL.value,
            "message": f"Disk check failed: {str(e)}"
        }


def run_check(service):
    """Dispatcher: call the right checker based on check_type."""
    check_type = service.get("check_type", "").lower()
    target = service.get("target", "")
    port = service.get("port")
    expected_status = service.get("expected_status")

    try:
        if check_type == CheckType.HTTP.value:
            return check_http(target, expected_status=expected_status or 200)

        elif check_type == CheckType.TCP.value:
            if not port:
                return {"status": StatusLevel.CRITICAL.value, "message": "Port required for TCP check"}
            return check_tcp(target, port)

        elif check_type == CheckType.DNS.value:
            return check_dns(target, expected_ip=expected_status)

        elif check_type == CheckType.SSL_CERT.value:
            port = port or 443
            return check_ssl_cert(target, port)

        elif check_type == CheckType.DOCKER.value:
            ssh_info = _parse_ssh_host(service.get("ssh_host"))
            return check_docker_container(target, host=ssh_info[0], ssh_user=ssh_info[1])

        elif check_type == CheckType.SYSTEMD.value:
            ssh_info = _parse_ssh_host(service.get("ssh_host"))
            return check_systemd_service(target, host=ssh_info[0], ssh_user=ssh_info[1])

        elif check_type == CheckType.SSH_CMD.value:
            ssh_info = _parse_ssh_host(service.get("ssh_host"))
            if not ssh_info[0]:
                return {"status": StatusLevel.CRITICAL.value, "message": "SSH host required"}
            return check_ssh_command(ssh_info[0], ssh_info[1], target, expected_output=expected_status)

        elif check_type == CheckType.PING.value:
            return check_ping(target)

        elif check_type == CheckType.DISK.value:
            ssh_info = _parse_ssh_host(service.get("ssh_host"))
            return check_disk(target, host=ssh_info[0], ssh_user=ssh_info[1])

        else:
            return {"status": StatusLevel.UNKNOWN.value, "message": f"Unknown check type: {check_type}"}

    except Exception as e:
        return {"status": StatusLevel.CRITICAL.value, "message": f"Check error: {str(e)}"}


def run_all_checks(services=None):
    """Run all enabled checks. Return list of results."""
    if services is None:
        from storage import list_services
        services = list_services(enabled_only=True)

    results = []
    for service in services:
        result = run_check(service)
        result["service_id"] = service.get("id")
        result["service_name"] = service.get("name")
        results.append(result)

    return results


def _run_ssh_command(host, user, command, timeout=10):
    """Helper: Run command via SSH. Returns (output, exit_code)."""
    ssh_cmd = f"ssh {user}@{host} '{command}'"
    try:
        output = subprocess.check_output(ssh_cmd, shell=True, timeout=timeout, text=True, stderr=subprocess.STDOUT)
        return output.strip(), 0
    except subprocess.CalledProcessError as e:
        return e.output or "", e.returncode
    except subprocess.TimeoutExpired:
        return "SSH timeout", 1


def _parse_ssh_host(ssh_host_str):
    """Parse 'user@host' format. Returns (host, user) or (None, None)."""
    if not ssh_host_str:
        return None, None
    if "@" in ssh_host_str:
        parts = ssh_host_str.split("@")
        return parts[1], parts[0]
    return ssh_host_str, "root"
