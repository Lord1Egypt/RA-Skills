"""
Meta Debugger - Self-diagnosing and self-healing AI system
"""
import json
import traceback
import time
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from collections import defaultdict
from functools import wraps
import random


@dataclass
class ErrorRecord:
    """Record of an error"""
    id: str
    error_type: str
    error_message: str
    context: Dict
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    stack_trace: str = ""
    root_cause: str = ""
    severity: str = "medium"


@dataclass
class FixRecord:
    """Record of a fix"""
    id: str
    error_id: str
    fix_type: str
    fix_description: str
    fix_code: str = ""
    success: bool = False
    applied_at: str = ""
    result: str = ""


@dataclass
class ErrorPattern:
    """Pattern for an error type"""
    error_type: str
    causes: List[str]
    fixes: List[str]
    prevention: List[str]
    frequency: int = 0
    success_rate: float = 0.0


class MetaDebugger:
    """
    Self-diagnosing and self-healing AI debugger
    
    Features:
    - Error detection and analysis
    - Root cause identification
    - Fix generation and application
    - Learning from errors
    - Prevention through patterns
    """
    
    # Common error patterns
    ERROR_PATTERNS = {
        "TimeoutError": {
            "causes": ["network_slow", "server_busy", "query_complex"],
            "fixes": ["retry", "increase_timeout", "cache"],
            "prevention": ["timeout_guards", "circuit_breaker"]
        },
        "ConnectionError": {
            "causes": ["network_down", "server_unavailable", "dns_failure"],
            "fixes": ["retry", "reconnect", "fallback"],
            "prevention": ["health_check", "load_balancer"]
        },
        "ValueError": {
            "causes": ["type_mismatch", "invalid_format", "out_of_range"],
            "fixes": ["type_conversion", "validation", "default_value"],
            "prevention": ["input_validation", "schema_check"]
        },
        "TypeError": {
            "causes": ["wrong_type", "null_reference", "attribute_missing"],
            "fixes": ["type_check", "null_check", "try_except"],
            "prevention": ["type_hints", "null_safety"]
        },
        "KeyError": {
            "causes": ["missing_key", "wrong_dict", "case_mismatch"],
            "fixes": ["get_default", "membership_check", "normalize_key"],
            "prevention": ["dict_validation", "schema_validation"]
        },
        "PermissionError": {
            "causes": ["no_permission", "read_only", "expired_token"],
            "fixes": ["request_permission", "refresh_token", "use_cache"],
            "prevention": ["permission_check", "token_refresh"]
        },
        "RateLimitError": {
            "causes": ["too_many_requests", "quota_exceeded", "api_limit"],
            "fixes": ["backoff", "queue_requests", "use_alternative"],
            "prevention": ["rate_limiter", "request_throttle"]
        }
    }
    
    def __init__(
        self,
        name: str = "default",
        auto_fix: bool = False,
        safe_mode: bool = True,
        max_retries: int = 3,
        storage_path: str = None
    ):
        self.name = name
        self.auto_fix = auto_fix
        self.safe_mode = safe_mode
        self.max_retries = max_retries
        
        # Storage
        storage_path = storage_path or f"~/.meta_debugger/{name}"
        self.storage_path = storage_path
        
        # Error tracking
        self.error_history: List[ErrorRecord] = []
        self.fix_history: List[FixRecord] = []
        self.patterns: Dict[str, ErrorPattern] = {}
        
        # Handlers
        self.error_handlers: Dict[str, Callable] = {}
        
        # Guardrails
        self.guardrails: List[Callable] = []
        
        # Metrics
        self.metrics = {
            'total_errors': 0,
            'fixed_errors': 0,
            'failed_fixes': 0,
            'prevented_errors': 0
        }
        
        # Initialize patterns
        self._init_patterns()
    
    def _init_patterns(self):
        """Initialize error patterns"""
        for error_type, pattern_data in self.ERROR_PATTERNS.items():
            self.patterns[error_type] = ErrorPattern(
                error_type=error_type,
                causes=pattern_data['causes'],
                fixes=pattern_data['fixes'],
                prevention=pattern_data['prevention']
            )
    
    # ==================== Error Handling ====================
    
    def error_handler(self, error_type: str = None):
        """Decorator for error handlers"""
        def decorator(func: Callable):
            self.error_handlers[error_type or func.__name__] = func
            return func
        return decorator
    
    def register_handler(self, error_type: str, handler: Callable):
        """Register a custom error handler"""
        self.error_handlers[error_type] = handler
    
    def handle(self, error: Exception, context: Dict = None) -> Dict:
        """
        Handle an error
        
        Args:
            error: The exception that occurred
            context: Additional context about the error
            
        Returns:
            Dict with handling result
        """
        context = context or {}
        
        # Record error
        error_record = self._record_error(error, context)
        
        # Analyze error
        analysis = self.analyze(error, context)
        
        # Get fix suggestions
        fixes = self.generate_fixes(error, analysis)
        
        # Apply fix if enabled
        result = {'error': error_record, 'analysis': analysis, 'fixes': fixes}
        
        if self.auto_fix and fixes:
            # Apply best fix
            applied_fix = self.apply_fix(fixes[0])
            result['applied_fix'] = applied_fix
        
        return result
    
    def _record_error(self, error: Exception, context: Dict) -> ErrorRecord:
        """Record error to history"""
        error_type = type(error).__name__
        error_message = str(error)
        
        # Get stack trace
        stack_trace = traceback.format_exc()
        
        # Analyze root cause
        root_cause = self._analyze_root_cause(error_type, error_message, stack_trace)
        
        # Determine severity
        severity = self._determine_severity(error_type, error_message)
        
        # Create record
        record = ErrorRecord(
            id=f"err_{len(self.error_history)}_{int(time.time())}",
            error_type=error_type,
            error_message=error_message,
            context=context,
            stack_trace=stack_trace,
            root_cause=root_cause,
            severity=severity
        )
        
        self.error_history.append(record)
        self.metrics['total_errors'] += 1
        
        # Update pattern frequency
        if error_type in self.patterns:
            self.patterns[error_type].frequency += 1
        
        return record
    
    def _analyze_root_cause(
        self,
        error_type: str,
        error_message: str,
        stack_trace: str
    ) -> str:
        """Analyze root cause of error"""
        msg_lower = error_message.lower()
        
        # Pattern-based analysis
        if error_type == "TimeoutError":
            if "connection" in msg_lower:
                return "Connection timeout - server took too long to respond"
            elif "read" in msg_lower:
                return "Read timeout - slow network or large response"
            return "Request timeout - operation took too long"
        
        elif error_type == "ValueError":
            if "invalid" in msg_lower:
                return f"Invalid value: {error_message}"
            elif "range" in msg_lower:
                return f"Value out of range: {error_message}"
            return f"Value error: {error_message}"
        
        elif error_type == "KeyError":
            # Extract key from message
            match = re.search(r"['\"](.+?)['\"]", error_message)
            key = match.group(1) if match else "unknown"
            return f"Missing key: '{key}'"
        
        elif error_type == "ConnectionError":
            if "refused" in msg_lower:
                return "Connection refused - server not running or port blocked"
            elif "reset" in msg_lower:
                return "Connection reset - server closed connection"
            return f"Connection failed: {error_message}"
        
        elif error_type == "PermissionError":
            if "denied" in msg_lower:
                return "Permission denied - insufficient permissions"
            elif "read-only" in msg_lower:
                return "Read-only - cannot modify"
            return f"Permission error: {error_message}"
        
        # Default
        return f"{error_type}: {error_message[:100]}"
    
    def _determine_severity(self, error_type: str, error_message: str) -> str:
        """Determine error severity"""
        # Critical errors
        critical = ["MemoryError", "SystemError", "KeyboardInterrupt"]
        if error_type in critical:
            return "critical"
        
        # High severity
        high = ["ConnectionError", "PermissionError", "AuthenticationError"]
        if error_type in high:
            if "expired" in error_message.lower() or "auth" in error_message.lower():
                return "critical"
            return "high"
        
        # Medium severity
        medium = ["ValueError", "TypeError", "KeyError", "TimeoutError"]
        if error_type in medium:
            return "medium"
        
        # Low severity
        return "low"
    
    # ==================== Analysis ====================
    
    def analyze(self, error: Exception, context: Dict = None) -> Dict:
        """
        Analyze error and return detailed analysis
        
        Args:
            error: The exception
            context: Error context
            
        Returns:
            Dict with analysis results
        """
        context = context or {}
        error_type = type(error).__name__
        error_message = str(error)
        
        # Get pattern info
        pattern = self.patterns.get(error_type, ErrorPattern(
            error_type=error_type,
            causes=["unknown"],
            fixes=["investigate"],
            prevention=["add_logging"]
        ))
        
        # Find similar past errors
        similar = self._find_similar_errors(error_type, error_message)
        
        # Build analysis
        analysis = {
            'error_type': error_type,
            'error_message': error_message,
            'severity': self._determine_severity(error_type, error_message),
            'root_cause': self._analyze_root_cause(error_type, error_message, traceback.format_exc()),
            'possible_causes': pattern.causes,
            'context': context,
            'similar_errors': similar,
            'suggestions': self._generate_suggestions(pattern, context)
        }
        
        return analysis
    
    def _find_similar_errors(self, error_type: str, error_message: str) -> List[Dict]:
        """Find similar past errors"""
        similar = []
        
        for record in self.error_history[-20:]:  # Last 20 errors
            if record.error_type == error_type:
                similar.append({
                    'message': record.error_message,
                    'timestamp': record.timestamp,
                    'root_cause': record.root_cause
                })
        
        return similar[:5]  # Return top 5
    
    def _generate_suggestions(self, pattern: ErrorPattern, context: Dict) -> List[str]:
        """Generate fix suggestions"""
        suggestions = []
        
        # Add fix suggestions
        for fix in pattern.fixes[:3]:
            suggestions.append(f"Try: {fix}")
        
        # Add prevention suggestions
        for prev in pattern.prevention[:2]:
            suggestions.append(f"Prevent: {prev}")
        
        # Add context-specific suggestions
        if context.get('function'):
            suggestions.append(f"Add error handling to: {context['function']}")
        
        return suggestions
    
    def get_stack_trace(self, error: Exception) -> Dict:
        """Parse stack trace"""
        tb = traceback.extract_tb(error.__traceback__)
        
        return {
            'type': type(error).__name__,
            'message': str(error),
            'frames': [
                {
                    'file': frame.filename,
                    'line': frame.lineno,
                    'function': frame.name,
                    'code': frame.line
                }
                for frame in tb
            ]
        }
    
    # ==================== Fix Generation ====================
    
    def generate_fixes(self, error: Exception, analysis: Dict = None) -> List[Dict]:
        """
        Generate fix candidates
        
        Args:
            error: The exception
            analysis: Optional analysis result
            
        Returns:
            List of fix candidates
        """
        analysis = analysis or self.analyze(error)
        error_type = analysis['error_type']
        
        fixes = []
        
        # Get pattern-based fixes
        pattern = self.patterns.get(error_type)
        if pattern:
            for fix_type in pattern.fixes:
                fix = self._create_fix(fix_type, error, analysis)
                fixes.append(fix)
        
        # Add generic fixes
        fixes.extend([
            {
                'type': 'retry',
                'description': 'Retry the operation',
                'action': {'max_retries': 3, 'backoff': 'exponential'},
                'probability': 0.7
            },
            {
                'type': 'log',
                'description': 'Log error and continue',
                'action': {'log': True, 'continue': True},
                'probability': 0.5
            }
        ])
        
        # Rank fixes
        return self.rank_fixes(fixes)
    
    def _create_fix(self, fix_type: str, error: Exception, analysis: Dict) -> Dict:
        """Create a specific fix"""
        fix_templates = {
            'retry': {
                'type': 'retry',
                'description': 'Retry with exponential backoff',
                'action': {'max_retries': 3, 'backoff': 'exponential', 'base': 2},
                'probability': 0.7
            },
            'increase_timeout': {
                'type': 'increase_timeout',
                'description': 'Increase timeout and retry',
                'action': {'timeout': 60, 'retry': True},
                'probability': 0.6
            },
            'cache': {
                'type': 'cache',
                'description': 'Use cached result',
                'action': {'use_cache': True},
                'probability': 0.5
            },
            'fallback': {
                'type': 'fallback',
                'description': 'Use fallback service',
                'action': {'fallback': True},
                'probability': 0.4
            },
            'type_conversion': {
                'type': 'type_conversion',
                'description': 'Convert to correct type',
                'action': {'convert': True},
                'probability': 0.8
            },
            'validation': {
                'type': 'validation',
                'description': 'Add input validation',
                'action': {'validate': True},
                'probability': 0.9
            },
            'default_value': {
                'type': 'default_value',
                'description': 'Use default value',
                'action': {'default': None},
                'probability': 0.6
            },
            'get_default': {
                'type': 'get_default',
                'description': 'Use dict.get() with default',
                'action': {'use_get': True, 'default': None},
                'probability': 0.8
            },
            'reconnect': {
                'type': 'reconnect',
                'description': 'Reconnect and retry',
                'action': {'reconnect': True, 'retry': True},
                'probability': 0.7
            },
            'refresh_token': {
                'type': 'refresh_token',
                'description': 'Refresh authentication token',
                'action': {'refresh': True},
                'probability': 0.9
            },
            'backoff': {
                'type': 'backoff',
                'description': 'Apply rate limit backoff',
                'action': {'backoff': True, 'delay': 60},
                'probability': 0.8
            }
        }
        
        return fix_templates.get(fix_type, {
            'type': fix_type,
            'description': f'Apply fix: {fix_type}',
            'action': {},
            'probability': 0.5
        })
    
    def rank_fixes(self, fixes: List[Dict]) -> List[Dict]:
        """Rank fixes by probability of success"""
        # Learn from history
        for fix in fixes:
            fix_type = fix['type']
            
            # Check success rate from history
            successes = sum(
                1 for f in self.fix_history
                if f.fix_type == fix_type and f.success
            )
            total = sum(1 for f in self.fix_history if f.fix_type == fix_type)
            
            if total > 0:
                historical_rate = successes / total
                # Blend with default probability
                fix['probability'] = (fix['probability'] + historical_rate) / 2
        
        # Sort by probability
        return sorted(fixes, key=lambda x: x.get('probability', 0), reverse=True)
    
    def apply_fix(self, fix: Dict) -> Dict:
        """
        Apply a fix
        
        Args:
            fix: Fix to apply
            
        Returns:
            Result of applying fix
        """
        # In safe mode, just return the fix without applying
        if self.safe_mode:
            return {
                'applied': False,
                'reason': 'safe_mode_enabled',
                'fix': fix,
                'suggestion': 'Review fix and apply manually or set safe_mode=False'
            }
        
        # Record fix attempt
        fix_record = FixRecord(
            id=f"fix_{len(self.fix_history)}_{int(time.time())}",
            error_id=self.error_history[-1].id if self.error_history else "",
            fix_type=fix['type'],
            fix_description=fix['description'],
            fix_code=str(fix.get('action', {})),
            applied_at=datetime.now().isoformat()
        )
        
        # Try to apply (simplified - actual implementation would depend on context)
        try:
            # This would be where actual fix logic goes
            fix_record.success = True
            fix_record.result = "Fix applied successfully"
            self.metrics['fixed_errors'] += 1
        except Exception as e:
            fix_record.success = False
            fix_record.result = str(e)
            self.metrics['failed_fixes'] += 1
        
        self.fix_history.append(fix_record)
        
        return {
            'applied': fix_record.success,
            'fix': fix,
            'result': fix_record.result
        }
    
    # ==================== Prevention ====================
    
    def add_guardrail(self, check: Callable, name: str = None):
        """Add a pre-execution guardrail check"""
        self.guardrails.append({
            'name': name or check.__name__,
            'check': check
        })
    
    def validate_input(self, input_value: Any, rules: Dict) -> Dict:
        """
        Validate input against rules
        
        Args:
            input_value: Value to validate
            rules: Validation rules
            
        Returns:
            Validation result
        """
        errors = []
        
        # Type check
        if 'type' in rules:
            expected_type = rules['type']
            if not isinstance(input_value, expected_type):
                errors.append(f"Expected type {expected_type}, got {type(input_value)}")
        
        # Range check
        if 'min' in rules and input_value < rules['min']:
            errors.append(f"Value {input_value} below minimum {rules['min']}")
        
        if 'max' in rules and input_value > rules['max']:
            errors.append(f"Value {input_value} above maximum {rules['max']}")
        
        # Enum check
        if 'enum' in rules and input_value not in rules['enum']:
            errors.append(f"Value not in allowed values: {rules['enum']}")
        
        # Pattern check
        if 'pattern' in rules and isinstance(input_value, str):
            if not re.match(rules['pattern'], input_value):
                errors.append(f"Value doesn't match pattern: {rules['pattern']}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'value': input_value
        }
    
    def build_pattern(self, error: Exception, context: Dict = None):
        """Build error pattern from error"""
        error_type = type(error).__name__
        
        if error_type not in self.patterns:
            self.patterns[error_type] = ErrorPattern(
                error_type=error_type,
                causes=[],
                fixes=[],
                prevention=[]
            )
        
        # Update pattern
        self.patterns[error_type].frequency += 1
    
    # ==================== Learning ====================
    
    def record_error(self, error: Exception, context: Dict = None):
        """Record error for learning"""
        self._record_error(error, context or {})
    
    def record_fix(self, error_id: str, fix: Dict, success: bool):
        """Record fix result for learning"""
        record = FixRecord(
            id=f"fix_{len(self.fix_history)}_{int(time.time())}",
            error_id=error_id,
            fix_type=fix.get('type', 'unknown'),
            fix_description=fix.get('description', ''),
            success=success,
            result='success' if success else 'failed'
        )
        
        self.fix_history.append(record)
        
        # Update pattern success rate
        error_record = next((e for e in self.error_history if e.id == error_id), None)
        if error_record:
            pattern = self.patterns.get(error_record.error_type)
            if pattern:
                total = sum(1 for f in self.fix_history if f.fix_type in pattern.fixes)
                successes = sum(1 for f in self.fix_history if f.fix_type in pattern.fixes and f.success)
                pattern.success_rate = successes / total if total > 0 else 0
    
    def get_insights(self) -> Dict:
        """Get learned insights"""
        insights = {
            'total_errors': self.metrics['total_errors'],
            'fix_success_rate': self.metrics['fixed_errors'] / max(1, self.metrics['total_errors']),
            'common_errors': self._get_common_errors(),
            'effective_fixes': self._get_effective_fixes(),
            'patterns': [
                {
                    'type': p.error_type,
                    'frequency': p.frequency,
                    'success_rate': p.success_rate
                }
                for p in sorted(self.patterns.values(), key=lambda x: x.frequency, reverse=True)[:10]
            ]
        }
        
        return insights
    
    def _get_common_errors(self) -> List[Dict]:
        """Get most common errors"""
        error_counts = defaultdict(int)
        for record in self.error_history:
            error_counts[record.error_type] += 1
        
        return [
            {'type': k, 'count': v}
            for k, v in sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
    
    def _get_effective_fixes(self) -> List[Dict]:
        """Get most effective fixes"""
        fix_success = defaultdict(lambda: {'success': 0, 'total': 0})
        
        for record in self.fix_history:
            fix_success[record.fix_type]['total'] += 1
            if record.success:
                fix_success[record.fix_type]['success'] += 1
        
        return [
            {
                'fix': k,
                'success_rate': v['success'] / max(1, v['total']),
                'total_attempts': v['total']
            }
            for k, v in sorted(
                fix_success.items(),
                key=lambda x: x[1]['success'] / max(1, x[1]['total']),
                reverse=True
            )[:5]
        ]
    
    # ==================== Decorator ====================
    
    def wrap(self, func: Callable):
        """Decorator to wrap functions with error handling"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                result = self.handle(e, {
                    'function': func.__name__,
                    'args': str(args)[:100],
                    'kwargs': str(kwargs)[:100]
                })
                
                if self.auto_fix and result.get('applied_fix', {}).get('applied'):
                    # Retry with fix - simplified
                    return func(*args, **kwargs)
                
                raise
        
        return wrapper
    
    # ==================== Metrics ====================
    
    def get_metrics(self) -> Dict:
        """Get debugging metrics"""
        return {
            **self.metrics,
            'error_history_size': len(self.error_history),
            'fix_history_size': len(self.fix_history),
            'patterns_count': len(self.patterns),
            'guardrails_count': len(self.guardrails)
        }
    
    def reset_metrics(self):
        """Reset metrics"""
        self.metrics = {
            'total_errors': 0,
            'fixed_errors': 0,
            'failed_fixes': 0,
            'prevented_errors': 0
        }


# Convenience function
def create_debugger(name: str = "default", **kwargs) -> MetaDebugger:
    """Create a MetaDebugger instance"""
    return MetaDebugger(name=name, **kwargs)
