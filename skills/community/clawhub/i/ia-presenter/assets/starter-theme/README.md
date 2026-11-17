# Starter theme

Copy this folder, then:

1. Rename the folder and set `"Name"` in `template.json` (the lowercase name is the
   `template` id used in `info.json`).
2. Rename `starter.css` and update `"Css"`.
3. Edit `presets.json` colors. Remember: `Dark*TextColor` = dark ink for light mode,
   `Light*TextColor` = light ink for dark mode.
4. Optional: add `template.png` (16:9 thumbnail), fonts, background images.
5. Install: `scripts/install_theme.sh ./MyTheme`, relaunch iA Presenter once, select the
   theme in Design → Theme (or `"template": "mytheme"`).

The `Layouts` entry forces the Section layout to dark appearance; the `LayoutExamples`
entry shows up in the layout picker and references `background.jpg` – add such a file or
remove the example.
