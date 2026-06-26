class GreenTeaLoader:
    def __init__(self):
        self.active = False
    
    def activate(self):
        self.active = True
        return "綠茶技能包已加載！切換至撒嬌模式～ 🍵"
    
    def deactivate(self):
        self.active = False
        return "綠茶技能包已關閉。回歸真實 Yua～"
    
    def is_active(self):
        return self.active
