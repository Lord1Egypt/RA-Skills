---
name: nasal-canvas-gui
description: Provides patterns for Nasal Canvas GUI — dialogs, windows, layouts, widgets, events, and message boxes.
---

# Canvas GUI

Canvas GUI is a framework for modern UI drawn using Canvas.

## Dialogs

Canvas dialogs are Nasal objects that build a `canvas.Window`, attach a canvas and a root group, populate it with `canvas.gui.widgets.*` instances through layouts, and return a table (`m`) that owns the whole tree.

### Skeleton

Every dialog follows this shape:

```nasal
var MyDialog = {
  new: func(width=400, height=300) {
    var m = {
      parents: [MyDialog],
      window: canvas.Window.new([width, height], "dialog")
    };

    m.window.set("title", "My Dialog")
            .setBool("resize", 1);

    m.root = m.window.getCanvas(1)
                    .set("background", canvas.style.getColor("bg_color"))
                    .createGroup();

    m.vbox = canvas.VBoxLayout.new();
    m.window.setLayout(m.vbox);

    # ... add widgets here ...

    var hint = m.vbox.sizeHint();
    hint[0] = math.max(width, hint[0]);
    m.window.setSize(hint);

    return m;
  },

  del: func {
    me.window.del();
  }
};

var dialog = MyDialog.new();
```

Rules the skeleton encodes:

- Every handle you later need (`window`, `root`, layouts, widgets) is stored on the object so `del` and callbacks can reach it.
- `m.parents: [MyDialog]` gives the object inheritance, so methods defined on `MyDialog` (`del`, helpers) are callable as `me.foo()`.
- `getCanvas(1)` creates the canvas if it does not exist. `createCanvas()` also works but additionally installs a mousedown listener and a placement.
- Set the background on the **canvas**, not the group.
- `setLayout` on the window makes the top-level layout drive the canvas size.
- Finish with `setSize(hint)` so the window fits its content instead of clipping.

## Window

`canvas.Window.new([w, h], type)` — `type` is `"dialog"` for a decorated, movable window; omit it for a borderless overlay.

| Call | Effect |
|---|---|
| `set("title", s)` / `setTitle(s)` | titlebar text |
| `setBool("resize", 1)` | allow user resizing |
| `set("resize", 1)` | same property via generic setter |
| `setPosition([x, y])` | `(0,0)` = top-left of screen |
| `setSize(w, h)` or `setSize([w, h])` | content size; calls `onResize` if defined |
| `move(x, y)` | relative move |
| `raise()` | bump z-index and focus |
| `setFocus()` / `clearFocus()` | focus bookkeeping with `gui` |
| `getSize()` | `[w, h]` |
| `del()` | destroy; canvas survives if other placements reference it |

`setBool("capture-events", 0)` makes the window click-through.

## Layouts

Layouts own geometry; widgets are added with `addItem`, never positioned by hand.

```nasal
var vbox = canvas.VBoxLayout.new();
var hbox = canvas.HBoxLayout.new();

vbox.setSpacing(0);
vbox.setContentsMargin(10);
vbox.addItem(someWidget);
hbox.addItem(vbox);
```

- Nest layouts to compose rows inside columns.
- `sizeHint()` returns `[w, h]` — feed it to `window.setSize()`.
- `ScrollArea` is a widget, not a layout: give it a layout via `setLayout()` and add children to `scrollArea.getContent()`.
- `TabWidget` is also a container: widgets added to a tab go on `tabWidget.getContent()`, and the tab body is a layout passed to `addTab`.

`BoxLayout` also exposes `addStretch()`, `addSpacing(n)`, `insertItem(i, item, stretch)`, `setStretchFactor(item, n)`, `setSpacing(n)`.

Use `addStretch()` to push a button row to the bottom of a VBox. `ScrollArea` and `TabWidget` expose `getContent()`; widgets inside a scroll area or tab are parented to that content group and placed in a layout assigned with `scrollArea.setLayout(l)`.

## Widgets

Construct as `canvas.gui.widgets.<Type>.new(parent, canvas.style, cfg)`, then chain setters. `parent` must be the container element the widget lives in — usually the tab content or the root group, **not** the layout object.

