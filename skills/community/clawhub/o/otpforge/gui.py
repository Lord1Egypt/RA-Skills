from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

try:
    from .core import OtpEntry, Vault, format_entry_name, render_codes
except ImportError:  # Allows running as `python gui.py`
    from core import OtpEntry, Vault, format_entry_name, render_codes


class OtpForgeApp:
    def __init__(self, root: tk.Tk, vault: Vault) -> None:
        self.root = root
        self.vault = vault
        self.root.title("OtpForge")
        self.root.geometry("760x460")
        self.root.minsize(700, 380)

        self.label_var = tk.StringVar()
        self.issuer_var = tk.StringVar()
        self.secret_var = tk.StringVar()
        self.digits_var = tk.StringVar(value="6")
        self.period_var = tk.StringVar(value="30")
        self._refresh_timer: str | None = None

        self._build_ui()
        self.refresh_rows()
        self._schedule_refresh()

    def _build_ui(self) -> None:
        top = ttk.Frame(self.root, padding=12)
        top.pack(fill=tk.X)

        ttk.Label(top, text="Label").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(top, textvariable=self.label_var, width=26).grid(row=1, column=0, padx=(0, 8), sticky=tk.W)

        ttk.Label(top, text="Issuer").grid(row=0, column=1, sticky=tk.W)
        ttk.Entry(top, textvariable=self.issuer_var, width=20).grid(row=1, column=1, padx=(0, 8), sticky=tk.W)

        ttk.Label(top, text="Secret (Base32)").grid(row=0, column=2, sticky=tk.W)
        self.show_secret_var = tk.BooleanVar(value=False)

        self.secret_entry = ttk.Entry(top, textvariable=self.secret_var, width=36, show="*")
        self.secret_entry.grid(row=1, column=2, padx=(0, 8), sticky=tk.W)

        ttk.Checkbutton(
            top,
            text="Show",
            variable=self.show_secret_var,
            command=self._toggle_secret_visibility,
        ).grid(row=1, column=5, padx=(0, 0), sticky=tk.W)

        ttk.Label(top, text="Digits").grid(row=0, column=3, sticky=tk.W)
        ttk.Entry(top, textvariable=self.digits_var, width=6).grid(row=1, column=3, padx=(0, 8), sticky=tk.W)

        ttk.Label(top, text="Period").grid(row=0, column=4, sticky=tk.W)
        ttk.Entry(top, textvariable=self.period_var, width=6).grid(row=1, column=4, padx=(0, 8), sticky=tk.W)

        top.grid_columnconfigure(2, weight=1)

        controls = ttk.Frame(self.root, padding=(12, 0, 12, 8))
        controls.pack(fill=tk.X)
        ttk.Button(controls, text="Save / Update", command=self.save_entry).pack(side=tk.LEFT)
        ttk.Button(controls, text="Copy Code", command=self.copy_selected_code).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(controls, text="Remove Selected", command=self.remove_selected).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(controls, text="Refresh", command=self.refresh_rows).pack(side=tk.LEFT, padx=(8, 0))

        table_frame = ttk.Frame(self.root, padding=(12, 0, 12, 12))
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("label", "code", "remaining"),
            show="headings",
            selectmode="browse",
        )
        self.tree.heading("label", text="Account")
        self.tree.heading("code", text="Code")
        self.tree.heading("remaining", text="Expires In")
        self.tree.column("label", width=420)
        self.tree.column("code", width=120, anchor=tk.CENTER)
        self.tree.column("remaining", width=100, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-1>", self._on_tree_double_click)

        self.status = ttk.Label(self.root, text="", padding=(12, 0, 12, 8))
        self.status.pack(fill=tk.X)

    def set_status(self, text: str) -> None:
        self.status.configure(text=text)

    def _toggle_secret_visibility(self) -> None:
        show = "" if self.show_secret_var.get() else "*"
        self.secret_entry.configure(show=show)

    def _on_tree_double_click(self, _event: object) -> None:
        # Double click = copy the selected code
        self.copy_selected_code()

    def copy_selected_code(self) -> None:
        selected = self.tree.selection()
        if not selected:
            self.set_status("No entry selected")
            return

        label = selected[0]
        values = self.tree.item(label, "values")
        if not values or len(values) < 2:
            self.set_status("No code available")
            return

        code = str(values[1])
        self.root.clipboard_clear()
        self.root.clipboard_append(code)
        self.set_status(f"Copied code for {label}")

    def save_entry(self) -> None:
        try:
            entry = OtpEntry(
                label=self.label_var.get().strip(),
                issuer=self.issuer_var.get().strip(),
                secret=self.secret_var.get().strip(),
                digits=int(self.digits_var.get()),
                period=int(self.period_var.get()),
            )
            self.vault.upsert(entry)
        except Exception as exc:
            messagebox.showerror("Save failed", str(exc), parent=self.root)
            return

        self.secret_var.set("")
        self.set_status(f"Saved {entry.label}")
        self.refresh_rows()

    def remove_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            self.set_status("No entry selected")
            return
        label = selected[0]
        if not self.vault.remove(label):
            self.set_status("Entry already removed")
            self.refresh_rows()
            return
        self.set_status(f"Removed {label}")
        self.refresh_rows()

    def refresh_rows(self) -> None:
        selected = self.tree.selection()
        selected_label = selected[0] if selected else None

        for iid in self.tree.get_children():
            self.tree.delete(iid)

        entries = self.vault.list_entries()
        for entry, code, remain in render_codes(entries):
            self.tree.insert(
                "",
                tk.END,
                iid=entry.label,
                values=(format_entry_name(entry), code, f"{remain}s"),
            )

        if selected_label and self.tree.exists(selected_label):
            self.tree.selection_set(selected_label)

    def _schedule_refresh(self) -> None:
        if self._refresh_timer is not None:
            self.root.after_cancel(self._refresh_timer)
        self._refresh_timer = self.root.after(1000, self._tick_refresh)

    def _tick_refresh(self) -> None:
        self.refresh_rows()
        self._schedule_refresh()


def launch(vault: Vault | None = None) -> None:
    root = tk.Tk()
    app = OtpForgeApp(root, vault or Vault())
    app.set_status("Ready")
    root.mainloop()


if __name__ == "__main__":
    launch()
