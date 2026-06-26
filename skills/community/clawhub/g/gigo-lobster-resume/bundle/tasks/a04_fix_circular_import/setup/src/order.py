from src.user import User  # circular


class Order:
    def __init__(self, user, items):
        self.user = user
        self.items = items

    @classmethod
    def create_for(cls, user, items):
        assert isinstance(user, User)
        return cls(user, items)