| Widget | Notable cfg / methods |
|---|---|
| `Button` | `setText`, `setFixedSize`, `setCheckable(1)`, `setChecked(0)`, event `clicked` / `toggled` |
| `Label` | `setText`, `setImage`, `setBackground`, `setAlignment(canvas.AlignBottom)`, `setVisible(0)` |
| `CheckBox` | `setText`, cfg `"label-position": "left"`, event `toggled` |
| `PropertyCheckBox` | cfg `"node": props.globals.getNode("/path")` — binds to a property |
| `RadioButton` | cfg `"parent-radio": otherRadio`; event `group-checked-radio-changed`; `getRadioButtonsGroup().getCheckedRadio()` |
| `Switch` | `setChecked(1)`, event `toggled` |
| `Slider` | cfg `"max-value"`, `"page-size"`, `"tick-step"`, `"value-style": gui.widgets.Slider.ValueStyle.Moving`, `"value-position"`, `"ticks-position"` |
| `Dial` | cfg `"min-value"`, `"max-value"`, `"step-size"`, `"value"`, `"value-format": "%.1f"`, `"wrap"`, `"show-value"`, `"show-ticks"`; setters `setShowValue`, `setShowTicks`, `setWrap` |
| `ComboBox` | `addMenuItem(text, id)`, `setFixedSize` |
| `List` | `createItem(text)`, `getSelectedItems()`, `setSizeHint([List._MAX_SIZE, List._MAX_SIZE])`, event `selection-changed` |
| `LineEdit` | single-line text input, `setText` |
| `ScrollArea` | `setLayout`, `getContent()`, `setSizeHint` |
| `TabWidget` | cfg `"tabs-closeable": 1`, `addTab(id, label, layout)`, `setCurrentTab(id)`, `getContent()` |
| `MenuBar` | `createMenu(label)` → `menu.createItem(text:, cb:, shortcut:)` |
| `HorizontalRule` | `setText(label)` to caption a section |

`setAlignment`, `setSizeHint`, `setFixedSize`, `setVisible` are available on the `gui.Widget` base class, so they work on every widget above.

## Events

Widgets use `listen(type, func)`:

```nasal
m.button.listen("clicked", func {
  MessageBox.information("Title", "Clicked!");
});

m.checkable.listen("toggled", func(e) {
  m.image.setVisible(int(e.detail.checked));
});
```

Canvas elements use `addEventListener(type, func(e))` and receive a MouseEvent with `screenX/Y`, `clientX/Y`, `localX/Y`, `deltaX/Y`, `click_count`, `button`, `buttons`:

```nasal
m.image._view._root.addEventListener("mousedown", func(e) {
  print("clicked at local " ~ e.localX ~ "," ~ e.localY);
});
```

Event types: `mousedown`, `mouseup`, `click`, `dblclick`, `drag`, `wheel`, `mousemove`, `mouseover`, `mouseout`, `mouseenter`, `mouseleave`, `keydown`, `keyup`, `keypress`. Only `mouseenter` / `mouseleave` do not bubble; call `e.stopPropagation()` to halt bubbling for the rest.

Canvases on a 3D model or in the scenery do **not** receive events by default — add `"capture-events": 1` to the placement.

## Message boxes

`canvas.MessageBox` shows a modal dialog without building a Window yourself — use it for confirmations, warnings, and blocking questions. Note it lives on `canvas`, not under `canvas.gui.widgets`; the bare `MessageBox` / `InputDialog` names used elsewhere are the higher-level convenience wrappers.

```nasal
canvas.MessageBox.information(title, text);              # OK only
canvas.MessageBox.warning(title, text);                  # non-critical
canvas.MessageBox.critical(title, text);                 # error / failure
canvas.MessageBox.question(title, text, cb, buttons);    # Yes/No by default
```

The optional callback receives the selected button, which you compare against the same constants. Combine buttons with `|`:

```nasal
canvas.MessageBox.warning(
  "Warning...",
  "Read this once and it can stay hidden.",
  func(sel) {
    if (sel != canvas.MessageBox.Ok)
      return;
    print("Acknowledged");
  },
  canvas.MessageBox.Ok
  | canvas.MessageBox.Cancel
  | canvas.MessageBox.DontShowAgain
);
```

Available buttons: `Ok`, `Cancel`, `Yes`, `No`, `DontShowAgain`. The callback gets only `sel` — title and text are not passed through.

The don't-show-again logic is handled internally by the library. It uses an md5 hash as a unique ID, so the selection persists across FlightGear restarts.

## Pitfalls

**Widget parent is a container element, not the layout.**

```nasal
# wrong — layout is not a canvas element
var b = canvas.gui.widgets.Button.new(m.vbox, canvas.style, {});

# right — add to the element, then to the layout
var b = canvas.gui.widgets.Button.new(m.root, canvas.style, {});
m.vbox.addItem(b);
```

