"""Capture lifecycle limits only; never changes trading or risk gates."""


def validate_plan(plan):
    continuous = (plan.get('version') == 2 and
                  plan.get('run_policy') == 'UNTIL_USER_STOPS')
    for field in ('deadline_ms', 'max_capture_bytes'):
        value = plan[field]
        if value is None and continuous:
            continue
        if type(value) is not int or value <= 0:
            raise ValueError(f'{field} must be positive; null requires explicit continuous policy')
    if type(plan['minimum_free_bytes']) is not int or plan['minimum_free_bytes'] < 5 * 2**30:
        raise ValueError('minimum 5 GiB free-disk protection required')


def deadline_reached(plan, host_ms):
    deadline = plan['deadline_ms']
    return deadline is not None and host_ms >= deadline


def storage_limit_reached(total_bytes, max_bytes, free_bytes, min_free):
    return ((max_bytes is not None and total_bytes > max_bytes) or free_bytes < min_free)
