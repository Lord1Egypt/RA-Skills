"""Fixture: a method that recurses through its own receiver."""
class Tree:
    """A node holding children."""

    def walk(self, depth):
        """Visit the children."""
        if depth:
            return self.walk(depth - 1)
        return 0