**Pick one container per widget.** In a tabbed dialog, widgets built for a tab use `m.tabs.getContent()` as parent, while the menubar uses `m.root`. Mixing them silently puts widgets in the wrong place:

```nasal
m.menubar = canvas.gui.widgets.MenuBar.new(m.root, canvas.style, {});
m.vbox.addItem(m.menubar);

m.tabs = gui.widgets.TabWidget.new(m.root, style, {"tabs-closeable": 1});
m.vbox.addItem(m.tabs);

m.label = gui.widgets.Label.new(m.tabs.getContent(), style, {}).setText("Hi");
```

**Do not set background on the group.** `m.root.set("background", ...)` is a no-op for the window surface; use `getCanvas(1).set("background", ...)`.

**Reaching inside a widget.** Some widgets expose their canvas element under `_view._root` (private). Prefer `listen` over poking internals; when you must attach a canvas-level listener, use `_view._root` and accept the coupling.

**Always provide `del`.** Call `me.window.del()` and delete widgets that hold property listeners (`PropertyCheckBox`, sliders bound to nodes) so they stop updating after the dialog closes.

**Fixed sizes fight layouts.** `setFixedSize` wins over the layout, and `sizeHint` won't shrink below it — use it for buttons and combo boxes only.

## Full example

Tabs, menubar, widgets of each family, and event wiring:

```nasal
var DemoDialog = {
  new: func {
    var m = {
      parents: [DemoDialog],
      window: canvas.Window.new([500, 500], "dialog")
    };
    m.window.setBool("resize", 1);

    m.root = m.window.getCanvas(1)
                    .set("background", canvas.style.getColor("bg_color"))
                    .createGroup();
    m.vbox = canvas.VBoxLayout.new();
    m.window.setLayout(m.vbox);

    m.menubar = canvas.gui.widgets.MenuBar.new(m.root, canvas.style, {});
    m.fileMenu = m.menubar.createMenu("File");
    m.fileMenu.createItem(text: "Quit", cb: func m.window.del(), shortcut: "<Ctrl>+Q");
    m.vbox.addItem(m.menubar);

    m.tabs = gui.widgets.TabWidget.new(m.root, canvas.style, {"tabs-closeable": 1});
    m.vbox.addItem(m.tabs);
    var content = m.tabs.getContent();

    var tab1 = canvas.VBoxLayout.new();
    m.tabs.addTab("tab-1", "Tab 1", tab1);

    tab1.addItem(gui.widgets.Label.new(content, canvas.style, {})
                    .setText("A label")
                    .setBackground("#ffaaaa"));

    tab1.addItem(gui.widgets.CheckBox.new(content, canvas.style, {})
                    .setText("Check me"));

    m.status = gui.widgets.Label.new(content, canvas.style, {})
                    .setText("Selected: none");
    tab1.addItem(m.status);

    m.list = gui.widgets.List.new(content);
    for (var i = 0; i < 30; i += 1) {
      m.list.createItem("Item " ~ i);
    }
    m.list.setSizeHint([m.list._MAX_SIZE, m.list._MAX_SIZE]);
    m.list.listen("selection-changed", func {
      m.status.setText("Selected: " ~
        (string.join(", ", std.map(func(item) item._text, m.list.getSelectedItems())) or "none"));
    });
    tab1.addItem(m.list);

    m.button = gui.widgets.Button.new(content, canvas.style, {})
                    .setText("A button")
                    .setFixedSize(128, 30)
                    .listen("clicked", func {
                      InputDialog.getText("You clicked", "Enter text:", func(button, text) {
                        MessageBox.information("Result",
                          "You entered '" ~ (text != nil ? text : "nothing") ~ "'");
                      });
                    });
    tab1.addItem(m.button);

    var tab2 = canvas.HBoxLayout.new();
    m.tabs.addTab("tab-2", "Tab 2", tab2);
    m.slider = gui.widgets.Slider.new(content, canvas.style, {
                    "max-value": 100,
                    "page-size": 20,
                    "tick-step": 10,
                    "value-style": gui.widgets.Slider.ValueStyle.Moving,
                    "value-position": gui.widgets.Slider.ValuePosition.Above
                  }).setValue(42);
    tab2.addItem(m.slider);

    var hint = m.vbox.sizeHint();
    m.window.setSize(hint);
    return m;
  },

  del: func {
    me.window.del();
  }
};

var demo = DemoDialog.new();
```
