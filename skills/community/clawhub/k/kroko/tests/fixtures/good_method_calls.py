"""Fixture: functions whose names match methods called on other objects."""
def get(store, key):
    """Read one value through the store."""
    return store.get(key)


def copy(source):
    """Copy through a delegate."""
    return source.copy()
