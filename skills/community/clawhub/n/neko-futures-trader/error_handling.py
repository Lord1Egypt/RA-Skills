#!/usr/bin/env python3
"""
Error Handling and Self-Debugging Module
Circuit breakers, retry logic, health checks, and auto-recovery
"""

import os
import sys
import time
import json
import traceback
from datetime import datetime, timedelta
from typing import Dict, Optional, Callable, Any
from collections import deque
import threading

# Load env
script_dir = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(script_dir, '.env')

if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and '=' in line:
                k, v = line.split('=', 1)
                os.environ[k] = v

# === CIRCUIT BREAKER ===

class CircuitBreaker:
    """Circuit breaker pattern for API calls"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = 'closed'  # closed, open, half_open
        
    def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == 'open':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'half_open'
            else:
                raise CircuitOpenError("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            if self.state == 'half_open':
                self.state = 'closed'
                self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold:
                self.state = 'open'
            raise
        
    @property
    def status(self) -> Dict:
        return {
            'state': self.state,
            'failures': self.failures,
            'last_failure': self.last_failure_time
        }

class CircuitOpenError(Exception):
    pass

# Global circuit breakers
binance_circuit = CircuitBreaker(failure_threshold=5, timeout=60)
telegram_circuit = CircuitBreaker(failure_threshold=3, timeout=30)

# === RATE LIMITER ===

class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = deque()
        self.lock = threading.Lock()
        
    def acquire(self) -> bool:
        with self.lock:
            now = time.time()
            
            # Remove old requests
            while self.requests and self.requests[0] < now - self.window_seconds:
                self.requests.popleft()
            
            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return True
            
            return False
    
    def wait_and_acquire(self, max_wait: int = 60):
        """Wait until rate limit allows request"""
        start = time.time()
        while time.time() - start < max_wait:
            if self.acquire():
                return True
            time.sleep(1)
        return False
    
    @property
    def status(self) -> Dict:
        return {
            'remaining': self.max_requests - len(self.requests),
            'reset_in': self.window_seconds if self.requests else 0
        }

# Global rate limiters
binance_rate_limit = RateLimiter(max_requests=1200, window_seconds=60)  # Binance: 1200/min
telegram_rate_limit = RateLimiter(max_requests=30, window_seconds=60)  # Telegram: 30/sec

# === HEALTH CHECK ===

class HealthCheck:
    """System health monitoring"""
    
    def __init__(self):
        self.checks = {}
        self.last_check = None
        self.start_time = time.time()
        self.errors = deque(maxlen=100)
        
    def register_check(self, name: str, check_func: Callable):
        self.checks[name] = check_func
        
    def run_check(self, name: str) -> Dict:
        if name not in self.checks:
            return {'status': 'unknown', 'message': 'Check not found'}
        
        try:
            result = self.checks[name]()
            return {'status': 'healthy' if result else 'unhealthy', 'result': result}
        except Exception as e:
            self.errors.append({
                'time': time.time(),
                'check': name,
                'error': str(e)
            })
            return {'status': 'error', 'error': str(e)}
        
    def run_all_checks(self) -> Dict:
        results = {}
        for name in self.checks:
            results[name] = self.run_check(name)
        
        self.last_check = time.time()
        
        overall = 'healthy'
        if any(r['status'] == 'error' for r in results.values()):
            overall = 'degraded'
        if all(r['status'] == 'unhealthy' for r in results.values()):
            overall = 'unhealthy'
            
        return {
            'overall': overall,
            'checks': results,
            'uptime': time.time() - self.start_time,
            'last_check': self.last_check
        }
    
    def add_error(self, source: str, error: str):
        self.errors.append({
            'time': time.time(),
            'source': source,
            'error': error
        })
    
    def get_recent_errors(self, count: int = 10) -> list:
        return list(self.errors)[-count:]

# Global health check
health_check = HealthCheck()

# === ERROR RECOVERY ===

class ErrorRecovery:
    """Auto-recovery from common errors"""
    
    def __init__(self):
        self.recovery_actions = {}
        
    def register_action(self, error_type: str, action: Callable):
        self.recovery_actions[error_type] = action
        
    def attempt_recovery(self, error: Exception, context: Dict) -> bool:
        error_type = type(error).__name__
        
        if error_type in self.recovery_actions:
            try:
                self.recovery_actions[error_type](error, context)
                return True
            except:
                return False
        
        return False

# Global error recovery
error_recovery = ErrorRecovery()

# === LOGGING ===

class StructuredLogger:
    """Structured logging with rotation"""
    
    def __init__(self, log_dir: str, max_size_mb: int = 10, max_files: int = 5):
        self.log_dir = log_dir
        self.max_size = max_size_mb * 1024 * 1024
        self.max_files = max_files
        self.current_file = os.path.join(log_dir, 'scanner.log')
        
    def _should_rotate(self) -> bool:
        if not os.path.exists(self.current_file):
            return False
        return os.path.getsize(self.current_file) > self.max_size
    
    def _rotate(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
        # Rename existing files
        for i in range(self.max_files - 1, 0, -1):
            old = f"{self.current_file}.{i}"
            new = f"{self.current_file}.{i + 1}"
            if os.path.exists(old):
                if i == self.max_files - 1:
                    os.remove(old)
                else:
                    os.rename(old, new)
        
        if os.path.exists(self.current_file):
            os.rename(self.current_file, f"{self.current_file}.1")
    
    def log(self, level: str, message: str, **kwargs):
        if self._should_rotate():
            self._rotate()
            
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'level': level,
            'message': message,
            **kwargs
        }
        
        with open(self.current_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def info(self, message: str, **kwargs):
        self.log('INFO', message, **kwargs)
        
    def warning(self, message: str, **kwargs):
        self.log('WARNING', message, **kwargs)
        
    def error(self, message: str, **kwargs):
        self.log('ERROR', message, **kwargs)

# Global logger
logger = StructuredLogger(script_dir)

# === API WRAPPER ===

def safe_api_call(func: Callable, *args, 
                 rate_limiter: RateLimiter = None,
                 circuit_breaker: CircuitBreaker = None,
                 max_retries: int = 3,
                 **kwargs) -> Dict:
    """Safe API call with all protections"""
    
    # Rate limiting
    if rate_limiter and not rate_limiter.wait_and_acquire():
        logger.warning('Rate limit exceeded', function=func.__name__)
        return {'error': 'Rate limit exceeded'}
    
    # Retry with circuit breaker
    for attempt in range(max_retries):
        try:
            if circuit_breaker:
                result = circuit_breaker.call(func, *args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            # Check for API errors in response
            if isinstance(result, dict):
                if 'code' in result and result.get('code') != 200:
                    logger.warning('API returned error', code=result.get('code'), msg=result.get('msg'))
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
            
            return result
            
        except CircuitOpenError:
            return {'error': 'Circuit breaker open'}
            
        except requests.exceptions.RequestException as e:
            logger.error('Request failed', error=str(e), attempt=attempt + 1)
            health_check.add_error(func.__name__, str(e))
            
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                return {'error': str(e)}
                
        except Exception as e:
            logger.error('Unexpected error', error=str(e), traceback=traceback.format_exc())
            health_check.add_error(func.__name__, str(e))
            return {'error': str(e)}
    
    return {'error': 'Max retries exceeded'}

# === HEALTH CHECKS ===

def check_binance_api() -> bool:
    """Check if Binance API is responsive"""
    import requests
    try:
        r = requests.get('https://api.binance.com/api/v3/ping', timeout=5)
        return r.status_code == 200
    except:
        return False

def check_disk_space() -> bool:
    """Check if disk space is sufficient"""
    import shutil
    stat = shutil.disk_usage('/')
    return stat.free / stat.total > 0.1  # More than 10% free

def check_memory() -> bool:
    """Check if memory is sufficient"""
    import psutil
    return psutil.virtual_memory().percent < 90

# Register health checks
health_check.register_check('binance_api', check_binance_api)
health_check.register_check('disk_space', check_disk_space)
health_check.register_check('memory', check_memory)

# === RECOVERY ACTIONS ===

def restart_scanner_action(error, context):
    """Auto-restart scanner on critical error"""
    logger.warning('Attempting to restart scanner', error=str(error))
    os.system('cd /root/.openclaw/workspace/neko-futures-trader && nohup python3 scanner-v8.py > scanner.log 2>&1 &')

def restart_price_monitor_action(error, context):
    """Auto-restart price monitor on critical error"""
    logger.warning('Attempting to restart price monitor', error=str(error))
    os.system('cd /root/.openclaw/workspace/neko-futures-trader && nohup python3 price-monitor.py > price-monitor.log 2>&1 &')

error_recovery.register_action('ConnectionError', restart_scanner_action)
error_recovery.register_action('Timeout', restart_price_monitor_action)

if __name__ == '__main__':
    # Test health check
    print("Running health checks...")
    result = health_check.run_all_checks()
    print(json.dumps(result, indent=2))
