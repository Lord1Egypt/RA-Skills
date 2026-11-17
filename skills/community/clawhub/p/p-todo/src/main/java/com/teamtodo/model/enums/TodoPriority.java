package com.teamtodo.model.enums;

import com.teamtodo.util.I18n;

public enum TodoPriority {
    LOW("priority.low"),
    MEDIUM("priority.medium"),
    HIGH("priority.high"),
    URGENT("priority.urgent");

    private final String labelKey;

    TodoPriority(String labelKey) { this.labelKey = labelKey; }

    public String getLabel() { return I18n.t(labelKey); }

    public static TodoPriority fromLabel(String label) {
        for (TodoPriority p : values()) {
            if (p.labelKey.equals(label)) return p;
        }
        return MEDIUM;
    }
}
