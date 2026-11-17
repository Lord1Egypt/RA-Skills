package com.teamtodo.model.enums;

import com.teamtodo.util.I18n;

public enum TodoStatus {
    PENDING("status.pending"),
    IN_PROGRESS("status.inProgress"),
    DONE("status.done"),
    CANCELLED("status.overdue");

    private final String labelKey;

    TodoStatus(String labelKey) { this.labelKey = labelKey; }

    public String getLabel() { return I18n.t(labelKey); }

    public static TodoStatus fromLabel(String label) {
        for (TodoStatus s : values()) {
            if (s.labelKey.equals(label)) return s;
        }
        return PENDING;
    }
}
