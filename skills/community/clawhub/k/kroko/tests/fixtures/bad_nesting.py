"""Fixture: control flow nested past the depth limit."""
def _deep(flag):
    """Walk four levels of nesting."""
    if flag == 1:
        if flag == 2:
            if flag == 3:
                if flag == 4:
                    return 4
    return 0
