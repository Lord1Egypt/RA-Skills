# Openplanet API Documentation

This is the documentation for Openplanet, a plugin and script development platform for Nadeo games like Trackmania and Maniaplanet.

## Table of Contents

### General Information
- Installing Openplanet
- School Mode
- Detecting Openplanet in ManiaScript
- Troubleshooting

### Plugin Development
- Tutorial: Writing plugins (Getting started)
    - Entry point execution
    - Menu options
    - The app object
- NanoVG introduction
- Speeding up the menu music
- Plugin Dependencies
- `info.toml` (plugin configuration)
- Callback functions
- Icons
- Settings
- Script imports
- Preprocessor
- Authentication

### Dependencies
- NadeoServices
- VehicleState
- Camera
- Controls

### API Reference
- Openplanet API
- Trackmania API
- Maniaplanet API
- Turbo API
- Web Services API

---

# Installing Openplanet

Installing Openplanet is straightforward.

1.  **Download and Run:** First, download the latest version of Openplanet and run the installer.

2.  **Select Game Directory:** During the setup, you will be asked to locate the installation path for your game. Make sure you select the exact directory where the game's main executable resides.
    *   **Trackmania (2020):** `Trackmania.exe`
    *   **Maniaplanet:** `ManiaPlanet.exe`
    *   **Trackmania Turbo:** `TrackManiaTurbo.exe`

> **Important:** Openplanet must be installed in the same directory as the game you are running. To double-check the correct location, start the game, open the Task Manager, right-click the game's process, and select "Open file location". Be especially careful if you've installed Trackmania through the Epic Games Store, as it may have created two separate game installations.

### Antivirus & Windows Defender Warnings

It's possible that antivirus software or Windows Defender flags Openplanet. **These are false positives; Openplanet is safe to install and use.**

These warnings typically occur because Openplanet hooks into another process (the game) and its installer is not code-signed (due to the high cost of signing certificates).

**To bypass Windows SmartScreen:**
*   If you see a popup, click on **More info -> Run anyway**.
*   If that button is not available, right-click the installer file in Explorer, click **Properties**, and check the **"Unblock"** box at the bottom.

### Verification

Once installed, simply start your game as normal. You should see a message in the top-left corner: **"Press F3 for Openplanet menu"**.

If the overlay doesn't appear or work, please refer to the [Troubleshooting](#troubleshooting) guide.

---

# School Mode

**School Mode** is a special mode that prevents you from playing online and submitting records to official leaderboards (with some exceptions for whitelisted maps). This allows you to use certain plugins made specifically for practice and training.

## How to Use School Mode

With the Openplanet overlay open (`F3`), navigate to:
`Openplanet -> Signature Mode -> School`

> **Note:** Exiting School Mode will kick you out of any ongoing game. This is necessary because school mode plugins may still affect the game state even after they have been disabled.

## For Plugin Developers

For plugin developers, enabling **Developer Mode** now also implies that **School Mode** is active. Exemptions are granted in specific situations, such as when playing maps in the "Openplanet School" campaign. For more information, refer to the developer-specific documentation on school mode.

## Background

The "School Mode" feature was created to address the debate around "speed drift helper" plugins. While Ubisoft Nadeo's official stance was that visual-only helpers were acceptable, the wider community felt they offered an unfair competitive advantage.

However, these plugins also provide significant value for accessibility and practice. School Mode provides a regulated environment where these tools can be used for training without compromising the integrity of competitive leaderboards. It moves these plugins out of a gray area into a dedicated mode available to everyone.

---

# Detecting Openplanet in ManiaScript

To detect Openplanet in ManiaScript, you check the value of `System.ExtraTool_Info` on the clientside. This will be a string containing "Openplanet" and its version.

Example functions:

```maniascript
#Include "TextLib" as TL

// Returns true if the user has Openplanet installed
Boolean HasOpenplanet() {
  return TL::RegexFind("^Openplanet ", System.ExtraTool_Info, "").count == 1;
}

// Returns the signature mode currently used in Openplanet
Text GetOpenplanetSignatureMode() {
  declare Text[] SignatureMode = TL::RegexMatch(" \\[([A-Z]*)\\]$", System.ExtraTool_Info, "");
  if (SignatureMode.count == 1) {
    return SignatureMode[0];
  }
  return "REGULAR";
}
```


The signature modes available with Openplanet by default are:

*   `OFFICIAL`: Only plugins shipped with Openplanet can run.
*   `REGULAR`: Only signed regular plugins can run.
*   `SCHOOL`: Only signed school mode and regular plugins can run.
*   `DEVMODE`: All signed and unsigned plugins can run.

Competition profiles can also be returned (e.g., `COMPETITION` if the TMWT competition profile is enabled).

The list of signature modes are "tiered," meaning that one signature mode allows its own set of plugins plus anything "above" it in the table below:

| Current / Define | OFFICIAL | REGULAR | SCHOOL | DEVMODE |
| :--------------- | :------- | :------ | :----- | :------ |
| Official         | ✅       | ❌      | ❌     | ❌      |
| Regular          | ✅       | ✅      | ❌     | ❌      |
| School           | ✅       | ✅      | ✅     | ❌      |
| Developer        | ✅       | ✅      | ✅     | ✅      |

> **Note:** This detection works only on the client where Openplanet is running. To check on the server if a client is running Openplanet, you need to send them a Manialink with the detection code and perform a network request/response.

---

# Plugin Development

## Tutorial: Writing plugins (Getting started)

Plugins in Openplanet are written in [Angelscript](https://www.angelcode.com/angelscript/documentation.html). You can find a quick overview [here](https://www.angelcode.com/angelscript/overview.html).

> **Note:** To write your own plugins for Trackmania (2020), you need **Club Edition**. For details, please see [here](URL_TO_CLUB_EDITION_DETAILS).

### Setting everything up

You don't need special tools to write a plugin; any text editor and a tool to create `.zip` files are sufficient. However, using a dedicated code editor like [Visual Studio Code](https://code.visualstudio.com/) or [Sublime Text](https://www.sublimetext.com/) (both offer Angelscript highlighting plugins) and a tool like [7-zip](https://www.7-zip.org/) for archiving can make the process much easier.

Custom Openplanet plugins are saved in:
`C:\Users\<username>\Openplanet<...>\Plugins`

Substitute `<username>` with your Windows username, and `<...>` with the folder specific to your Openplanet version (e.g., `OpenplanetNext`, `Openplanet4`, `OpenplanetTurbo`). Inside the `Plugins` folder, create a new folder for your plugin, for example, `TestPlugin`.

> **Tip:** If you have trouble finding your user plugin folder, you can open it directly from the Openplanet overlay: `Openplanet -> Plugin Manager -> Open Plugin Folder`.

### Enabling Developer Mode

In Openplanet 1.24.4, **Developer Mode** was introduced. By default, it is disabled to prevent unsigned plugins from being loaded. For development, you must enable it as your plugin will only be signed during the upload and review process on the website.

To enable Developer Mode:
1.  Open the Openplanet overlay (`F3`).
2.  Go to `Developer -> Signature Mode`.
3.  Select the **"Developer"** option.

Once selected, the mode is enabled. To disable it, deselect the option and restart the game. Optionally, you can enable developer mode on game startup through the Openplanet settings.

Now that Developer Mode is enabled, you can start working on your plugin.

### Writing the plugin

Modern plugins consist of at least two files:
1.  `info.toml`: A file containing the plugin's metadata (name, author, etc.).
2.  An Angelscript file: Contains the actual code of the plugin.

Let's start with the `info.toml` file, then write the plugin code.

#### `info.toml`

All Openplanet plugins must have a file named `info.toml` at the root of the plugin directory. This file contains meta-information about the plugin.

For a simple plugin, you only need to provide the plugin's name, author, and a category:

```toml
[meta]
name        = "Test Plugin"
author      = "Timmy"
category    = "Testing"
```

For a comprehensive guide on all metadata options, please refer to the [modern plugins guide](URL_TO_MODERN_PLUGINS_GUIDE).

#### Writing code

You need to provide an entry point and an actual code file for your plugin. Create a file named `main.as` in your plugin folder. While script file names within the plugin do not strictly matter, a well-structured plugin makes code easier to manage.

Your `main.as` file will contain the main entry point for any plugin: `void Main()`. This function is called when the plugin is loaded.

```angelscript
void Main()
{
   print("Hello world!");
}
```

The line `print("Hello World!")` will output the message "Hello World!" into the Openplanet log. This helps you verify if your plugin is working when loaded. This simple code is sufficient for now, as the goal is just to get a basic plugin operational. Subsequent chapters of the tutorial will cover more advanced functionalities.

> **Note:** You can write your code across multiple files. Openplanet loads the entire plugin directory as a single script module, effectively merging all code files. Therefore, avoid multiple definitions of elements with the same name, as this can lead to unexpected behavior or compilation errors.

### Entry point execution

Whenever a plugin is started, its `Main()` function is called first. This function is a **coroutine**, meaning it can be suspended (yielded) to return execution control to the game (and other Openplanet plugins). If you are familiar with ManiaScript, the execution flow will seem familiar.

Let's demonstrate this. Ensure you have the Openplanet log open in the overlay (`Openplanet -> Log`). Put this code in your `Main()` function:

```angelscript
void Main()
{
  while (true) {
    print("Hello, world!");
    sleep(1000);
  }
}
```

If you save the file and reload the scripts in Openplanet, you will see "Hello, world!" printed to the log every second.

In this script, an infinite `while (true)` loop is used. Inside the loop, `print("Hello, world!")` outputs a message, and `sleep(1000)` suspends script execution for 1000 milliseconds (1 second).

If you change the `sleep` delay to `0` milliseconds, execution will be returned on the next game frame. A shortcut for this is to simply call `yield()`.

> **Note:** In ManiaScript gamemodes, script execution is fixed at 100 FPS. In Openplanet, all plugins run at the render framerate.

### Menu options

Plugins have the ability to add menu options and display custom windows on the overlay. To start showing menu options, you need to add the `RenderMenu()` function to your plugin:

```angelscript
void RenderMenu()
{
}
```

This function is called every frame to render the menu and cannot be yielded. To show a menu option, use the `UI::MenuItem` function. The UI functions work as an immediate mode GUI, so in this case, `MenuItem` will return `true` or `false` based on whether it was clicked that frame.

You can write the following code to create a simple menu item:

```angelscript
void RenderMenu()
{
  if (UI::MenuItem("My first menu item!")) {
    print("You clicked me!!");
  }
}
```

For more information on what other UI functions there are, see the [UI documentation](URL_TO_UI_DOCUMENTATION).

For information on which specific function declarations will be called by Openplanet, see [plugin functions](URL_TO_PLUGIN_FUNCTIONS).

### The app object

The central brain of ManiaPlanet is the `CGameCtnApp` object and its descendants. From here, you can access most of the game's objects. You can see this object and what it currently contains in the Nod Explorer. The base object is (as of writing this) always `CTrackMania`, regardless of the specific game. However, in case Nadeo ever changes this in the future, Openplanet uses the base class `CGameCtnApp`.

To get this object in your plugin, you use the `CGameCtnApp@ GetApp()` function:

```angelscript
void Main()
{
  CGameCtnApp@ app = GetApp();
}
```

If you need access to a child class (e.g., `CTrackMania` in this case), you have to explicitly cast it, like this:

```angelscript
void Main()
{
  CTrackMania@ app = cast<CTrackMania>(GetApp());
}
```

This works for every Nod object. If the type being cast to is not actually of that type, it will return `null`.

### Testing everything up to now

With your `info.toml` and `main.as` files created, you're ready to test your plugin for the first time!

1.  Start Trackmania.
2.  Open the Openplanet overlay (`F3`).
3.  In the `Developer` menu item, you should now see an option to load a plugin called "Test Plugin" – this is the plugin you just created.

If everything is set up correctly, you should see two new lines in your Openplanet log:
1.  A message indicating that your plugin was loaded.
2.  The "Hello world!" message from your `print` statement.

### Packing the files

Openplanet plugins are distributed as `.op` files, which are essentially renamed `.zip` files. You need to pack your plugin files into a single archive when you're ready to share or publish it.

To create the `.op` file:
1.  Open your plugin's folder (`TestPlugin`) in File Explorer.
2.  Select all files inside the folder (e.g., `info.toml` and `main.as`).
3.  Create a new `.zip` archive from the selected files (e.g., using 7-zip).
    *   Compression is acceptable.
    *   **Do not** set a password.
    *   **Ensure it's a `.zip` file** (e.g., `.rar` files do not work).
4.  Rename the resulting `.zip` file (e.g., `TestPlugin.zip`) to use the `.op` extension (e.g., `TestPlugin.op`).
5.  Place this `.op` file into the main `Plugins` folder (`C:\Users\<username>\Openplanet<...>\Plugins`).

To verify your packed plugin:
1.  Unload the folder-based plugin in the Openplanet overlay (look for the folder icon next to its name).
2.  Now, load the plugin from the newly created archive (look for the box icon next to its name).

If it loads and you see your "Hello world!" message in the log, you've successfully created and packed your first plugin!

### Signatures

Plugins must be "signed" to work outside of Developer Mode. This process happens automatically on the Openplanet website as part of the plugin review. Simply [submit & upload your plugin here](URL_TO_SUBMISSION_PAGE) and wait for it to be reviewed.

---

## NanoVG introduction

The [NanoVG-Library](https://github.com/memononen/nanovg) offers a feature-rich API to scripts to draw various 2D shapes on the screen. This tutorial will introduce you to the API and how to draw shapes. This tutorial assumes you understood the basics of writing a plugin and the basics of Angelscript.

All code examples (and a bit more) are available as a plugin for Openplanet [here](URL_TO_NANOVG_PLUGIN_EXAMPLES). Enable the plugin in the settings and go to the Scripts menu to navigate through the examples.

### Table of Contents (NanoVG)

-   Drawing a Rectangle
-   Drawing a Triangle
-   Colours and Gradients
-   Bézier curves

### Drawing a Rectangle

Let's start simple: our first goal is to draw a red rectangle somewhere on the screen. For this, we use `void nvg::Rect(float x, float y, float w, float h)`. This function specifies a rectangle by its top-left corner (`x` and `y`) and its width (`w`) and height (`h`).

> Keep in mind you give the pixels where the top left corner is, so very large values might be perfectly fine on your 4K screen, but will not be visible on someone with a 720p screen!

Since `nvg::Rect` only specifies the shape, we need to fill it with color using `nvg::FillColor(const vec4&in color)`. The `color` vector consists of red, green, blue, and opacity components, with values ranging between 0 and 1. For a 50% opaque red rectangle, we'll use `vec4(1, 0, 0, 0.5)`.

> **Note:** The `vec4` type is a vector with four components (e.g., `vec4(a, b, c, d)`). `vec2` and `vec3` behave similarly for two or three components. These vectors are used to define colors or screen positions.

Now, we have almost everything to draw our first rectangle. Put this code in your `Render()` function:

```angelscript
void Render() {
    nvg::BeginPath();
    nvg::Rect(100, 100, 300, 150);
    nvg::FillColor(vec4(1, 0, 0, 0.5));
    nvg::Fill();
    nvg::ClosePath();
}
```

-   `nvg::BeginPath();`: Tells the API when your shape or path begins.
-   `nvg::ClosePath();`: Tells the API when your shape or path ends.
-   `nvg::Fill();`: Actually draws the shape onto the screen with the previously specified color.

To add rounded corners, use `void nvg::RoundedRect(float x, float y, float w, float h, float r)`, where `r` is the rounding radius.
Example with rounded corners:
```angelscript
nvg::RoundedRect(100, 100, 300, 150, 10);
```

Other simple shapes:
*   **Circles:** `void nvg::Circle(const vec2&in center, float r)` - defined by center coordinates and radius.
*   **Ellipses:** `void nvg::Ellipse(const vec2&in center, float rx, float ry)` - defined by center and x/y radii.
*   **Rectangles with varying rounded corners:** `void nvg::RoundedRectVarying(float x, float y, float w, float h, float rtl, float rtr, float rbr, float rbl)` - `rtl` (top left), `rtr` (top right), `rbr` (bottom right), `rbl` (bottom left).

> **Note:** If you only want shapes drawn when the Openplanet overlay is open, draw them in the `RenderInterface()` function. The `Render()` function draws onto the screen even if the overlay is closed. More information on plugin functions is available [here](URL_TO_PLUGIN_FUNCTIONS).

### Drawing a Triangle

To draw more complex shapes like triangles or custom polygons, we use **paths**. This works by drawing lines with an imaginary pencil on a canvas.

Key functions:
*   `nvg::MoveTo(vec2(x, y));`: Moves the imaginary pencil to a starting point without drawing.
*   `nvg::LineTo(vec2(a, b));`: Draws a line from the current pencil position to the specified coordinates.

To draw a triangle:
1.  Move to the starting point.
2.  Draw lines to each subsequent corner.
3.  Draw a final line back to the starting point to close the shape.
4.  Fill or stroke the shape.

Example triangle code:

```angelscript
void Render() {
    nvg::BeginPath();

    nvg::MoveTo(vec2(100,100)); // top left corner
    nvg::LineTo(vec2(400,100)); // top right corner: 100 (x) + 300 (w), y remains
    nvg::LineTo(vec2(100,250)); // bottom left corner: x remains, 100 (y) + 150 (h)
    nvg::LineTo(vec2(100,100)); // back to top left

    nvg::FillColor(vec4(1, 0, 1, 0.5)); // Pink color
    nvg::Fill();

    nvg::ClosePath();
}
```

To draw only the outline (stroke) instead of filling:
*   `nvg::StrokeColor(const vec4&in color)`: Specifies the color of the outline.
*   `nvg::StrokeWidth(float size)`: Sets the width of the outline.
*   `nvg::Stroke();`: Draws the outline.

Example of a stroked triangle with no fill:

```angelscript
void Render() {
    nvg::BeginPath();

    nvg::MoveTo(vec2(100,100));
    nvg::LineTo(vec2(400,100));
    nvg::LineTo(vec2(100,250));
    nvg::LineTo(vec2(100,100));

    nvg::StrokeColor(vec4(1, 0.5, 0, 0.5)); // Orange color
    nvg::StrokeWidth(5.5);
    nvg::Stroke();

    nvg::ClosePath();
}
```

If you omit the final `LineTo` command that closes the shape, you'll draw an open path instead of a filled polygon. NanoVG can still fill unclosed paths by drawing a straight line between the path's start and end points.

> **Note:** Convex polygons will always fill and stroke correctly. Concave polygons will work for outlining, but filling them might cause visual artifacts (e.g., filling unintended areas or causing a large square fill). In such cases, split the concave polygon into two or more convex polygons for proper filling.

### Colours and Gradients

Beyond flat colors, NanoVG supports **gradients**. You can choose between linear, box, and radial gradients.

*   **Linear Gradients:** Create a color fade along a straight line between two points (`start` and `end`).
    *   `nvg::Paint nvg::LinearGradient(const vec2&in start, const vec2&in end, const vec4&in color1, const vec4&in color2)`
*   **Box Gradients:** Define a box with an inner circular area. The gradient fades from `color1` (inner) to `color2` (outer) over a specified fade distance (`f`). Outside the fade area, it's `color2`.
    *   `nvg::Paint nvg::BoxGradient(float x, float y, float w, float h, float r, float f, const vec4&in color1, const vec4&in color2)`
*   **Radial Gradients:** Define a gradient based on two radii around a `center` point. `color1` fills the inner circle (`inr`), `color2` fills outside the outer circle (`outr`), and the gradient fades between them.
    *   `nvg::Paint nvg::RadialGradient(const vec2&in center, float inr, float outr, const vec4&in color1, const vec4&in color2)`

Gradients are generated by `xyzGradient` functions, which return a `nvg::Paint` variable. This paint can then be applied to a shape using `nvg::FillPaint(paint)` or `nvg::StrokePaint(paint)`.

Example showing all three gradients on rectangles:

```angelscript
void Render() {
    // Box Gradient
    nvg::BeginPath();
    nvg::Rect(100, 100, 300, 500);
    nvg::FillPaint(nvg::BoxGradient(100, 200, 300, 300, 150, 100, vec4(1,0,0,1), vec4(1, 1, 0, 1))); // Red to Yellow
    nvg::Fill();
    nvg::ClosePath();

    // Linear Gradient
    nvg::BeginPath();
    nvg::Rect(500, 100, 300, 500);
    nvg::FillPaint(nvg::LinearGradient(vec2(500, 100), vec2(500, 600), vec4(1, 0, 0, 1), vec4(1, 1, 0, 1))); // Red to Yellow, top to bottom
    nvg::Fill();
    nvg::ClosePath();

    // Radial Gradient
    nvg::BeginPath();
    nvg::Rect(900, 100, 300, 500);
    nvg::FillPaint(nvg::RadialGradient(vec2(1050, 350), 100, 200, vec4(1, 0, 0, 1), vec4(1, 1, 0, 1))); // Red to Yellow, center outwards
    nvg::Fill();
    nvg::ClosePath();
}
```

> **Note:** If your screen resolution is smaller than 1280 x 720, you might need to adjust the values in this example as it takes up a space of 1200 pixels width and 600 pixels height from the top left.

### Bézier curves

Bézier curves are commonly used in computer graphics to draw smooth, rounded shapes and paths. They consist of a start point, an end point, and one or more control points that define the curve's shape.

*   **Linear Bézier curves:** Have no control points; they are simply a straight line (equivalent to `nvg::LineTo`).
*   **Quadratic Bézier curves:** Have a single control point. The curve is a simple quadratic function that passes through the start and end points, bending towards the control point.
    *   `nvg::QuadTo(const vec2&in c, const vec2&in pos)`: `c` is the control point, `pos` is the end point. The start point is the current cursor position.
*   **Cubic Bézier curves:** Have two control points. They offer more control and smoother transitions than quadratic curves.
    *   `nvg::BezierTo(const vec2&in c1, const vec2&in c2, const vec2&in pos)`: `c1` and `c2` are the two control points, `pos` is the end point.

**Quadratic Bézier Curve Example:**

```angelscript
void Render() {
    nvg::BeginPath();

    // start point: (100, 100)
    nvg::MoveTo(vec2(100, 100));

    // control point: (200, 400), end point: (300, 100)
    nvg::QuadTo(vec2(200, 400), vec2(300, 100));

    nvg::StrokeColor(vec4(1, 0.5, 0, 0.5));
    nvg::StrokeWidth(5.5); nvg::Stroke();

    nvg::ClosePath();
}
```
You can daisy-chain multiple quadratic Bézier curves to create complex shapes. To ensure smooth transitions between curves, the previous curve's control point, the join point (end of previous/start of current), and the current curve's control point should align on a straight line.

**Cubic Bézier Curve Example:**

```angelscript
void Render() {
    nvg::BeginPath();

    nvg::MoveTo(vec2(100, 100));
    nvg::BezierTo(vec2(150, 400), vec2(450, 200), vec2(300, 400)); // First curve

    nvg::StrokeColor(vec4(0, 0.5, 1, 0.5)); // Blue color
    nvg::StrokeWidth(5.5); nvg::Stroke();

    nvg::ClosePath();
}
```

Similar to quadratic curves, cubic Bézier curves can be chained for complex paths. Maintaining collinearity between the end of one curve's control point, the join point, and the start of the next curve's control point is crucial for smoothness.

> **Note:** When filling shapes defined by curves, NanoVG will automatically draw a straight line between the path's end and start points. Concave shapes formed by curves will behave similarly to concave polygons when filled, potentially causing visual artifacts. For proper filling, consider splitting complex concave shapes into simpler convex ones.

---

## Speeding up the menu music

This tutorial demonstrates how to modify game audio properties (specifically, pitch) using an Openplanet plugin, showcasing how to find and manipulate game objects, use settings, and implement callbacks for dynamic updates.

### Finding what we need

Using the [Nod Explorer](https://openplanet.nl/docs/nodexplorer), you can explore the game's internal object hierarchy. For audio, you'll typically find an object named `AudioPort` of type `COalAudioPort`.

Inside `COalAudioPort`, you'll find a list of `Sources`. By inspecting these, you can identify the `CAudioSource` object corresponding to the main menu music (often identifiable by its `PlugSound` property and the underlying `CPlugFileOggVorbis` type). Each `CAudioSource` has a `Pitch` property that controls playback speed.

### Scripting the plugin

1.  **Get the main application object:**
    The game's main application is accessible via `GetApp()`, which returns a `CGameCtnApp` object. While the game's specific type is often `CTrackMania`, casting is not always necessary for basic access.

    ```angelscript
    void Main()
    {
      auto app = GetApp();
    }
    ```

    If a specific child class is needed, you can cast: `CTrackMania@ app = cast<CTrackMania>(GetApp());`

2.  **Access the AudioPort:**
    You can get the `AudioPort` directly:

    ```angelscript
    // Get the AudioPort object
    auto audioPort = GetApp().AudioPort;
    ```

3.  **Find the music source and set pitch:**
    To make the plugin robust to game updates (where the index of the music source might change), iterate through the `audioPort.Sources` list. Identify music files by checking if their `PlugFile` property can be cast to `CPlugFileOggVorbis`.

    ```angelscript
    // Go through all available audio sources
    for (uint i = 0; i < audioPort.Sources.Length; i++) {
      auto source = audioPort.Sources[i];

      // Get the sound that the source can play
      auto sound = source.PlugSound;

      // Check if its file is an .ogg file (assuming music is OGG)
      if (cast<CPlugFileOggVorbis>(sound.PlugFile) is null) {
        // Skip if it's not an ogg file
        continue;
      }

      // Set the pitch of the sound source
      source.Pitch = 1.7f; // Speeds up the music
      // A 'break;' can be added here if you only want to affect the first found music source
    }
    ```

    Reload the scripts in Openplanet (`F3 -> Developer -> Reload Scripts`) to hear the change.

### Slowing it down (Adding a setting)

You can add a plugin setting to control the pitch dynamically. Settings are declared as global variables with the `Setting` metadata option.

```angelscript
[Setting name="Slower music"]
bool Setting_SlowerMusic; // This will appear as a checkbox in Openplanet settings
```

In your code, use this setting to adjust the pitch:

```angelscript
// Set the pitch of the sound source
if (Setting_SlowerMusic) {
  source.Pitch = 0.01f; // Very slow
} else {
  source.Pitch = 1.7f; // Faster
}
```

To make pitch changes apply instantly without reloading scripts, use the `OnSettingsChanged()` callback function.
1.  Move your pitch-changing logic into a separate function (e.g., `UpdatePitch()`).
2.  Call `UpdatePitch()` from both `Main()` and `OnSettingsChanged()`.

```angelscript
void UpdatePitch()
{
  auto audioPort = GetApp().AudioPort;

  for (uint i = 0; i < audioPort.Sources.Length; i++) {
    auto source = audioPort.Sources[i];
    auto sound = source.PlugSound;

    if (cast<CPlugFileOggVorbis>(sound.PlugFile) is null) {
      continue;
    }

    if (Setting_SlowerMusic) {
      source.Pitch = 0.01f;
    } else {
      source.Pitch = 1.7f;
    }
  }
}

void Main()
{
  UpdatePitch();
}

void OnSettingsChanged()
{
  UpdatePitch();
}
```

### We have a bug (Startup race condition)

When restarting the game, the music might not change. This is because the music source might not exist yet when the plugin first loads. To fix this, you can make `UpdatePitch()` return `true` if it successfully changed the pitch, and then have `Main()` loop and `yield()` until the pitch is set.

```angelscript
bool UpdatePitch()
{
  auto audioPort = GetApp().AudioPort;
  bool changed = false; // Track if at least one OGG sound's pitch was changed

  for (uint i = 0; i < audioPort.Sources.Length; i++) {
    auto source = audioPort.Sources[i];
    auto sound = source.PlugSound;

    if (cast<CPlugFileOggVorbis>(sound.PlugFile) is null) {
      continue;
    }

    if (Setting_SlowerMusic) {
      source.Pitch = 0.01f;
    } else {
      source.Pitch = 1.7f;
    }
    changed = true; // Pitch was successfully set for an OGG source
  }
  return changed;
}

void Main()
{
  while (!UpdatePitch()) {
    yield(); // Keep trying until pitch is set
  }
}

void OnSettingsChanged()
{
  UpdatePitch();
}
```

### Extending it to all music

The current solution only pitches currently loaded music. To affect all in-game music, `UpdatePitch()` needs to be called continuously, every frame.

```angelscript
void Main()
{
  while (true) { // Infinite loop
    UpdatePitch();
    yield(); // Yields execution back to the game for the next frame
  }
}
```
> **Note:** This approach can slightly affect FPS, especially if there are many sound sources (500+).
>
> **Challenge:** Consider more efficient ways to update pitch:
> *   Update only on map change (requires waiting a few frames for music to load).
> *   Update only if the number of `Sources` changes.
> *   Update every N frames (e.g., every 2nd or 3rd frame) or every second, instead of every frame.

---

## Plugin Dependencies

As of Openplanet 1.21.0, plugins can depend on other plugins. For a plugin (A) to run if it depends on another plugin (B), both A and B need to be installed. Dependent plugins inherit parts of the implementation of their dependencies by importing their exports. These exported functions (and optionally shared classes) can then be used by any dependent plugins.

For example, the built-in `NadeoServices` plugin allows dependent plugins to use the same access tokens for Nadeo's live services. This saves resources, simplifies development, and avoids potential rate limiting or conflicts.

### Depending on a plugin

If you are a developer and wish to depend on another plugin, add the plugin dependency to your `info.toml` file. For example, to integrate with the `NadeoServices` plugin:

```toml
[script]
dependencies = [ "NadeoServices" ]
```

The string `"NadeoServices"` is the **plugin identifier**. You can find a plugin's identifier by looking at its location: it will either be the folder name (e.g., `C:/Users/Username/OpenplanetNext/Plugins/FooBar/`) or the base file name of an `.op` file (e.g., `C:/Users/Username/OpenplanetNext/Plugins/FooBar.op`).

When your plugin loads, the `Export.as` file (or other specified exports) from `NadeoServices` is compiled into your plugin. It is recommended to check the source of this file, as it often contains documentation on how to use the plugin's exported scripts.

For the `NadeoServices` dependency example, you would then simply call any of the exported functions:

```angelscript
void Main()
{
  NadeoServices::AddAudience("NadeoLiveServices");
  // ...
}
```

### Exporting to other plugins

If you want other plugin developers to be able to depend on your plugin, you have to export script files. There are two ways to do this inside `info.toml`:

*   `exports`: An array of files in your plugin that will be compiled into any dependent plugins, but **NOT** into your own dependency plugin.
*   `shared_exports`: Similar to `exports`, but the files will be compiled into **both** your plugin and the dependent plugins. Shared exports are typically useful for providing classes using Angelscript's [shared entities](https://www.angelcode.com/angelscript/sdk/docs/manual/doc_shared_entities.html).

Example `info.toml` entry for exports:

```toml
[script]
exports = [ "src/Export.as" ]
shared_exports = [ "src/ExportShared.as" ]
```

#### Exporting functions

Function exports use Angelscript's function importing mechanism to create a connection between multiple script modules. This involves exporting a file containing your function definition using the `import ... from "...";` syntax.

For example, if your plugin ID is `Foo`, you could write the following exported script (e.g., `src/Export.as`):

```angelscript
namespace Foo
{
  import void DoSomething() from "Foo"; // "Foo" refers to your plugin's ID
}
```

> **Note:** The exported script is not compiled with your plugin. You must declare the actual function in a separate file (e.g., `src/FooFunctions.as`) that is compiled into your plugin:
> ```angelscript
> namespace Foo
> {
>   void DoSomething()
>   {
>     print("Hello, world!");
>   }
> }
> ```
> If you've worked with header files in C or C++ before, this concept should be familiar. When you change the function signature, ensure you update it in both files!

#### Exporting classes and other entities

If you want to export a class (e.g., via a returned value from an exported function or as a parameter), you have two options:

1.  **Add the class to a regular exported script (`exports`):** The drawback is that you cannot use the same class in your own plugin's code because exported scripts are not compiled into the dependency plugin itself.
2.  **Make the class `shared` and put it in a `shared_exports` script:** This allows you to use (and pass around handles to) the class in both your plugin and dependent plugins.

To make a class shared, simply add the `shared` keyword as described in [Angelscript's shared entities documentation](https://www.angelcode.com/angelscript/sdk/docs/manual/doc_shared_entities.html).

> **Important Rule for Shared Entities:** Shared entities have a restriction: they cannot access non-shared entities because non-shared entities are exclusive to the script module in which they were compiled. If you feel like breaking this restriction, reconsider if a class truly needs to be exported. Often, the problem can be solved purely with exported functions without shared entities.

### Required and optional dependencies

By default, dependencies listed in `dependencies` are **required**. If any required dependency is not installed, your plugin will not compile, and an error will be displayed to the user.

As of Openplanet 1.22.2, you can also specify **optional dependencies** using `optional_dependencies`. This is an additional array of plugin IDs. If an optional dependency is not installed, your plugin will still compile, but without any of the exported files from that specific optional dependency.

If an optional dependency *is* installed, Openplanet will add a preprocessor definition that you can use in your scripts. The definition will have a prefix of `DEPENDENCY_` followed by the plugin ID in uppercase, with spaces, dashes, and periods replaced by underscores.

For example, if you have an optional dependency on `Dashboard` and `Dashboard` is installed, you can check for `DEPENDENCY_DASHBOARD` in your scripts:

```angelscript
#if DEPENDENCY_DASHBOARD
  auto playerState = Dashboard::ViewingPlayerState();
  // ... use Dashboard functions
#else
  warn("Dashboard is not installed!"); // Or provide fallback logic
#endif
```

---

# Troubleshooting

Below are some common issues you might be having, and ways to solve them.

## The game doesn't start

You're likely missing the latest 64-bit version of the Visual Studio C++ runtime. **Do not skip this!** Don't assume you already have this installed on your system! If Openplanet doesn't work, this is very likely the cause. [Download it from here](https://aka.ms/vs/17/release/vc_redist.x64.exe).

Note that if you're trying to get Openplanet for TrackMania Turbo to work, you'll need to install the 32-bit version of the runtime, which you can [download here](https://aka.ms/vs/17/release/vc_redist.x86.exe).

After following the installer's instructions, you might have to restart your PC before it'll work.

## The game works but Openplanet doesn't start/can't be accessed

Almost all issues are caused by the following things - check these first:

*   **Did you start the game in offline mode?** Openplanet requires the game to connect to Ubisoft's servers during startup to check your access level and permissions. Ensure Ubisoft Connect is not in offline mode.
*   **Are you on a laptop and F3 doesn't seem to do anything?** Try pressing `Fn` and `F3` at the same time.
*   **Missing Visual Studio C++ runtime:** As mentioned above, this is the most common cause. Make sure you have the latest 64-bit version installed. [Download it from here](https://aka.ms/vs/17/release/vc_redist.x64.exe).
*   **Restart your computer**, especially right after installing the VS C++ runtime.
*   **Installation directory:** Openplanet needs to be installed in the same directory as the game executable. You can find the game's location by opening the Task Manager, right-clicking `Trackmania.exe`, and selecting "Open file location".

In the rare case that none of those apply to you, other causes can be:
*   Using an older unsupported version of Windows (e.g., Windows 7).
*   Interfering third-party applications like anti-virus, firewalls, or overlays (ReShade, MSI Afterburner, Overwolf, etc.). Try disabling them.
*   A corrupt installation of Openplanet.

### Further troubleshooting

First, check for an `OpenplanetHook.log` file in your Trackmania installation directory. A successful startup looks like this:

```log
[22:35:12] Finding libs path
[22:35:12] Updating PATH to add: 'D:\Games\Trackmania\Openplanet\Lib'
[22:35:12] Attaching DLL to: 'D:\Games\Trackmania\Trackmania.exe'
[22:35:12] Module handle: 00007FF9E2A50000
[22:35:14] DirectInput8Create
```

A failed startup could look like this (e.g., `error 126`):

```log
[22:36:05] Finding libs path
[22:36:05] Updating PATH to add: 'D:\Games\Trackmania\Openplanet\Lib'
[22:36:05] Attaching DLL to: 'D:\Games\Trackmania\Trackmania.exe'
[22:36:05] Failed to load Openplanet module, error 126
[22:36:05] Module handle: 0000000000000000
[22:36:05] DirectInput8Create
[22:36:05] Openplanet.dll is not loaded yet!
[22:36:05] Couldn't find DinputInit function!
```

Next, check your main Openplanet log file located at: `C:\Users\<Your Username>\OpenplanetNext\Openplanet.log` (folder name may vary, e.g., `Openplanet4` or `OpenplanetTurbo`). Look for obvious errors.

You can ask for additional help on the Openplanet Discord.

## Openplanet works on one of my Trackmania installations, but not on the other

If you have multiple Trackmania installations (e.g., Steam and Ubisoft Connect), updating can cause issues.
1.  Start the Trackmania installation where Openplanet doesn't work. An installer should pop up. If not, download the latest version manually.
2.  Follow the installer, but pay close attention to the installation path. Make sure it points to the correct Trackmania directory.
3.  Install the update and restart your game.

## Openplanet starts but plugins can't be installed

This is likely a folder permissions issue. If you see errors like `Unable to load plugin '...' because the zip file doesn't exist!` in your logs:
1.  In Windows Explorer, navigate to `C:\Users`.
2.  Right-click your user's directory and open its `Properties`.
3.  Go to the `Security` tab and ensure your user account has `Full control` over the directory.
4.  Restart Trackmania.

## Temporarily disable Openplanet

You can temporarily disable Openplanet using the following steps:
1.  Start holding down the `Pause/Break` key on your keyboard. Do not release it yet.
2.  Click `Play` in Ubisoft Connect, the Epic Games Launcher, or Steam.
3.  When you see the game itself load (the window has opened), release the `Pause/Break` key.

If you don't have the `Pause/Break` key on your keyboard, you can also rename `dinput8.dll` in your game directory to something else (e.g., `dinput8.dll.bak`).

## Troubleshooting crashes

To troubleshoot crashes, download and install [this registry file](URL_TO_REGISTRY_FILE) to enable writing `.dmp` files for game crashes. After a crash, a `.dmp` file will be created in `C:\Users\Username\AppData\Local\CrashDumps\`.

> **NOTE:** Do not post `.dmp` files publicly! They may contain sensitive information. Only send them to Openplanet developers directly when you are asked to provide one.

## Compatibility

### Linux & Mac Compatibility
For information about compatibility on Linux (e.g., via Wine), check [this page](URL_TO_LINUX_PAGE). The guide for Mac should be similar. With Crossover, ensure you are using DXVK as the rendering engine.

### Game Compatibility
Openplanet is compatible with:
*   Trackmania (2020)
*   ManiaPlanet 4
*   TrackMania Turbo

### Reference: Openplanet-Changelog-API

# Openplanet Changelog

This document lists the changes and updates across different versions of Openplanet.

## [1.29.5] - 2026-04-17 (for Maniaplanet 4)

### Added
*   `Word wrapping` setting to Log window
*   Milliseconds to log output
*   `UI::Drag*` functions
*   `IO::ShareMode` parameter to `IO::File` in order to open files with sharing enabled
*   `UI::VirtualKey::None`
*   `UI::Plot::BeginSubplots` and `UI::Plot::EndSubplots`
*   `Crypto::Sha512`
*   `Meta::OpenplanetVersionGitCommit` and `Meta::OpenplanetVersionGitBranch`
*   Plugin filter to network info window
*   Exclusive allow rule in competition profiles
*   "Show executing plugin in window title" setting in Settings menu (helps debug specific crashes)
*   Support for the standard `/D` flag in installer to specify directory from command line (useful for automated setups)
*   Useful Information to Turbo build

### Updated
*   Angelscript
*   dear imgui

### Changed
*   Changed "N missed" to "N resolved" in pack explorer UI to avoid confusion
*   Changed internal deployment of Openplanet builds to streamline built-in plugin versioning
*   Removed support for some older plugins last updated before January 2022
*   Removed implot demo to save final binary space
*   Removed automatically creating the legacy Scripts folder to avoid confusion for new plugin developers

### Fixed
*   Fixed empty lines not printing to log
*   Fixed 32-bit warning about VC++ runtime in log
*   Fixed `UI::IsGameUIVisible()` on Turbo
*   Fixed not disabling enable checkbox in settings window for essential plugins
*   Fixed not using proper arguments when opening preferred text editor
*   Fixed crash when trying to disable essential plugins
*   Fixed potential crash when typing text into certain textboxes

## [1.29.1] - 2026-01-27 (for Maniaplanet 4)

### Added
*   Horizontal scrollbar to log window
*   Support for printing log lines with newlines

### Updated
*   Angelscript

### Fixed
*   Log window scrolling back to the top on titlebar expansion
*   Scaling on school mode menu


## [1.29.0] - 2026-01-21 (for Maniaplanet 4)

### Added
*   Basic filtering in Nod Explorer
*   Context menus to Nod Explorer members
*   Masking of password fields in Nod Explorer
*   New Display namespace (this deprecates the Draw namespace)
*   `UI::MeasureString` (this deprecates `Draw::MeasureString`)
*   Support for loading webp images
*   "Hide collapse button on windows" setting and `UI::GetDefaultWindowFlags`
*   `UI::SetNextWindowSizeConstraints`, `UI::SetNextWindowCollapsed`, `UI::SetNextWindowBgAlpha`, `UI::IsMouseHoveringRect`, `UI::TableGetHoveredRow`, `UI::TableGetHoveredColumn`
*   A bunch of ImPlot utility functions
*   `enableif` and `onchange` to setting variables
*   Showing overlay when calling `Meta::OpenSettings`
*   Support for printing log lines with newlines
*   Proper error reporting for file IO errors
*   Handling of ImGui user errors as script exceptions
*   Warnings in log for unknown meta tags on functions and variables (eg. typo in "[Setting]" or "[SettingsTab]")
*   `GetCmdBufferCore()` and `GetSystemConfig()`
*   `Dev::ReadUint` alternatives of UInt for consistency
*   Free register parameter to Dev::Hook API
*   License display menu and changed layout of support buttons in About dialog
*   Separate `UNITED_FOREVER` and `NATIONS_FOREVER` preprocessor defines

### Improved
*   Toml parsing

### Updated
*   Angelscript

### Fixed
*   Notifications disappearing at inaccurate times
*   Leaking handles when virtual loader fails to open a file
*   `Time::Now` relying on an uninitialized variable in plugin initializer code
*   "programmer error" in debugger plugin list
*   Enum size for some proc return values
*   Broken logging when printing 2048 characters or more
*   Crash when opening call proc window with global enum
*   Crash that could happen on shutdown

## [1.28.0] - 2025-08-16 (for Maniaplanet 4)

### Added
*   `UI::LoadSystemFont` to load fonts installed in Windows (from `C:\Windows\Fonts`).
*   `UI::PushFont()` with `size` parameter.
*   `UI::PushFontSize()`.
*   `UI::TextAligned()`.
*   `Meta::OpenSettings()` to open the settings window to a plugin's page.
*   Option for FPS counter to Finetuner.
*   New fonts that can be used by plugins: `Montserrat.ttf`, `Montserrat-Bold.ttf`, `Oswald.ttf`, `Oswalf-Bold.ttf`.
*   Ability to set an empty icon for `SettingsTab` using `icon=""`.
*   Parameter documentation for `UI::ShowNotification`.
*   Plugin build duration to verbose build log.
*   Fallback to local appdata directory if needed (instead of `C:\Users\Username\Openplanet\`).
*   Documentation for global and type properties.
*   Option to show plugin setting variable names.
*   New About dialog.

### Deprecated
*   `UI::LoadFont` with ranges and fallback parameters (use the simpler overload instead).

### Improved
*   Table readability on Plugins tab in Settings window.

### Removed
*   UI scale step restriction.

### Updated
*   Dear ImGui with massive font handling improvements:
    *   Overlay scaling setting can now be changed at runtime without requiring a game restart.
    *   Overlay scaling is now completely stable no matter how large you make it.
    *   Fonts are now dynamically resized and rasterized as needed.
    *   Fonts are no longer limited to a single size; they can be changed at runtime.
    *   Font loading is now a very fast operation instead of freezing up the game.
    *   Font ranges are no longer necessary: all characters are loaded.
    *   Font fallbacks are no longer configurable, as they allow virtually every important Unicode character without limitation.
    *   Font fallbacks are now automatically loaded from system fonts: Arial, Meiryo UI for Japanese characters (may not exist on Wine), YaHei UI for Chinese characters (and Japanese characters on Wine).
*   Angelscript, which fixes an issue with shared namespaced classes across different plugin modules.

### Fixed
*   Crash due to exception when trying to create user directory but there are no permissions (OneDrive issue).
*   `Draw::MeasureString` not using current UI font as default font.
*   Missing types in `UI::GetStyleVarX`.
*   Update branch setting on Maniaplanet and Turbo not having any effect on startup.
*   Assertion when passing empty strings to `UI::InputText`.
*   Missing documentation for `UI::SeparatorFlags`.
*   Some issues reported in Finetuner.
*   Crash when solo reloading or unloading a plugin from menu.
*   Crash when unhooking inside of a hook by throwing an exception instead.

## [1.27.12] - 2025-06-16 (for Maniaplanet 4)

### Added
*   The new "Finetuner" plugin, built to replace the popular (now unmaintained) "Tweaker" plugin.
*   Ability to favorite plugins to a separate list in menu.
*   A new UI for the plugins tab in the settings window.
*   A developer menu item to open plugins in preferred editor.
*   Options for the preferred text editor (Sublime Text, Visual Studio Code, or VSCodium).
*   Option to always enable the script compatibility layer (`Compatibility.as`).
*   Ability to use negative indices and lengths in `string::SubStr`.
*   Better error reporting for failing IO operations.
*   A script exception when `Math::clamp` is called with `min > max`.
*   `Net::HttpRequest::StartToFile`.
*   `Net::HttpRequest::Progress*` properties.
*   `Net::HttpRequest::Cancel()`.
*   `awaitable` in favor of the now-deprecated `Meta::PluginCoroutine` (`startnew` now returns `awaitable@`).
*   `Meta::GetPreferredTextEditor` and `Meta::OpenTextEditor`.
*   `Meta::Plugin::Essential`.
*   `Meta::StartWithRunContext` to replace `Meta::PluginCoroutine::WithRunContext`.
*   Ability for plugins to reload themselves using `Meta::ReloadPlugin` by queuing the reload action until the next frame.
*   `string::Repeat`.
*   `UI::Font::Default`, `UI::Font::Default20`, `UI::Font::Default26`, `UI::Font::DefaultBold`, `UI::Font::DefaultMono`.
*   `UI::ColorEditFlags`.
*   More parameters to `UI::InputFloat[234]`.
*   `UI::SetCursorPosX` and `UI::SetCursorPosY`.
*   Missing parameters to `UI::SameLine`.
*   UV coordinates and tint color parameters to `UI::Image`.
*   Displaying of type name in nod explorer for explorer-unimplemented members.
*   `IsSuccess()` and `Error()` to `Auth::PluginAuthTask`.
*   `Dev::Get<T>` and `Dev::Set<T>` as an experimental API.
*   Safe memory functions to Dev API (with significant overhead).
*   `CurrentVec2` and `CurrentInt2` to `MwStack`.
*   `MwId::opEquals`.
*   `Math::Randomizer`.
*   Matrix equal test operators.
*   Missing flags from `UI::InputTextFlags` and added descriptions for each value.
*   `Time::FrameCount`.
*   `Icons::GetAll`.

### Changed
*   Don't allow script timeout to go below 1000 ms (except for the special value 0).
*   Update script engine behavior to disallow empty list elements. For example: `{1,2,3,}` contains 3 elements now instead of 4, the 4th element being the default value (0 here).
*   Updated `Settings.ini` to rename some potentially conflicting options.

### Updated
*   Angelscript.

### Fixed
*   Unnamable entries in hash file report scope.
*   Discarded http requests causing the game to hang.
*   Assertions due to previously unsupported return types in game API.
*   Plugins that are blocked by other plugins unnecessarily loading prematurely.
*   `Fids::Get*Folder` not working with trailing path separator.
*   Broken UI unroll when multiple stylevars or colors are popped and there's a mid-pop issue.
*   Support for `UI::TreeNodeFlags::NoTreePushOnOpen`.
*   `Time::ParseFormatString` not throwing an exception and silently returning 0 on failure.
*   Crash on `Json::Value(null)`.
*   Crash when `ToJson()` is invoked for handles to script objects.
*   Crash that could happen when using multiple setting attributes without values.
*   Crash that could happen when using `Regex::SearchAllResult::opIndex`.

## [1.27.5] - 2025-01-16 (for Maniaplanet 4)

### Added
*   Support for properties in script setting conditionals.
*   `Time::ParseFormatString`.
*   `UI::GetCursorScreenPos` and `UI::SetCursorScreenPos`.
*   `UI::DrawList::AddBezierCubic` and `UI::DrawList::AddBezierQuadratic`.
*   ImGui ID stack debug option shortcut.
*   Type size field to json output documentation.
*   Warning about installing the VC++ redist when showing error 1114 (outdated redist) and 998 (for Linux).

### Updated
*   Angelscript (this adds `foreach`).

### Fixed
*   `uint` script setting not allowing `step` attribute.
*   Script builder not handling metadata correctly when there are scoped namespaces.
*   2 plugins with the same name but different ID not working properly in settings tabs.
*   `TableColumnSortSpecs::SortDirection` property returning invalid values.
*   `Time::ParseRelativeTime` not returning correct results when not using 3 digits after the period.
*   `await()` with single callback never returning.
*   Broken behavior for `iso4` members in Nod Explorer.
*   Rendering invalid escape codes in custom ImGui coloring.
*   Usability issue on Call Proc window.
*   A potential issue with the overlay on Turbo when using Wine (plus some more verbosity in log if this fails).
*   A potential crash when Alt+Tabbing while using fullscreen.
*   Crash when passing invalid timestamp to `Time::FormatString` or `Time::Parse`.
*   Crash when unable to open some files for writing.

## [1.27.2] - 2024-09-16 (for Maniaplanet 4)

### Added
*   New Plugin Manager design (the old design is still available in the settings).
*   Named separators for categories in settings menu.
*   Option for named category separators in Plugins menu.
*   Fid filename to array if it exists in Nod Explorer.
*   New `Path` API's.
*   `if`, `beforerender`, and `afterrender` to `[setting]`.
*   `step` attribute to `[setting]` for `int`, `uint`, `double`, `float`.
*   Support for newlines in `[Setting]`.
*   Improved display of structured settings.
*   First version of new `UI::Plot` API.
*   `UI::SeparatorTextOpenplanet`.
*   `UI::SetItemTooltip`, `UI::SetTooltip`, and `UI::BeginItemTooltip`.
*   `UI::TextLink` and `UI::TextLinkOpenURL`.
*   `UI::Shortcut` and `UI::SetNextItemShortcut`.
*   `UI::IsKeyDown` and `UI::IsKeyReleased`.
*   `UI::PushID` with an integer.
*   `MouseButton` button to `UI::IsItemClicked`.
*   `UI::SetItemKeyOwner`.
*   `UI::WantCaptureMouse` and `UI::WantCaptureKeyboard`.
*   `UI::GetMouseWheelDelta` and `UI::GetMouseWheelDeltaHor`.
*   Support for multiple font range loading in `UI::LoadFont`.
*   `pretty` parameter to `Json::Write` and `Json::ToFile`.
*   `string::LastIndexOf`.
*   `wstring::opCmp`.
*   `Math::PI2`, `Math::PIl`, `Math::PI2l` constants.
*   `Math::Round` with decimal places.
*   `Math::PosInf`, `Math::NegInf`, `Math::PosInfl`, `Math::NegInfl`.
*   `mat3::Transpose` and `mat4::Transpose`.
*   `mat4(const mat3 &in)` and `mat3(const mat4 &in)` constructors.
*   `IO::Copy`.
*   `IO::FileCreatedTime`.
*   More functionality to the `Tests` API's (still a work in progress).
*   `Meta::Plugin::HasManifest`.
*   `Meta::IsSchoolModeWhitelisted`.
*   `Meta::ReloadPlugin`.
*   Support for `Meta::UnloadPlugin` to unload itself.
*   `Reflect::MwClassInfo::Size`.
*   `MwArrayInPlaceDyn<T>`.
*   More descriptive error for plugin `info.toml` load failures.
*   "Open game folder" option to menu.
*   Log level string to log file.
*   Command line flag `/openplanet:developer` to start in developer signature mode.
*   New icons to Openplanet's icon font: Ubisoft, ManiaExchange, ItemExchange, ManiaPark, Evo, TikTok.

### Updated
*   Game version data (faster startup time).
*   Overlay layout and style a little bit.
*   Angelscript.
*   ImGui (this adds many new API's and flag values to the UI API's).

### Deprecated
*   Fallback parameters in `nvg::LoadFont` as they are practically free in NanoVG (fallback fonts are now always included) - this fixes problems when 2 plugins load the same font with different fallback settings.

### Fixed
*   Offzone patch no longer working.
*   Crash when assigning handle in scripts (#525 and #542).
*   Crash when unloaded plugin tries to render in Recent in Developer menu.
*   Shared exports not being included with the plugin when their filename ends with another exported path.
*   `Text::TryParseDouble` having the wrong signature.
*   `Text::StripFormatCodes` not stripping empty links.
*   Hovered flags in `UI::IsItemHovered` not working.
*   `ChildClasses` not showing on Maniaplanet and older in `MwClassInfo`.
*   Counting unnameable files in hash file report statistics.
*   Some broken font loading logic.

## [1.26.14] - 2024-08-16 (for Maniaplanet 4)

### Added
*   Game version data for 2024-02-26 (faster startup time).
*   File search to Pack Explorer.
*   Several missing UI style variables: `DisabledAlpha`, `TabBarBorderSize`, `SeparatorTextBorderSize`, `DockingSeparatorSize`, `SeparatorTextAlign`, `SeparatorTextPadding`.
*   `Meta::Plugin::SignatureLevel`.
*   `Audio::LoadSampleFromAbsolutePath` for more efficient sample loading from absolute paths (like plugin storage folder).
*   Consistent formatting for script sanity check errors.
*   Warning for exported dependencies if they are already a dependency of the current build.

### Fixed
*   Missing settings save when closing settings dialog through menu.
*   Allocating too much memory when loading longer audio files, which could eventually cause the game to crash and/or freeze for a long time.
*   Missing script exception when unable to find audio source.
*   Being able to play streamed samples from more than 1 voice.
*   Crash when removing non-handle objects from game buffers in scripts.
*   Crash when parsing metadata with extraneous whitespace or newlines.
*   `wstring::SubStr` differing in behavior when not providing length parameter.
*   Missing const on iso classes.

### Updated
*   Miniaudio to v0.11.21.
*   Angelscript.

### Reference: OpenPlanet-Global-API

# Openplanet API Documentation

This is the documentation for Openplanet, a plugin and script development platform for Nadeo games like Trackmania and Maniaplanet.

## Table of Contents

### General Information
- Home
- Troubleshooting
- Installing Openplanet
- School Mode

### Plugin Development
- Getting started
- info.toml
- Callback functions
- Icons
- Settings
- Script imports
- Preprocessor
- Authentication

### Dependencies
- NadeoServices
- VehicleState
- Camera
- Controls

### API Reference
- **Openplanet API**
    - Audio
    - Auth
    - Crypto
    - Dev
    - Discord
    - Draw
    - Fids
    - Icons
    - Import
    - Internal
    - IO
    - Json
    - Math
    - Meta
    - Net
    - nvg (NanoVG)
    - Path
    - Permissions
    - Reflection
    - Regex
    - SQLite
    - Settings
    - Text
    - Time
    - XML
    - mat3
    - mat4
    - string
- Trackmania API
- Maniaplanet API
- Turbo API
- Web Services API

---

# API Reference

## Openplanet API

### Audio
Namespace: `Audio`

Playback of sounds.

#### Classes

*   `class Audio::Sample`: Represents an audio sample.
*   `class Audio::Voice`: Represents a currently playing voice of audio.

#### Functions

*   `Audio::Sample@ Audio::LoadSample(const string&in filename, bool streamed = false)`
    *   **Description:** Loads a sound.
    *   **Returns:** `Audio::Sample@`
*   `Audio::Sample@ Audio::LoadSample(MemoryBuffer&in buffer, bool streamed = false)`
    *   **Description:** Loads a sound from a memory buffer.
    *   **Returns:** `Audio::Sample@`
*   `Audio::Sample@ Audio::LoadSampleFromAbsolutePath(const string&in filename, bool streamed = false)`
    *   **Description:** Loads a sound from an absolute path.
    *   **Returns:** `Audio::Sample@`
*   `Audio::Voice@ Audio::Play(Sample@ sample, float gain = 1.0f)`
    *   **Description:** Plays the given sample and returns the voice, immediately starting playback.
    *   **Returns:** `Audio::Voice@`
*   `Voice@ Audio::Start(Sample@ sample)`
    *   **Description:** Starts the given sample and returns the voice, but does not immediately begin playback. Use this if you want to modify voice parameters before the first audio frames play. Note that if you don't let a sample play out, it will leak memory!
    *   **Returns:** `Audio::Voice@`

---

### Auth
Namespace: `Auth`

Third-party API authentication.

#### Classes

*   `class Auth::PluginAuthTask`: An asynchronous authentication task with the Openplanet and Nadeo backends for the current plugin.

#### Functions

*   `Auth::PluginAuthTask@ Auth::GetToken()`
    *   **Description:** Starts a task that authenticates the current user with the Openplanet and Nadeo backends. This is useful to authenticate users with external third-party services securely. Note that you must have authentication enabled in your plugin admin panel for this to work. The resulting token must be sent to your server, which should validate it using the Openplanet.dev API.
    *   **Returns:** `Auth::PluginAuthTask@`

---

### Crypto
Namespace: `Crypto`

Cryptography and hashing routines.

#### Functions

*   `string Crypto::MD5(const string&in str)`
    *   **Description:** Calculate the MD5 hash of the given string.
    *   **Returns:** `string`
*   `string Crypto::Sha1(const string&in str)`
    *   **Description:** Calculate the SHA1 hash of the given string.
    *   **Returns:** `string`
*   `string Crypto::Sha256(const string&in str)`
    *   **Description:** Calculate the SHA256 hash of the given string.
    *   **Returns:** `string`
*   `MemoryBuffer@ Crypto::Random(int length)`
    *   **Description:** Generates cryptographically secure random bytes and returns the buffer.
    *   **Returns:** `MemoryBuffer@`
*   `string Crypto::RandomBase64(int length, bool url = false)`
    *   **Description:** Generates cryptographically secure random bytes and returns its base64 string.
    *   **Returns:** `string`

---

### Dev
Namespace: `Dev`

Advanced memory access.

#### Classes

*   `class Dev::ForceCast`
*   `class Dev::HookInfo`

#### Functions

*   `void Dev::Sleep(uint ms)`
*   `uint64 Dev::BaseAddress()`
    *   **Returns:** `uint64`
*   `uint64 Dev::BaseAddressEnd()`
    *   **Returns:** `uint64`
*   `uint64 Dev::FindPattern(const string&in pattern)`
    *   **Returns:** `uint64`
*   `string Dev::Patch(uint64 ptr, const string&in pattern)`
    *   **Description:** Patches memory at `ptr` with `pattern`.
    *   **Returns:** The original bytes as a backup (`string`).
*   `HookInfo@ Dev::Hook(uint64 ptr, int padding, const string&in func, int pushRegisters = 0)`
    *   **Description:** Hooks directly into game code. You should unhook this manually using `Dev::Unhook()`. The function accepts arbitrarily-ordered parameters named as x86 registers (e.g., `CMwNod@ rcx`).
    *   **Returns:** `Dev::HookInfo@`
*   `void Dev::Unhook(HookInfo@ hook)`
    *   **Description:** Unhooks a registered hook. Do not call this from the function itself.
*   `void Dev::InterceptProc(const string&in className, const string&in procName, ProcIntercept@ func)`
*   `void Dev::InterceptProc(const string&in className, const string&in procName, ProcInterceptEx@ func)`
*   `void Dev::ResetInterceptProc(const string&in className, const string&in procName)`
*   `void Dev::ResetInterceptProc(const string&in className, const string&in procName, ProcIntercept@ func)`
*   `void Dev::ResetInterceptProc(const string&in className, const string&in procName, ProcInterceptEx@ func)`
*   `uint64 Dev::Allocate(uint size, bool executable = false)`
    *   **Returns:** `uint64`
*   `void Dev::Free(uint64 ptr)`
*   `void Dev::DebugBreak()`
*   `string Dev::Read(uint64 ptr, uint64 size)`
    *   **Returns:** `string`
*   `int8 Dev::ReadInt8(uint64 ptr)`
    *   **Returns:** `int8`
*   `int16 Dev::ReadInt16(uint64 ptr)`
    *   **Returns:** `int16`
*   `int Dev::ReadInt32(uint64 ptr)`
    *   **Returns:** `int`
*   `int64 Dev::ReadInt64(uint64 ptr)`
    *   **Returns:** `int64`
*   `uint8 Dev::ReadUInt8(uint64 ptr)`
    *   **Returns:** `uint8`
*   `uint16 Dev::ReadUInt16(uint64 ptr)`
    *   **Returns:** `uint16`
*   `uint Dev::ReadUInt32(uint64 ptr)`
    *   **Returns:** `uint`
*   `uint64 Dev::ReadUInt64(uint64 ptr)`
    *   **Returns:** `uint64`
*   `float Dev::ReadFloat(uint64 ptr)`
    *   **Returns:** `float`
*   `double Dev::ReadDouble(uint64 ptr)`
    *   **Returns:** `double`
*   `vec2 Dev::ReadVec2(uint64 ptr)`
    *   **Returns:** `vec2`
*   `vec3 Dev::ReadVec3(uint64 ptr)`
    *   **Returns:** `vec3`
*   `vec4 Dev::ReadVec4(uint64 ptr)`
    *   **Returns:** `vec4`
*   `int2 Dev::ReadInt2(uint64 ptr)`
    *   **Returns:** `int2`
*   `int3 Dev::ReadInt3(uint64 ptr)`
    *   **Returns:** `int3`
*   `nat2 Dev::ReadNat2(uint64 ptr)`
    *   **Returns:** `nat2`
*   `nat3 Dev::ReadNat3(uint64 ptr)`
    *   **Returns:** `nat3`
*   `iso3 Dev::ReadIso3(uint64 ptr)`
    *   **Returns:** `iso3`
*   `iso4 Dev::ReadIso4(uint64 ptr)`
    *   **Returns:** `iso4`
*   `string Dev::ReadCString(uint64 ptr, uint length)`
    *   **Returns:** `string`
*   `string Dev::ReadCString(uint64 ptr)`
    *   **Returns:** `string`
*   `string Dev::SafeRead(uint64 ptr, uint64 size)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `string`
*   `int8 Dev::SafeReadInt8(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `int8`
*   `int16 Dev::SafeReadInt16(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `int16`
*   `int Dev::SafeReadInt32(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `int`
*   `int64 Dev::SafeReadInt64(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `int64`
*   `uint8 Dev::SafeReadUInt8(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `uint8`
*   `uint16 Dev::SafeReadUInt16(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `uint16`
*   `uint Dev::SafeReadUInt32(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `uint`
*   `uint64 Dev::SafeReadUInt64(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `uint64`
*   `float Dev::SafeReadFloat(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `float`
*   `double Dev::SafeReadDouble(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `double`
*   `vec2 Dev::SafeReadVec2(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `vec2`
*   `vec3 Dev::SafeReadVec3(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `vec3`
*   `vec4 Dev::SafeReadVec4(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `vec4`
*   `int2 Dev::SafeReadInt2(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `int2`
*   `int3 Dev::SafeReadInt3(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `int3`
*   `nat2 Dev::SafeReadNat2(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `nat2`
*   `nat3 Dev::SafeReadNat3(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `nat3`
*   `iso3 Dev::SafeReadIso3(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `iso3`
*   `iso4 Dev::SafeReadIso4(uint64 ptr)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `iso4`
*   `string Dev::SafeReadCString(uint64 ptr, uint length)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
    *   **Returns:** `string`
*   `void Dev::Write(uint64 ptr, const string&in pattern)`
*   `void Dev::Write(uint64 ptr, int8 i)`
*   `void Dev::Write(uint64 ptr, int16 i)`
*   `void Dev::Write(uint64 ptr, int i)`
*   `void Dev::Write(uint64 ptr, int64 i)`
*   `void Dev::Write(uint64 ptr, uint8 i)`
*   `void Dev::Write(uint64 ptr, uint16 i)`
*   `void Dev::Write(uint64 ptr, uint i)`
*   `void Dev::Write(uint64 ptr, uint64 i)`
*   `void Dev::Write(uint64 ptr, float f)`
*   `void Dev::Write(uint64 ptr, double f)`
*   `void Dev::Write(uint64 ptr, const vec2&in v)`
*   `void Dev::Write(uint64 ptr, const vec3&in v)`
*   `void Dev::Write(uint64 ptr, const vec4&in v)`
*   `void Dev::Write(uint64 ptr, const int2&in v)`
*   `void Dev::Write(uint64 ptr, const int3&in v)`
*   `void Dev::Write(uint64 ptr, const nat2&in v)`
*   `void Dev::Write(uint64 ptr, const nat3&in v)`
*   `void Dev::Write(uint64 ptr, const iso3&in v)`
*   `void Dev::Write(uint64 ptr, const iso4&in v)`
*   `void Dev::WriteCString(uint64 ptr, const string&in str)`
*   `void Dev::SafeWrite(uint64 ptr, const string&in pattern)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, int8 i)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, int16 i)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, int i)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, int64 i)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, uint8 i)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, uint16 i)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, uint i)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, uint64 i)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, float f)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, double f)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, const vec2&in v)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, const vec3&in v)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, const vec4&in v)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, const int2&in v)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, const int3&in v)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, const nat2&in v)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, const nat3&in v)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, const iso3&in v)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWrite(uint64 ptr, const iso4&in v)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `void Dev::SafeWriteCString(uint64 ptr, const string&in str)`
    *   **Description:** Safe version of the simpler function. Note that this has significant overhead.
*   `T Get<T>(const ?&in nod, uint offset)`
    *   **Returns:** `T`
*   `int8 Dev::GetOffsetInt8(const ?&in nod, uint offset)`
    *   **Returns:** `int8`
*   `int16 Dev::GetOffsetInt16(const ?&in nod, uint offset)`
    *   **Returns:** `int16`
*   `int Dev::GetOffsetInt32(const ?&in nod, uint offset)`
    *   **Returns:** `int`
*   `int64 Dev::GetOffsetInt64(const ?&in nod, uint offset)`
    *   **Returns:** `int64`
*   `uint8 Dev::GetOffsetUint8(const ?&in nod, uint offset)`
    *   **Returns:** `uint8`
*   `uint16 Dev::GetOffsetUint16(const ?&in nod, uint offset)`
    *   **Returns:** `uint16`
*   `uint Dev::GetOffsetUint32(const ?&in nod, uint offset)`
    *   **Returns:** `uint`
*   `uint64 Dev::GetOffsetUint64(const ?&in nod, uint offset)`
    *   **Returns:** `uint64`
*   `float Dev::GetOffsetFloat(const ?&in nod, uint offset)`
    *   **Returns:** `float`
*   `double Dev::GetOffsetDouble(const ?&in nod, uint offset)`
    *   **Returns:** `double`
*   `vec2 Dev::GetOffsetVec2(const ?&in nod, uint offset)`
    *   **Returns:** `vec2`
*   `vec3 Dev::GetOffsetVec3(const ?&in nod, uint offset)`
    *   **Returns:** `vec3`
*   `vec4 Dev::GetOffsetVec4(const ?&in nod, uint offset)`
    *   **Returns:** `vec4`
*   `int2 Dev::GetOffsetInt2(const ?&in nod, uint offset)`
    *   **Returns:** `int2`
*   `int3 Dev::GetOffsetInt3(const ?&in nod, uint offset)`
    *   **Returns:** `int3`
*   `nat2 Dev::GetOffsetNat2(const ?&in nod, uint offset)`
    *   **Returns:** `nat2`
*   `nat3 Dev::GetOffsetNat3(const ?&in nod, uint offset)`
    *   **Returns:** `nat3`
*   `iso3 Dev::GetOffsetIso3(const ?&in nod, uint offset)`
    *   **Returns:** `iso3`
*   `iso4 Dev::GetOffsetIso4(const ?&in nod, uint offset)`
    *   **Returns:** `iso4`
*   `CMwNod@ Dev::GetOffsetNod(const ?&in nod, uint offset)`
    *   **Returns:** `CMwNod@`
*   `string Dev::GetOffsetString(const ?&in nod, uint offset)`
    *   **Returns:** `string`
*   `void Set<T>(const ?&in nod, uint offset, const T&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const int8&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const int16&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const int&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const int64&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const uint8&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const uint16&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const uint&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const uint64&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const float&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const double&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const vec2&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const vec3&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const vec4&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const int2&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const int3&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const nat2&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const nat3&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const iso3&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const iso4&in v)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, CMwNod@ newNod)`
*   `void Dev::SetOffset(const ?&in nod, uint offset, const string&in str)`

#### Enums

*   `enum Dev::PushRegisters`

#### Function Definitions (`funcdef`)

*   `bool Dev::ProcIntercept(CMwStack&in)`
    *   **Returns:** `bool`
*   `bool Dev::ProcInterceptEx(CMwStack&in, CMwNod@)`
    *   **Returns:** `bool`

---

### Discord
Namespace: `Discord`

Discord rich presence.

#### Classes

*   `class Discord::Status`: A Discord status update.
*   `class Discord::User`: Information about a user.

#### Functions

*   `void Discord::Initialize(const string&in applicationId)`
    *   **Description:** Initialize the Discord RPC API.
*   `void Discord::Shutdown()`
    *   **Description:** Shutdown the Discord RPC API.
*   `bool Discord::IsReady()`
    *   **Description:** Check if the Discord RPC API is ready.
    *   **Returns:** `bool`
*   `User@ Discord::GetUser()`
    *   **Description:** Gets the currently logged in Discord user.
    *   **Returns:** `Discord::User@`
*   `void Discord::SetStatus(const Status&in status)`
    *   **Description:** Sets the current Discord rich presence status.
*   `void Discord::Respond(const string&in userId, Response reply)`
    *   **Description:** Respond to a join request.
*   `string Discord::GetQueuedJoin()`
    *   **Description:** Get the queued up join secret to join.
    *   **Returns:** `string`
*   `string Discord::GetQueuedSpectate()`
    *   **Description:** Get the queued up spectate secret to join.
    *   **Returns:** `string`
*   `int Discord::GetNumJoinRequests()`
    *   **Description:** Get the amount of queued up join requests received.
    *   **Returns:** `int`
*   `User@ Discord::GetQueuedJoinRequest()`
    *   **Description:** Gets the first queued up join request. Returns `null` if there's no more join requests.
    *   **Returns:** `Discord::User@`

#### Enums

*   `enum Discord::Response`: The response code for `Discord::Respond()`.

---

### Draw
Namespace: `Draw`

Limited drawing functions.

#### Functions

*   `int Draw::GetWidth()`
    *   **Description:** Gets the width of the game's resolution.
    *   **Returns:** `int`
*   `int Draw::GetHeight()`
    *   **Description:** Gets the height of the game's resolution.
    *   **Returns:** `int`
*   `vec2 Draw::MeasureString(const string&in str, UI::Font@ font = null, float size = 0.0f, float wrapWidth = 0.0f)`
    *   **Description:** Calculates the size that a string will be drawn at.
    *   **Returns:** `vec2`

---

### Fids
Namespace: `Fids`

Game files and folders.

#### Functions

*   `CSystemFidFile@ Fids::GetResource(const string&in path)`
    *   **Description:** Gets a fid from the Resources drive.
    *   **Returns:** `CSystemFidFile@`
*   `CSystemFidsFolder@ Fids::GetResourceFolder(const string&in path)`
    *   **Description:** Gets a fid container from the Resources drive.
    *   **Returns:** `CSystemFidsFolder@`
*   `CSystemFidFile@ Fids::GetProgramData(const string&in path)`
    *   **Description:** Gets a fid from the ProgramData drive.
    *   **Returns:** `CSystemFidFile@`
*   `CSystemFidsFolder@ Fids::GetProgramDataFolder(const string&in path)`
    *   **Description:** Gets a fid container from the ProgramData drive.
    *   **Returns:** `CSystemFidsFolder@`
*   `CSystemFidFile@ Fids::GetUser(const string&in path)`
    *   **Description:** Gets a fid from the User drive.
    *   **Returns:** `CSystemFidFile@`
*   `CSystemFidsFolder@ Fids::GetUserFolder(const string&in path)`
    *   **Description:** Gets a fid container from the User drive.
    *   **Returns:** `CSystemFidsFolder@`
*   `CSystemFidFile@ Fids::GetGame(const string&in path)`
    *   **Description:** Gets a fid from the Game drive.
    *   **Returns:** `CSystemFidFile@`
*   `CSystemFidsFolder@ Fids::GetGameFolder(const string&in path)`
    *   **Description:** Gets a fid container from the Game drive.
    *   **Returns:** `CSystemFidsFolder@`
*   `CSystemFidFile@ Fids::GetFake(const string&in path)`
    *   **Description:** Gets a fid from the Fake drive.
    *   **Returns:** `CSystemFidFile@`
*   `CSystemFidsFolder@ Fids::GetFakeFolder(const string&in path)`
    *   **Description:** Gets a fid container from the Fake drive.
    *   **Returns:** `CSystemFidsFolder@`
*   `CMwNod@ Fids::Preload(CSystemFidFile@ fid)`
    *   **Description:** Preloads the nod for the fid.
    *   **Returns:** `CMwNod@`
*   `bool Fids::Extract(CSystemFidFile@ fid, bool hookMethod = false)`
    *   **Description:** Extracts the file to disk.
    *   **Returns:** `bool`
*   `string Fids::GetFullPath(CSystemFidFile@ fid)`
    *   **Description:** Gets the full path of the fid.
    *   **Returns:** `string`
*   `void Fids::UpdateTree(CSystemFidsFolder@ fids, bool withFiles = true)`
    *   **Description:** Updates the fid collection tree by rescanning the disk.
*   `CSystemFidFile@ Fids::GetFidsFile(CSystemFidsFolder@ fids, const string&in path)`
    *   **Description:** Get a fid from the given path in the given collection.
    *   **Returns:** `CSystemFidFile@`
*   `CSystemFidsFolder@ Fids::GetFidsFolder(CSystemFidsFolder@ fids, const string&in path)`
    *   **Description:** Get a fid collection from the given path in this collection.
    *   **Returns:** `CSystemFidsFolder@`

---

### Icons
Namespace: `Icons`

Icon helper functions.

#### Functions

*   `dictionary@ Icons::GetAll()`
    *   **Description:** Returns a dictionary containing all available icon string constants.
    *   **Returns:** `dictionary@`

---

### Import
Namespace: `Import`

Loading external functions from DLL's.

#### Classes

*   `class Import::Library`: A library representing a DLL. Instances of Library exist in between multiple plugins, and have to be loaded using `Import::GetLibrary`. When all instances of Library are destroyed, the DLL is freed and unloaded.
*   `class Import::Function`: An imported symbol from a library.
*   `class Import::Ref`: A reference to a script variable.

#### Functions

*   `Library@ Import::GetLibrary(const string&in path)`
    *   **Description:** Gets a library. If it's already loaded, this will return a handle to the already loaded library.
    *   **Returns:** `Import::Library@`

#### Enums

*   `enum Import::CallConvention`: The calling convention to use for this call on 32-bit builds. Convention options don't matter on 64-bit builds.

---

### Internal
Namespace: `Internal`

Functions for built-in plugin use only.

#### Namespaces

*   `namespace Internal::NadeoServices`

---

### IO
Namespace: `IO`

Filesystem input/output.

#### Classes

*   `class IO::File`: Manages a file reading or writing stream.
*   `class IO::FileSource`: Manages a file reading stream from a file source, such as a plugin's zip or folder contents.

#### Functions

*   `string IO::FromStorageFolder(const string&in filename)`
    *   **Description:** Gets the absolute path for a file in your plugin's storage folder. This is typically `C:\Users\Username\OpenplanetNext\PluginStorage\YourPluginIdentifier`. When calling this function and the folder doesn't exist yet, it will automatically be created for you.
    *   **Returns:** `string`
*   `string IO::FromDataFolder(const string&in filename)`
    *   **Description:** Gets the absolute path for a file in the data folder. This is typically `C:\Users\Username\OpenplanetNext`.
    *   **Returns:** `string`
*   `string IO::FromAppFolder(const string&in filename)`
    *   **Description:** Gets the absolute path for a file in the game's application folder. This is where your game is installed, for example `D:\Games\Trackmania`.
    *   **Returns:** `string`
*   `string IO::FromUserGameFolder(const string&in filename)`
    *   **Description:** Gets the absolute path for a file in the game's user folder. This is what the game considers the user folder, for example `C:\Users\Username\Documents\Trackmania`. Note that it is possible for this function to return only the given filename without any absolute path, in case the game doesn't have the necessary info, but you should consider this to happen very rarely (if ever).
    *   **Returns:** `string`
*   `bool IO::FileExists(const string&in filename)`
    *   **Description:** Checks if the given path exists.
    *   **Returns:** `bool`
*   `uint64 IO::FileSize(const string&in filename)`
    *   **Description:** Gets the size of the given file.
    *   **Returns:** `uint64`
*   `int64 IO::FileCreatedTime(const string&in filename)`
    *   **Description:** Gets the created time of the given file.
    *   **Returns:** `int64`
*   `int64 IO::FileModifiedTime(const string&in filename)`
    *   **Description:** Gets the last modified time of the given file.
    *   **Returns:** `int64`
*   `void IO::Delete(const string&in filename)`
    *   **Description:** Deletes the given file.
*   `void IO::Copy(const string&in path, const string&in target)`
    *   **Description:** Copies the given file.
*   `void IO::Move(const string&in path, const string&in target)`
    *   **Description:** Moves the given file or directory.
*   `bool IO::FolderExists(const string&in path)`
    *   **Description:** Checks if the given path exists.
    *   **Returns:** `bool`
*   `void IO::CreateFolder(const string&in path, bool recursive = true)`
    *   **Description:** Creates a folder at the given location.
*   `void IO::DeleteFolder(const string&in path, bool recursive = false)`
    *   **Description:** Deletes the folder at the given location. When `recursive` is `false`, the directory is only deleted if it is empty. Please be careful when setting `recursive` to `true`.
*   `string[]@ IO::IndexFolder(const string&in path, bool recursive)`
    *   **Description:** Lists files and folders in the current folder. If `recursive` is `true`, it will only return files.
    *   **Returns:** `string[]@`
*   `void IO::SetClipboard(const string&in text)`
    *   **Description:** Copies text on the clipboard.

#### Enums

*   `enum IO::FileMode`: The file mode to put the file stream in.

---

### Json
Namespace: `Json`

Json deserialization and serialization.

#### Classes

*   `class Json::Value`: A value in a Json tree. Can be an array, object, or any other value.

#### Functions

*   `Value@ Json::Object()`
    *   **Description:** Create a new Json object value.
    *   **Returns:** `Json::Value@`
*   `Value@ Json::Array()`
    *   **Description:** Create a new Json array value.
    *   **Returns:** `Json::Value@`
*   `Value@ Json::Parse(const string&in json)`
    *   **Description:** Deserializes (parses) a string into a Json value tree.
    *   **Returns:** `Json::Value@`
*   `string Json::Write(const Value@ value, bool pretty = false)`
    *   **Description:** Serializes a Json value tree to a string.
    *   **Returns:** `string`
*   `Value@ Json::FromFile(const string&in filename)`
    *   **Description:** Deserialize (parses) contents of a file into a Json value tree. This can either be a file on disk or a file that's part of the plugin hierarchy.
    *   **Returns:** `Json::Value@`
*   `void Json::ToFile(const string&in filename, const Value@ value, bool pretty = false)`
    *   **Description:** Serializes a Json value tree to a file.

#### Enums

*   `enum Json::Type`: Json value type that a Value might be.

---

### Math
Namespace: `Math`

Math functions and structures.

#### Constants

*   `float Math::PI`: Pi as a float.
*   `float Math::PI2`: Pi multiplied by 2 as a float.
*   `double Math::PIl`: Pi as a double.
*   `double Math::PI2l`: Pi multiplied by 2 as a double.
*   `float Math::PosInf`: Positive infinity as a float.
*   `float Math::NegInf`: Negative infinity as a float.
*   `double Math::PosInfl`: Positive infinity as a double.
*   `double Math::NegInfl`: Negative infinity as a double.

#### Classes

*   `class Math::Randomizer`: A randomizer that can be seeded with a specific seed. The default constructor uses the seed 5489.

#### Functions

*   `int Math::Abs(int i)`
    *   **Returns:** `int`
*   `float Math::Abs(float f)`
    *   **Returns:** `float`
*   `float Math::Sin(float f)`
    *   **Returns:** `float`
*   `float Math::Asin(float f)`
    *   **Returns:** `float`
*   `float Math::Cos(float f)`
    *   **Returns:** `float`
*   `float Math::Acos(float f)`
    *   **Returns:** `float`
*   `float Math::Tan(float f)`
    *   **Returns:** `float`
*   `float Math::Atan(float f)`
    *   **Returns:** `float`
*   `float Math::Atan2(float y, float x)`
    *   **Returns:** `float`
*   `float Math::Exp(float f)`
    *   **Returns:** `float`
*   `float Math::Pow(float x, float y)`
    *   **Returns:** `float`
*   `float Math::Sqrt(float f)`
    *   **Returns:** `float`
*   `float Math::ToDeg(float rad)`
    *   **Returns:** `float`
*   `float Math::ToRad(float deg)`
    *   **Returns:** `float`
*   `float Math::Rand(float min, float max)`
    *   **Description:** Generate a random floating-point value between `min` (inclusive) and `max` (exclusive).
    *   **Returns:** `float`
*   `int Math::Rand(int min, int max)`
    *   **Description:** Generate a random integer between `min` (inclusive) and `max` (exclusive).
    *   **Returns:** `int`
*   `float Math::Log(float f)`
    *   **Returns:** `float`
*   `float Math::Log2(float f)`
    *   **Returns:** `float`
*   `float Math::Log10(float f)`
    *   **Returns:** `float`
*   `float Math::Log1p(float f)`
    *   **Returns:** `float`
*   `float Math::Logb(float f)`
    *   **Returns:** `float`
*   `float Math::Floor(float f)`
    *   **Returns:** `float`
*   `float Math::Ceil(float f)`
    *   **Returns:** `float`
*   `float Math::Round(float f)`
    *   **Returns:** `float`
*   `float Math::Round(float f, int decimals)`
    *   **Returns:** `float`
*   `float Math::InvLerp(const float&in min, const float&in max, const float&in value)`
    *   **Returns:** `float`
*   `float Math::InvLerp(const int&in min, const int&in max, const int&in value)`
    *   **Returns:** `float`
*   `float Math::Lerp(const float&in min, const float&in max, float x)`
    *   **Returns:** `float`
*   `vec2 Math::Lerp(const vec2&in min, const vec2&in max, float x)`
    *   **Returns:** `vec2`
*   `vec3 Math::Lerp(const vec3&in min, const vec3&in max, float x)`
    *   **Returns:** `vec3`
*   `vec4 Math::Lerp(const vec4&in min, const vec4&in max, float x)`
    *   **Returns:** `vec4`
*   `float Math::Distance2(const vec2&in a, const vec2&in b)`
    *   **Returns:** `float`
*   `float Math::Distance2(const vec3&in a, const vec3&in b)`
    *   **Returns:** `float`
*   `float Math::Distance(const vec2&in a, const vec2&in b)`
    *   **Returns:** `float`
*   `float Math::Distance(const vec3&in a, const vec3&in b)`
    *   **Returns:** `float`
*   `float Math::Dot(const vec2&in a, const vec2&in b)`
    *   **Returns:** `float`
*   `float Math::Dot(const vec3&in a, const vec3&in b)`
    *   **Returns:** `float`
*   `float Math::Angle(const vec2&in a, const vec2&in b)`
    *   **Returns:** `float`
*   `float Math::Angle(const vec3&in a, const vec3&in b)`
    *   **Returns:** `float`
*   `vec3 Math::Cross(const vec3&in a, const vec3&in b)`
    *   **Returns:** `vec3`
*   `int Math::Min(int x, int y)`
    *   **Description:** Returns `x` or `y`, whichever is lower.
    *   **Returns:** `int`
*   `float Math::Min(float x, float y)`
    *   **Description:** Returns `x` or `y`, whichever is lower.
    *   **Returns:** `float`
*   `int Math::Max(int x, int y)`
    *   **Description:** Returns `x` or `y`, whichever is higher.
    *   **Returns:** `int`
*   `float Math::Max(float x, float y)`
    *   **Description:** Returns `x` or `y`, whichever is higher.
    *   **Returns:** `float`
*   `int Math::Clamp(int x, int min, int max)`
    *   **Description:** Clamps the value `x` between `min` and `max`. Throws an exception when `min` is higher than `max`.
    *   **Returns:** `int`
*   `float Math::Clamp(float x, float min, float max)`
    *   **Description:** Clamps the value `x` between `min` and `max`. Throws an exception when `min` is higher than `max`.
    *   **Returns:** `float`
*   `bool Math::IsNaN(float)`
    *   **Returns:** `bool`
*   `bool Math::IsInf(float)`
    *   **Returns:** `bool`
*   `uint16 Math::SwapBytes(uint16)`
    *   **Returns:** `uint16`
*   `uint Math::SwapBytes(uint)`
    *   **Returns:** `uint`
*   `uint64 Math::SwapBytes(uint64)`
    *   **Returns:** `uint64`
*   `quat Math::Slerp(const quat&in a, const quat&in b, float x)`
    *   **Returns:** `quat`

---

### Meta
Namespace: `Meta`

Openplanet meta plugin API.

#### Classes

*   `class Meta::PluginSetting`: Information about a plugin's setting.
*   `class Meta::Plugin`: Information about an Openplanet plugin.
*   `class Meta::PluginIndex`: An index of plugin information that can be sorted by its dependency tree.
*   `class Meta::PluginIndexItem`: An item in a `PluginIndex`.
*   `class Meta::UnloadedPluginInfo`

#### Functions

*   `awaitable@ Meta::StartWithRunContext(RunContext runContext, CoroutineFunc@ func)`
    *   **Description:** Starts a new yieldable coroutine from the given function. Function should be a declaration of 'void Func()'.
    *   **Returns:** `awaitable@`
*   `awaitable@ Meta::StartWithRunContext(RunContext runContext, CoroutineFuncUserdata@ func, ref userdata)`
    *   **Description:** Starts a new yieldable coroutine from the given function which also provides a userdata handle parameter. Function should be a declaration of 'void Func(ref@)'.
    *   **Returns:** `awaitable@`
*   `awaitable@ Meta::StartWithRunContext(RunContext runContext, CoroutineFuncUserdataInt64@ func, const int userdata)`
    *   **Description:** Starts a new yieldable coroutine from the given function which also provides a userdata signed integer. Function should be a declaration of 'void Func(int64)'.
    *   **Returns:** `awaitable@`
*   `awaitable@ Meta::StartWithRunContext(RunContext runContext, CoroutineFuncUserdataInt64@ func, const int64 userdata)`
    *   **Description:** Starts a new yieldable coroutine from the given function which also provides a userdata signed integer. Function should be a declaration of 'void Func(int64)'.
    *   **Returns:** `awaitable@`
*   `awaitable@ Meta::StartWithRunContext(RunContext runContext, CoroutineFuncUserdataUint64@ func, const uint userdata)`
    *   **Description:** Starts a new yieldable coroutine from the given function which also provides a userdata unsigned integer. Function should be a declaration of 'void Func(uint64)'.
    *   **Returns:** `awaitable@`
*   `awaitable@ Meta::StartWithRunContext(RunContext runContext, CoroutineFuncUserdataUint64@ func, const uint64 userdata)`
    *   **Description:** Starts a new yieldable coroutine from the given function which also provides a userdata unsigned integer. Function should be a declaration of 'void Func(uint64)'.
    *   **Returns:** `awaitable@`
*   `awaitable@ Meta::StartWithRunContext(RunContext runContext, CoroutineFuncUserdataDouble@ func, const double userdata)`
    *   **Description:** Starts a new yieldable coroutine from the given function which also provides a userdata floating point number. Function should be a declaration of 'void Func(double)'.
    *   **Returns:** `awaitable@`
*   `awaitable@ Meta::StartWithRunContext(RunContext runContext, CoroutineFuncUserdataString@ func, const string&in userdata)`
    *   **Description:** Starts a new yieldable coroutine from the given function which also provides a userdata string. Function should be a declaration of 'void Func(const string &in)'.
    *   **Returns:** `awaitable@`
*   `TextEditorType Meta::GetPreferredTextEditor()`
    *   **Description:** Gets the preferred text editor.
    *   **Returns:** `Meta::TextEditorType`
*   `void Meta::OpenTextEditor(const string&in path, int line = 0)`
    *   **Description:** Opens the preferred text editor with the given path and line number.
*   `Plugin@ Meta::ExecutingPlugin()`
    *   **Description:** Gets the currently executing plugin.
    *   **Returns:** `Meta::Plugin@`
*   `Plugin@[]@ Meta::AllPlugins()`
    *   **Description:** Gets all plugins that are loaded.
    *   **Returns:** `Meta::Plugin@[]@`
*   `UnloadedPluginInfo[]@ Meta::UnloadedPlugins()`
    *   **Description:** Gets the identifiers of all unloaded plugins. Note that this function may be slow!
    *   **Returns:** `Meta::UnloadedPluginInfo[]@`
*   `Plugin@ Meta::GetPluginFromID(const string&in id)`
    *   **Description:** Gets a plugin from its ID.
    *   **Returns:** `Meta::Plugin@`
*   `Plugin@ Meta::GetPluginFromSiteID(int siteID)`
    *   **Description:** Gets a plugin from its site ID, if set.
    *   **Returns:** `Meta::Plugin@`
*   `Plugin@ Meta::LoadPlugin(const string&in path, PluginSource source, PluginType type)`
    *   **Description:** Loads a plugin into memory from the given absolute path and returns a handle to the plugin.
    *   **Returns:** `Meta::Plugin@`
*   `void Meta::UnloadPlugin(Plugin@ plugin)`
    *   **Description:** Queues a plugin to be unloaded from memory completely when it is safe to do so. Note that this will invalidate the plugin object passed in on the next frame! Do not use the Plugin handle after calling this!
*   `void Meta::ReloadPlugin(Plugin@ plugin)`
    *   **Description:** Queues a plugin to be reloaded when it is safe to do so. Note that this will invalidate the plugin object passed in on the next frame! Do not use the Plugin handle after calling this!
*   `void Meta::OpenSettings(Plugin@ plugin = null)`
    *   **Description:** Opens the settings window to the page of the given plugin.
*   `void Meta::SaveSettings()`
    *   **Description:** Forces Openplanet to save its settings immediately. Normally this happens on game shutdown or when the settings window is closed. You should not have to call this function unless you know you really need to!
*   `bool Meta::IsDeveloperMode()`
    *   **Description:** Returns `true` if developer mode is currently enabled.
    *   **Returns:** `bool`
*   `bool Meta::IsSchoolModeWhitelisted()`
    *   **Description:** Returns `true` when the current session is whitelisted by school mode, and school mode is enabled. If you want to check if school mode is enabled, use the `SIG_SCHOOL` preprocessor define instead.
    *   **Returns:** `bool`
*   `string Meta::OpenplanetVersion()`
    *   **Description:** Returns the current version of Openplanet.
    *   **Returns:** `string`
*   `string Meta::OpenplanetVersionDate()`
    *   **Description:** Returns the current date of Openplanet's build.
    *   **Returns:** `string`
*   `string Meta::OpenplanetBuildInfo()`
    *   **Description:** Returns the current build info of Openplanet's build.
    *   **Returns:** `string`
*   `void Meta::LoadOverlayStyle(const string&in path)`
*   `void Meta::ReloadOverlayStyle()`
*   `void Meta::ResetOverlayStyle()`
*   `void Meta::Terminate()`
    *   **Description:** Immediately terminates the game process. This is the same as clicking "Exit" in the Openplanet menu.

#### Enums

*   `enum Meta::TextEditorType`: Type of text editor.
*   `enum Meta::PluginType`: The type of plugin.
*   `enum Meta::PluginSource`: Where this plugin is loaded from.
*   `enum Meta::PluginSettingType`: The type of this setting variable.
*   `enum Meta::RunContext`: Execution context for a coroutine.

---

### Net
Namespace: `Net`

Networking and sockets.

#### Classes

*   `class Net::HttpRequest`: Holds the state of an executing HTTP request.
*   `class Net::Socket`: A non-blocking TCP socket.
*   `class Net::SecureSocket`: Represents a TCP socket with a TLS encryption layer.

#### Functions

*   `HttpRequest@ Net::HttpGet(const string&in url)`
    *   **Description:** Creates an HTTP GET request to the given URL and automatically starts the request.
    *   **Returns:** `Net::HttpRequest@`
*   `HttpRequest@ Net::HttpPost(const string&in url, const string&in data = "", const string&in contentType = "application/x-www-form-urlencoded")`
    *   **Description:** Creates an HTTP POST request to the given URL and automatically starts the request.
    *   **Returns:** `Net::HttpRequest@`
*   `HttpRequest@ Net::HttpHead(const string&in url)`
    *   **Description:** Creates an HTTP HEAD request to the given URL and automatically starts the request.
    *   **Returns:** `Net::HttpRequest@`
*   `HttpRequest@ Net::HttpPut(const string&in url, const string&in data = "", const string&in contentType = "application/x-www-form-urlencoded")`
    *   **Description:** Creates an HTTP PUT request to the given URL and automatically starts the request.
    *   **Returns:** `Net::HttpRequest@`
*   `HttpRequest@ Net::HttpDelete(const string&in url)`
    *   **Description:** Creates an HTTP DELETE request to the given URL and automatically starts the request.
    *   **Returns:** `Net::HttpRequest@`
*   `HttpRequest@ Net::HttpPatch(const string&in url, const string&in data = "", const string&in contentType = "application/x-www-form-urlencoded")`
    *   **Description:** Creates an HTTP PATCH request to the given URL and automatically starts the request.
    *   **Returns:** `Net::HttpRequest@`
*   `string Net::UrlEncode(const string&in str)`
    *   **Description:** URL encode a string.
    *   **Returns:** `string`
*   `string Net::UrlDecode(const string&in str)`
    *   **Description:** URL decode a string.
    *   **Returns:** `string`

#### Enums

*   `enum Net::HttpMethod`

---

### nvg (NanoVG)
Namespace: `nvg`

NanoVG bindings.

#### Classes

*   `class nvg::Texture`: Represents a texture for the NanoVG API.
*   `class nvg::Paint`: A paint style that can be used as a fill or a stroke.

#### Functions

*   `nvg::Texture@ nvg::LoadTexture(const string&in filename, int flags = 0)`
    *   **Description:** Load a texture for the NanoVG API.
    *   **Returns:** `nvg::Texture@`
*   `nvg::Texture@ nvg::LoadTexture(MemoryBuffer&in buffer, int flags = 0)`
    *   **Description:** Load a texture for the NanoVG API from a memory buffer.
    *   **Returns:** `nvg::Texture@`
*   `int nvg::LoadFont(const string&in filename, bool fallbackIcons = false, bool fallbackArial = false)`
    *   **Description:** Load a font for use in the NanoVG API.
    *   **Returns:** `int`
*   `void nvg::Save()`
*   `void nvg::Restore()`
*   `void nvg::Reset()`
*   `void nvg::ShapeAntiAlias(bool enabled)`
*   `void nvg::StrokeColor(const vec4&in color)`
*   `void nvg::StrokePaint(const Paint&in paint)`
*   `void nvg::FillColor(const vec4&in color)`
*   `void nvg::FillPaint(const Paint&in paint)`
*   `void nvg::MiterLimit(float limit)`
*   `void nvg::StrokeWidth(float size)`
*   `void nvg::LineCap(LineCapType cap)`
*   `void nvg::LineJoin(LineCapType join)`
*   `void nvg::GlobalAlpha(float alpha)`
*   `void nvg::ResetTransform()`
*   `void nvg::SetTransform(const mat3&in t)`
*   `mat3 nvg::CurrentTransform()`
    *   **Returns:** `mat3`
*   `void nvg::Transform(const mat3&in t)`
*   `void nvg::Translate(float x, float y)`
*   `void nvg::Translate(const vec2&in)`
*   `void nvg::Rotate(float angle)`
*   `void nvg::SkewX(float angle)`
*   `void nvg::SkewY(float angle)`
*   `void nvg::Scale(float x, float y)`
*   `void nvg::Scale(const vec2&in)`
*   `Paint nvg::LinearGradient(const vec2&in start, const vec2&in end, const vec4&in color1, const vec4&in color2)`
    *   **Returns:** `nvg::Paint`
*   `Paint nvg::BoxGradient(float x, float y, float w, float h, float r, float f, const vec4&in color1, const vec4&in color2)`
    *   **Returns:** `nvg::Paint`
*   `Paint nvg::BoxGradient(const vec2&in pos, const vec2&in size, float r, float f, const vec4&in color1, const vec4&in color2)`
    *   **Returns:** `nvg::Paint`
*   `Paint nvg::RadialGradient(const vec2&in center, float inr, float outr, const vec4&in color1, const vec4&in color2)`
    *   **Returns:** `nvg::Paint`
*   `Paint nvg::TexturePattern(const vec2&in origin, const vec2&in size, float angle, Texture@ texture, float alpha)`
    *   **Returns:** `nvg::Paint`
*   `void nvg::Scissor(float x, float y, float w, float h)`
*   `void nvg::IntersectScissor(float x, float y, float w, float h)`
*   `void nvg::ResetScissor()`
*   `void nvg::AddFallbackFont(int baseFont, int fallbackFont)`
*   `void nvg::FontFace(int font)`
*   `void nvg::FontSize(float size)`
*   `void nvg::FontBlur(float blur)`
*   `void nvg::TextLetterSpacing(float spacing)`
*   `void nvg::TextLineHeight(float lineHeight)`
*   `void nvg::TextAlign(int align)`
*   `float nvg::Text(float x, float y, const string&in str)`
    *   **Description:** Draws text using the current font settings.
    *   **Returns:** `float`
*   `float nvg::Text(const vec2&in pos, const string&in str)`
    *   **Description:** Draws text using the current font settings.
    *   **Returns:** `float`
*   `void nvg::TextBox(float x, float y, float w, const string&in str)`
    *   **Description:** Draws text inside of a word wrapping box using the current font settings.
*   `void nvg::TextBox(const vec2&in pos, float w, const string&in str)`
    *   **Description:** Draws text inside of a word wrapping box using the current font settings.
*   `vec2 nvg::TextBounds(const string&in str)`
    *   **Description:** Measures the size of the given text using the current font settings.
    *   **Returns:** `vec2`
*   `vec2 nvg::TextBoxBounds(float w, const string&in str)`
    *   **Description:** Measures the size of the given text inside of a word wrapping box using the current font settings.
    *   **Returns:** `vec2`
*   `void nvg::BeginPath()`
*   `void nvg::MoveTo(const vec2&in pos)`
*   `void nvg::LineTo(const vec2&in pos)`
*   `void nvg::BezierTo(const vec2&in c1, const vec2&in c2, const vec2&in pos)`
*   `void nvg::QuadTo(const vec2&in c, const vec2&in pos)`
*   `void nvg::ArcTo(const vec2&in pos1, const vec2&in pos2, float radius)`
*   `void nvg::ClosePath()`
*   `void nvg::PathWinding(Winding dir)`
*   `void nvg::Arc(const vec2&in center, float r, float a0, float a1, Winding dir)`
*   `void nvg::Rect(float x, float y, float w, float h)`
*   `void nvg::Rect(const vec2&in pos, const vec2&in size)`
*   `void nvg::RoundedRect(float x, float y, float w, float h, float r)`
*   `void nvg::RoundedRect(const vec2&in pos, const vec2&in size, float r)`
*   `void nvg::RoundedRectVarying(float x, float y, float w, float h, float rtl, float rtr, float rbr, float rbl)`
*   `void nvg::RoundedRectVarying(const vec2&in pos, const vec2&in size, float rtl, float rtr, float rbr, float rbl)`
*   `void nvg::Ellipse(const vec2&in center, float rx, float ry)`
*   `void nvg::Circle(const vec2&in center, float r)`
*   `void nvg::Fill()`
*   `void nvg::Stroke()`

#### Enums

*   `enum nvg::TextureFlags`: Flags to use when loading NanoVG textures.
*   `enum nvg::LineCapType`
*   `enum nvg::Winding`
*   `enum nvg::Align`

---

### Path
Namespace: `Path`

String operations for file paths.

#### Functions

*   `string Path::GetExtension(const string&in path)`
    *   **Description:** Gets the file extension for the given path, including the period. If there is no file extension, this returns an empty string. For example, `hello.txt` will return `.txt`.
    *   **Returns:** `string`
*   `bool Path::HasExtension(const string&in path)`
    *   **Description:** Returns `true` if the given path has a file extension.
    *   **Returns:** `bool`
*   `string Path::ChangeExtension(const string&in path, const string&in extension)`
    *   **Description:** Changes the file extension in the given path and returns the new path. If the original path has no file extension, this will add the given file extension.
    *   **Returns:** `string`
*   `string Path::RemoveExtension(const string&in path)`
    *   **Description:** Removes the file extension from the given path. If there is no file extension, this returns the original path. For example, `hello.txt` will return `hello`.
    *   **Returns:** `string`
*   `string Path::Join(const string&in a, const string&in b)`
    *   **Description:** Combines two paths into one. This automatically glues the paths with forward slashes where needed. For example, passing `hello` and `world` will return `hello/world`, but so will passing `hello/` and `world`. You should not combine multiple absolute paths using this function.
    *   **Returns:** `string`
*   `bool Path::Equals(const string&in a, const string&in b, bool caseSensitive = false)`
    *   **Description:** Returns `true` if the given 2 paths can be considered equal.
    *   **Returns:** `bool`
*   `string Path::GetDirectoryName(const string&in path)`
    *   **Description:** Returns the path to the directory of the containing path, including the path separator, excluding the filename. For example, `hello/world/foo.txt` will return `hello/world/`.
    *   **Returns:** `string`
*   `string Path::GetFileName(const string&in path)`
    *   **Description:** Gets the file name and extension of the given path. For example, `hello/world/foo.txt` will return `foo.txt`.
    *   **Returns:** `string`
*   `string Path::GetFileNameWithoutExtension(const string&in path)`
    *   **Description:** Gets the file name of the given path without the extension. For example, `hello/world/foo.txt` will return `foo`.
    *   **Returns:** `string`
*   `string Path::SanitizeFileName(const string&in name)`
    *   **Description:** Sanitizes the given filename and replaces invalid characters with underscores. You may use this for both file names and folder names.
    *   **Returns:** `string`

---

### Permissions
Namespace: `Permissions`

Trackmania permission checks.

#### Functions

*   `bool Permissions::DisplayClubAds()`
    *   **Description:** User can see ads about Club Edition.
    *   **Returns:** `bool`
*   `bool Permissions::DisplayStandardAds()`
    *   **Description:** User can see ads about Standard Edition.
    *   **Returns:** `bool`
*   `bool Permissions::CanRemoveAds()`
    *   **Description:** User can remove ads.
    *   **Returns:** `bool`
*   `bool Permissions::CreateItemAndMod()`
    *   **Description:** User can create items and mods.
    *   **Returns:** `bool`
*   `bool Permissions::CreateLocalMap()`
    *   **Description:** User can create a map locally.
    *   **Returns:** `bool`
*   `bool Permissions::CreateLocalReplay()`
    *   **Description:** User can save a video in the replay editor.
    *   **Returns:** `bool`
*   `bool Permissions::CreateLocalSkin()`
    *   **Description:** User can create a skin locally.
    *   **Returns:** `bool`
*   `bool Permissions::PlayRecords()`
    *   **Description:** User can play against map's records.
    *   **Returns:** `bool`
*   `bool Permissions::ViewRecords()`
    *   **Description:** User can view the map's records.
    *   **Returns:** `bool`
*   `bool Permissions::ViewPBGhostMultiplayer()`
    *   **Description:** User can view their PB ghost when playing in multiplayer modes.
    *   **Returns:** `bool`
*   `bool Permissions::InGameChat()`
    *   **Description:** User can chat in-game.
    *   **Returns:** `bool`
*   `bool Permissions::OpenAdvancedMapEditor()`
    *   **Description:** User can open the advanced map editor.
    *   **Returns:** `bool`
*   `bool Permissions::OpenReplayEditor()`
    *   **Description:** User can open the replay editor.
    *   **Returns:** `bool`
*   `bool Permissions::OpenSimpleMapEditor()`
    *   **Description:** User can open the simple map editor.
    *   **Returns:** `bool`
*   `bool Permissions::OpenSkinEditor()`
    *   **Description:** User can open the skin editor.
    *   **Returns:** `bool`
*   `bool Permissions::PlayAgainstReplay()`
    *   **Description:** User can play against a replay.
    *   **Returns:** `bool`
*   `bool Permissions::PlayArcadeChannel()`
    *   **Description:** User can play on the arcade channel.
    *   **Returns:** `bool`
*   `bool Permissions::PlayCurrentOfficialMonthlyCampaign()`
    *   **Description:** User can play the current official monthly campaign.
    *   **Returns:** `bool`
*   `bool Permissions::PlayCurrentOfficialQuarterlyCampaign()`
    *   **Description:** User can play the current official quarterly campaign.
    *   **Returns:** `bool`
*   `bool Permissions::PlayHotSeat()`
    *   **Description:** User can play the HotSeat mode.
    *   **Returns:** `bool`
*   `bool Permissions::PlayLocalMap()`
    *   **Description:** User can play a local map.
    *   **Returns:** `bool`
*   `bool Permissions::PlayMatchmaking()`
    *   **Description:** User can play matchmaking.
    *   **Returns:** `bool`
*   `bool Permissions::PlayOnlineCompetition()`
    *   **Description:** User can play online competitions.
    *   **Returns:** `bool`
*   `bool Permissions::PlayPastOfficialMonthlyCampaign()`
    *   **Description:** User can play the past official monthly campaigns.
    *   **Returns:** `bool`
*   `bool Permissions::PlayPastOfficialQuarterlyCampaign()`
    *   **Description:** User can play the past official quarterly campaigns.
    *   **Returns:** `bool`
*   `bool Permissions::PlayPublicClubCampaign()`
    *   **Description:** User can play public club campaigns.
    *   **Returns:** `bool`
*   `bool Permissions::PlayPublicClubRoom()`
    *   **Description:** User can play on the public club rooms.
    *   **Returns:** `bool`
*   `bool Permissions::PlaySplitscreen()`
    *   **Description:** User can play the splitscreen mode.
    *   **Returns:** `bool`
*   `bool Permissions::PlayTOTDChannel()`
    *   **Description:** User can play the TOTD channel and COTD.
    *   **Returns:** `bool`
*   `bool Permissions::CreateClub()`
    *   **Description:** User can create a club.
    *   **Returns:** `bool`
*   `bool Permissions::CreateActivity()`
    *   **Description:** User can create a club activity.
    *   **Returns:** `bool`
*   `bool Permissions::CreateClubCompetition()`
    *   **Description:** User can create a competition in a club.
    *   **Returns:** `bool`
*   `bool Permissions::ViewClub()`
    *   **Description:** User can display a club page.
    *   **Returns:** `bool`
*   `bool Permissions::JoinClub()`
    *   **Description:** User can join a club.
    *   **Returns:** `bool`
*   `bool Permissions::PlayPrivateActivity()`
    *   **Description:** User can play a private club activity.
    *   **Returns:** `bool`
*   `bool Permissions::UseCustomCollection()`
    *   **Description:** User can use a custom item collection.
    *   **Returns:** `bool`
*   `bool Permissions::AccessServerReview()`
    *   **Description:** User can access the server review.
    *   **Returns:** `bool`
*   `bool Permissions::CreateAndUploadMap()`
    *   **Description:** User can upload a map to server review.
    *   **Returns:** `bool`
*   `bool Permissions::CreateGameMode()`
    *   **Description:** User can create game modes.
    *   **Returns:** `bool`
*   `bool Permissions::CreateLocalServer()`
    *   **Description:** User can create a local server.
    *   **Returns:** `bool`
*   `bool Permissions::FindLocalServer()`
    *   **Description:** User can find a local server.
    *   **Returns:** `bool`
*   `bool Permissions::CreateAndUploadSkin()`
    *   **Description:** User can save a skin (upload).
    *   **Returns:** `bool`
*   `bool Permissions::UseCustomSkin()`
    *   **Description:** User can use a custom skin.
    *   **Returns:** `bool`
*   `bool Permissions::CanSubscribeToClub()`
    *   **Description:** User can upgrade their game to the Club Edition.
    *   **Returns:** `bool`
*   `bool Permissions::CanSubscribeToStandard()`
    *   **Description:** User can upgrade their game to the Standard Edition.
    *   **Returns:** `bool`
*   `bool Permissions::GainXP()`
    *   **Description:** User can play to gain experience points.
    *   **Returns:** `bool`

---

### Reflection
Namespace: `Reflection`

Info about game classes and members.

#### Classes

*   `class Reflection::MwMemberInfo`: Information about a type's member.
*   `class Reflection::MwClassInfo`: Information about a type.

#### Functions

*   `const MwClassInfo@ Reflection::GetType(const string&in name)`
    *   **Description:** Get the type info of the given name.
    *   **Returns:** `const Reflection::MwClassInfo@`
*   `const MwClassInfo@ Reflection::GetType(uint id)`
    *   **Description:** Get the type info of the given ID.
    *   **Returns:** `const Reflection::MwClassInfo@`
*   `const MwClassInfo@ Reflection::TypeOf(CMwNod@ nod)`
    *   **Description:** Get the type info of the given nod.
    *   **Returns:** `const Reflection::MwClassInfo@`
*   `int Reflection::GetRefCount(CMwNod@ nod)`
    *   **Description:** Get the reference count of the given nod.
    *   **Returns:** `int`

---

### Regex
Namespace: `Regex`

Regular expressions.

#### Classes

*   `class Regex::SearchAllResult`: Result of a call to `Regex::SearchAll`.

#### Functions

*   `string Regex::Replace(const string&in source, const string&in pattern, const string&in replace, int flags = Regex::Flags::ECMAScript)`
    *   **Description:** Perform a regex search and replace on the given string.
    *   **Returns:** `string`
*   `bool Regex::IsMatch(const string&in source, const string&in pattern, int flags = Regex::Flags::ECMAScript)`
    *   **Description:** Perform a regex match on the source string and returns `true` if it matches.
    *   **Returns:** `bool`
*   `bool Regex::Contains(const string&in source, const string&in pattern, int flags = Regex::Flags::ECMAScript)`
    *   **Description:** Perform a regex match on the source string and returns `true` if it contains the pattern.
    *   **Returns:** `bool`
*   `string[]@ Regex::Match(const string&in source, const string&in pattern, int flags = Regex::Flags::ECMAScript)`
    *   **Description:** Performs a regex match on the source string and returns the matched groups if it matches, or an empty array if it doesn't.
    *   **Returns:** `string[]@`
*   `string[]@ Regex::Search(const string&in source, const string&in pattern, int flags = Regex::Flags::ECMAScript)`
    *   **Description:** Searches for a regex match on the source string and returns the matched groups if it matches, or an empty array if it doesn't.
    *   **Returns:** `string[]@`
*   `SearchAllResult@ Regex::SearchAll(const string&in source, const string&in pattern, int flags = Regex::Flags::ECMAScript)`
    *   **Description:** Searches for a regex match on the source string and returns all the matches.
    *   **Returns:** `Regex::SearchAllResult@`

#### Enums

*   `enum Regex::Flags`: Flags that can be passed to regular expression functions.

---

### Settings
Namespace: `Settings`

Openplanet's settings.

#### Classes

*   `class Settings::Section`: Represents a section in the settings file.

---

### SQLite
Namespace: `SQLite`

SQLite database access.

#### Classes

*   `class SQLite::Statement`: A prepared SQLite statement and result set. Note that SQLite statements can be relatively IO-heavy depending on its use. Refer to the SQLite documentation for more information.
*   `class SQLite::Database`: An SQLite database.

---

### Text
Namespace: `Text`

Text parsing and formatting.

#### Functions

*   `int Text::ParseInt(const string&in str, int base = 10)`
    *   **Description:** Parses the given string as an integer.
    *   **Returns:** `int`
*   `int64 Text::ParseInt64(const string&in str, int base = 10)`
    *   **Description:** Parses the given string as a 64-bit integer.
    *   **Returns:** `int64`
*   `uint Text::ParseUInt(const string&in str, int base = 10)`
    *   **Description:** Parses the given string as an unsigned integer.
    *   **Returns:** `uint`
*   `uint64 Text::ParseUInt64(const string&in str, int base = 10)`
    *   **Description:** Parses the given string as a 64-bit unsigned integer.
    *   **Returns:** `uint64`
*   `float Text::ParseFloat(const string&in str)`
    *   **Description:** Parses the given string as a float.
    *   **Returns:** `float`
*   `double Text::ParseDouble(const string&in str)`
    *   **Description:** Parses the given string as a double.
    *   **Returns:** `double`
*   `vec4 Text::ParseHexColor(string str)`
    *   **Description:** Parses the given string as a hexadecimal color such as "#FF0000".
    *   **Returns:** `vec4`
*   `bool Text::TryParseInt(const string&in str, int&out, int base = 10)`
    *   **Description:** Tries to parse the given string as an integer. This will return `true` only if the string was parsed entirely and was not empty.
    *   **Returns:** `bool`
*   `bool Text::TryParseInt64(const string&in str, int64&out, int base = 10)`
    *   **Description:** Tries to parse the given string as a 64-bit integer. This will return `true` only if the string was parsed entirely and was not empty.
    *   **Returns:** `bool`
*   `bool Text::TryParseUInt(const string&in str, int&out, int base = 10)`
    *   **Description:** Tries to parse the given string as an unsigned integer. This will return `true` only if the string was parsed entirely and was not empty.
    *   **Returns:** `bool`
*   `bool Text::TryParseUInt64(const string&in str, int64&out, int base = 10)`
    *   **Description:** Tries to parse the given string as a 64-bit unsigned integer. This will return `true` only if the string was parsed entirely and was not empty.
    *   **Returns:** `bool`
*   `bool Text::TryParseFloat(const string&in str, float&out)`
    *   **Description:** Parses the given string as a float. This will return `true` only if the string was parsed entirely and was not empty.
    *   **Returns:** `bool`
*   `bool Text::TryParseDouble(const string&in str, double&out)`
    *   **Description:** Parses the given string as a double. This will return `true` only if the string was parsed entirely and was not empty.
    *   **Returns:** `bool`
*   `bool Text::TryParseHexColor(string str, vec4&out)`
    *   **Description:** Parses the given string as a hexadecimal color such as "#FF0000". This will return `true` only if the string was parsed entirely and was not empty.
    *   **Returns:** `bool`
*   `string Text::Format(const string&in format, int8)`
    *   **Returns:** `string`
*   `string Text::Format(const string&in format, int16)`
    *   **Returns:** `string`
*   `string Text::Format(const string&in format, int)`
    *   **Returns:** `string`
*   `string Text::Format(const string&in format, int64)`
    *   **Returns:** `string`
*   `string Text::Format(const string&in format, uint8)`
    *   **Returns:** `string`
*   `string Text::Format(const string&in format, uint16)`
    *   **Returns:** `string`
*   `string Text::Format(const string&in format, uint)`
    *   **Returns:** `string`
*   `string Text::Format(const string&in format, uint64)`
    *   **Returns:** `string`
*   `string Text::Format(const string&in format, float)`
    *   **Returns:** `string`
*   `string Text::Format(const string&in format, double)`
    *   **Returns:** `string`
*   `string Text::FormatPointer(uint64 ptr)`
    *   **Description:** Formats a pointer to its more representative hexadecimal format, for example: `0x12345678`.
    *   **Returns:** `string`
*   `string Text::FormatGameColor(const vec3&in rgb)`
    *   **Description:** Formats a color in Maniaplanet-style color formatting, for example: `$f00`.
    *   **Returns:** `string`
*   `string Text::FormatOpenplanetColor(const vec3&in rgb)`
    *   **Description:** Formats a color in Openplanet-style UI color formatting, for example: `\$f00`.
    *   **Returns:** `string`
*   `string Text::StripFormatCodes(const string&in s)`
    *   **Description:** Strips all Maniaplanet-style formatting codes from a string.
    *   **Returns:** `string`
*   `string Text::StripNonColorFormatCodes(const string&in s)`
    *   **Description:** Strips all non-color Maniaplanet-style formatting codes from a string.
    *   **Returns:** `string`
*   `string Text::OpenplanetFormatCodes(const string&in s)`
    *   **Description:** Takes a string, converts Maniaplanet-style formatting codes and turns them into Openplanet UI formatting codes. This will also get rid of all Openplanet-unsupported formatting codes.
    *   **Returns:** `string`
*   `string Text::StripOpenplanetFormatCodes(const string&in s)`
    *   **Description:** Strips all Openplanet-supported formatting codes from a string.
    *   **Returns:** `string`
*   `string Text::EncodeHex(const string&in, bool upper = false)`
    *   **Description:** Encodes a string so that all characters are encoded as a sequence of hexadecimal bytes. Note that if you want to encode binary data, you should probably use `MemoryBuffer::ReadToHex` instead.
    *   **Returns:** `string`
*   `string Text::DecodeHex(const string&in)`
    *   **Description:** Decodes a string where characters are encoded as a sequence of hexadecimal bytes. Note that if you want to decode binary data, you should probably use `MemoryBuffer::WriteFromHex` instead.
    *   **Returns:** `string`
*   `string Text::EncodeBase64(const string&in, bool url = false)`
    *   **Description:** Encode a string as a base64 encoded string. Note that if you want to encode binary data, you should probably use `MemoryBuffer::ReadToBase64` instead.
    *   **Returns:** `string`
*   `string Text::DecodeBase64(const string&in, bool url = false)`
    *   **Description:** Decode a base64 encoded string to a string. Note that if you want to decode binary data, you should probably use `MemoryBuffer::WriteFromBase64` instead.
    *   **Returns:** `string`

---

### Time
Namespace: `Time`

Date and time.

#### Classes

*   `class Time::Info`: Information about a specific timestamp, simplified into its common components.

#### Properties

*   `uint64 Time::Now`
    *   **Description:** Gets the time (in milliseconds) since the game started.
    *   **Returns:** `uint64`
*   `int64 Time::Stamp`
    *   **Description:** Gets the current machine timestamp in seconds. Also commonly referred to as epoch time.
    *   **Returns:** `int64`
*   `uint64 Time::FrameCount`
    *   **Description:** Gets the number of frames that Openplanet has processed. Note that this is not the same as the game's own frame counter; it may be off by a number of frames.
    *   **Returns:** `uint64`

#### Functions

*   `string Time::FormatString(const string&in format, int64 stamp = -1)`
    *   **Description:** Format a time into the given format as specified by `strftime` in the local time.
    *   **Returns:** `string`
*   `string Time::FormatStringUTC(const string&in format, int64 stamp = -1)`
    *   **Description:** Format a time into the given format as specified by `strftime` in UTC.
    *   **Returns:** `string`
*   `int64 Time::ParseFormatString(const string&in format, const string&in stamp)`
    *   **Description:** Parses a time from a string into a timestamp.
    *   **Returns:** `int64`
*   `string Time::Format(uint64 time, bool fractions = true, bool forceMinutes = true, bool forceHours = false, bool short = false)`
    *   **Description:** Format a game time (in milliseconds) to its race time representation. For example, `61234` will be `"1:01.234"`.
    *   **Returns:** `string`
*   `string Time::Format(int64 time, bool fractions = true, bool forceMinutes = true, bool forceHours = false, bool short = false)`
    *   **Description:** Format a game time (in milliseconds) to its race time representation. For example, `61234` will be `"1:01.234"`.
    *   **Returns:** `string`
*   `uint64 Time::ParseRelativeTime(const string&in time)`
    *   **Description:** Parses a relative game time from its race time representation.
    *   **Returns:** `uint64`
*   `Info Time::Parse(int64 stamp = -1)`
    *   **Description:** Parses a time into a structure containing individual time components in the local time.
    *   **Returns:** `Time::Info`
*   `Info Time::ParseUTC(int64 stamp = -1)`
    *   **Description:** Parses a time into a structure containing individual time components in UTC.
    *   **Returns:** `Time::Info`

---

### Tests
Namespace: `Tests`

Testing suite utilities.

#### Classes

*   `class Tests::Context`: Context passed to test functions. Do not keep references to this context as they will be invalidated directly after the test function returns.

---

### XML
Namespace: `XML`

XML deserialization.

#### Classes

*   `class XML::Node`: A node within an XML tree.
*   `class XML::Document`: An XML tree document.

---

### mat3
Namespace: `mat3`

Static functions for the `mat3` class.

#### Functions

*   `mat3 mat3::Identity()`
    *   **Returns:** `mat3`
*   `mat3 mat3::Translate(const vec2&in v)`
    *   **Returns:** `mat3`
*   `mat3 mat3::Rotate(float angle)`
    *   **Returns:** `mat3`
*   `mat3 mat3::Scale(const vec2&in scale)`
    *   **Returns:** `mat3`
*   `mat3 mat3::Scale(float scale)`
    *   **Returns:** `mat3`
*   `mat3 mat3::Inverse(const mat3&in)`
    *   **Returns:** `mat3`
*   `mat3 mat3::Transpose(const mat3&in)`
    *   **Returns:** `mat3`

---

### mat4
Namespace: `mat4`

Static functions for the `mat4` class.

#### Functions

*   `mat4 mat4::Identity()`
    *   **Returns:** `mat4`
*   `mat4 mat4::Translate(const vec3&in v)`
    *   **Returns:** `mat4`
*   `mat4 mat4::Rotate(float angle, const vec3&in dir)`
    *   **Returns:** `mat4`
*   `mat4 mat4::Scale(const vec3&in scale)`
    *   **Returns:** `mat4`
*   `mat4 mat4::Scale(float scale)`
    *   **Returns:** `mat4`
*   `mat4 mat4::Perspective(float yFov, float aspect, float nearZ, float farZ)`
    *   **Returns:** `mat4`
*   `mat4 mat4::Inverse(const mat4&in)`
    *   **Returns:** `mat4`
*   `mat4 mat4::LookAt(const vec3&in eye, const vec3&in center, const vec3&in up)`
    *   **Returns:** `mat4`
*   `mat4 mat4::Transpose(const mat4&in)`
    *   **Returns:** `mat4`

---

### string
Namespace: `string`

Static functions for the `string` class.

#### Functions

*   `string string::Join(const string[]&in arr, const string&in delimiter)`
    *   **Description:** Join an array of strings into a single where each item is separated using the given delimiter.
    *   **Returns:** `string`
*   `string string::Repeat(const string&in str, int count)`
    *   **Description:** Repeats a the given string `count` times.
    *   **Returns:** `string`

### Reference: Openplanet-Starter-API

# Openplanet API Documentation

This is the documentation for Openplanet, a plugin and script development platform for Nadeo games like Trackmania and Maniaplanet.

## Table of Contents

### General Information
- Home
- Troubleshooting
- Installing Openplanet
- School Mode
- Detecting Openplanet in ManiaScript
- Temporarily disable Openplanet

### Plugin Development
- Getting started
- Callback functions
- `info.toml`
- Icons
- Settings
- **Script imports**
- **Preprocessor**
- Authentication
- Plugin Dependencies

### Dependencies
- NadeoServices
- VehicleState
- Camera
- Controls

### API Reference
- Openplanet API
- Trackmania API
- Maniaplanet API
- Turbo API
- Web Services API

---

# Plugin Development

## Callback functions

These are the functions that will be called for each plugin, if the plugin exists.

| Function Signature                     | Description                                                                                                                                              | Yieldable |
| :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------- |
| `void Main()`                          | Main entry point.                                                                                                                                        | Yes       |
| `void Render()`                        | Render function called every frame (always, even if overlay is closed).                                                                                    | No        |
| `void RenderInterface()`               | Render function called every frame intended for UI when the Openplanet overlay is active.                                                                | No        |
| `void RenderMenu()`                    | Render function called every frame intended only for menu items in UI.                                                                                     | No        |
| `void RenderMenuMain()`                | Render function called every frame intended only for menu items in the main menu of the UI.                                                              | No        |
| `void RenderSettings()`                | **Deprecated:** Use `[SettingsTab]` instead! Render function called every frame intended for within Openplanet's settings window for UI.                 | No        |
| `void Update(float dt)`                | Called every frame. `dt` is the delta time (milliseconds since last frame).                                                                              | No        |
| `void OnDisabled()`                    | Called when the plugin is disabled from the settings, the menu, or programmatically via the Meta API.                                                    | No        |
| `void OnEnabled()`                     | Called when the plugin is enabled from the settings, the menu, or programmatically via the Meta API.                                                     | No        |
| `void OnDestroyed()`                   | Called when the plugin is unloaded and completely removed from memory.                                                                                   | No        |
| `void OnSettingsChanged()`             | Called when a setting in the settings panel was changed.                                                                                                 | No        |
| `void OnSettingsSave(Settings::Section& section)` | Called when the settings for the plugin are being saved.                                                                                 | No        |
| `void OnSettingsLoad(Settings::Section& section)` | Called when the settings for the plugin are being loaded.                                                                                | No        |
| `void OnKeyPress(bool down, VirtualKey key)` | Called whenever a key is pressed on the keyboard. See documentation for `VirtualKey` enum.                                                         | No        |
| `UI::InputBlocking OnKeyPress(bool down, VirtualKey key)` | (Alternative signature) Called whenever a key is pressed. Can block input.                                                               | No        |
| `void OnMouseButton(bool down, int button, int x, int y)` | Called whenever a mouse button is pressed. `x` and `y` are the viewport coordinates.                                                     | No        |
| `UI::InputBlocking OnMouseButton(bool down, int button, int x, int y)` | (Alternative signature) Called whenever a mouse button is pressed. Can block input. `x` and `y` are viewport coordinates. | No        |
| `void OnMouseMove(int x, int y)`       | Called whenever the mouse moves. `x` and `y` are the viewport coordinates.                                                                               | No        |
| `void OnMouseWheel(int x, int y)`      | Called whenever the mouse wheel is scrolled. `x` and `y` are the scroll delta values.                                                                    | No        |
| `UI::InputBlocking OnMouseWheel(int x, int y)` | (Alternative signature) Called whenever the mouse wheel is scrolled. Can block input. `x` and `y` are scroll delta values.                       | No        |
| `void OnLoadCallback(CMwNod@ nod)`     | Called when a Nod is loaded from a file. Requires `RegisterLoadCallback` first. Meant for early callbacks. Avoid if not strictly necessary.              | No        |

---

## `info.toml` reference

The `info.toml` file specifies important metadata for a plugin. It has a number of possible options you can set. The format of this file is [TOML](https://toml.io/en/latest).

### Meta table

The required `[meta]` table contains basic metadata information about the plugin.

| Key       | Type      | Required    | Description                                                                                                                                                                                                                                 |
| :-------- | :-------- | :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `version` | String    | Yes         | The version of the plugin. Defaults to `1.0` if not provided, but is required for successful submission on the website.                                                                                                                   |
| `name`    | String    | Recommended | The name of the plugin. When not provided, this defaults to the identifier of the plugin.                                                                                                                                                   |
| `author`  | String    | Recommended | The author of the plugin.                                                                                                                                                                                                                   |
| `category`| String    | Recommended | The category of the plugin. When not provided, this defaults to `Uncategorized`. It's recommended to use category names that other plugins are also using for better grouping in the plugin list.                                            |
| `blocks`  | String array | No       | A list of plugin identifiers to block from loading if this plugin is loaded. Useful when a plugin needs to block an older version of a plugin with a different identifier. Only include if necessary.                                       |
| `perms`   | String    | Deprecated  | (Deprecated) Permissions required to run this plugin. Use the Permissions API instead. Possible values: `free`, `paid`, and `full`.                                                                                                          |
| `siteid`  | Integer   | No          | The ID for this plugin on the Openplanet website, used for update checking. This is automatically added during the review process; you don't need to manually add it.                                                                    |

### Game table

The optional `[game]` table contains game-specific options for the plugin.

| Key         | Type   | Description                                                                                                                                                                                                                     |
| :---------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `min_version` | String | The minimum version of the game required to use this plugin. Format: `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`. E.g., `2022-02-03` matches any game build from February 3rd, 2022 onwards. `2022-02-03 18:03` matches builds on or after 6:03 PM UTC. |
| `max_version` | String | The maximum version of the game required to use this plugin. See `min_version` for format.                                                                                                                                      |

### Script table

The optional `[script]` table configures the script runtime for the plugin.

| Key                | Type        | Description                                                                                                                                                                                                                                                                                               |
| :----------------- | :---------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `timeout`          | Integer     | The timeout time for callback execution in milliseconds. Set to `0` to disable the timeout, which removes execution time tracking overhead but allows infinite loops. Recommended to set to `0` only for performance-critical plugins where you are certain there are no infinite loops. Can be increased for large font/texture loading. |
| `imports`          | String array | Script filenames to include into the plugin module, located in Openplanet's `Scripts` folder. [List of scripts shipped with Openplanet here](URL_TO_SCRIPTS_LIST).                                                                                                                                                   |
| `exports`          | String array | List of files to export to dependent plugins. These scripts are compiled into dependent plugins but not this plugin. See also [Plugin Dependencies](#plugin-dependencies).                                                                                                                                   |
| `shared_exports`   | String array | List of files to export to dependent plugins. Similar to `exports`, but these scripts are also compiled into this plugin. See also [Plugin Dependencies](#plugin-dependencies).                                                                                                                            |
| `dependencies`     | String array | List of plugin identifiers to depend on. These are required dependencies; if not installed, the plugin won't load. See also [Plugin Dependencies](#plugin-dependencies).                                                                                                                                    |
| `export_dependencies`| String array | List of plugin identifiers that are depended on by this plugin and should also be exported to any plugin that depends on *this* plugin (e.g., if Plugin A depends on Plugin B, and Plugin B uses types from Plugin C, C can be `export_dependencies` for B).                                              |
| `optional_dependencies`| String array | List of plugin identifiers to optionally depend on. If not installed, the plugin loads without their exported scripts or `DEPENDENCY_X` define. See also [Plugin Dependencies](#plugin-dependencies).                                                                                             |
| `defines`          | String array | A list of preprocessor options to define during compilation. Useful for development. See also [Preprocessor](#the-preprocessor).                                                                                                                                                                   |
| `module`           | String      | Forces a specific module name. If not provided, the plugin identifier is used. Important for exporting functions to dependent plugins.                                                                                                                                                                    |

---

## Plugin settings

Plugins can save settings in the Openplanet settings file, which can then be edited from within Openplanet's settings window. To define a setting, create a global variable and add a `Setting` metadata line to it.

```angelscript
[Setting name="Something"]
bool Setting_Something;
```

### Supported types

The following types are supported for settings:

*   `bool`
*   `int` (including `int8`, `int16`, `int32`)
*   `uint` (including `uint8`, `uint16`, `uint32`)
*   `float`
*   `double`
*   `string`
*   `vec2`, `vec3`, `vec4`
*   `int2`, `int3`
*   `nat2`, `nat3`
*   `quat`
*   Any `enum`

### Default values

Settings can have default values, specified by the initial global variable value. If not user-defined, the setting will use this default. Users can also reset all settings to their default values in the Openplanet settings dialog.

```angelscript
[Setting name="Amount"]
int Setting_Amount = 10;
```


> **Note:** Settings that are at their default value will not be saved in the settings file. This means if you change a default value, users who were previously on that default will automatically adopt your new default value.

### Attributes

The `Setting` metadata supports a number of optional attributes.

#### Attributes supported for every type:

| Name          | Description                                                                                                                                                                                                                                                                                              |
| :------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`        | The name displayed in the settings dialog.                                                                                                                                                                                                                                                               |
| `description` | The description displayed in the settings dialog, shown as a small question mark icon next to the setting with a tooltip.                                                                                                                                                                                |
| `category`    | The category for the setting. This will automatically create multiple tabs in the settings window, where each category is its own tab.                                                                                                                                                                      |
| `hidden`      | Takes no value. Marks the setting so it will not be displayed in the Openplanet settings dialog. Useful for programmatic storage of settings. Avoid putting too much content here.                                                                                                                          |
| `if`          | Conditional expression (evaluated at runtime) determining whether to display this setting in the settings window. Should be the name of a function, or a global variable that is either a boolean or an enum value. E.g., `if="Setting_Display"`, `if="!Setting_Display"`, `if="Setting_DisplayType SomeValueName"`. (Requires 1.26.26+) |
| `beforerender`| Function to call before this setting is rendered in the settings window. Must point to a global function with signature `void SomeCallback()`. (Requires 1.27.0+)                                                                                                                                      |
| `afterrender` | Function to call after this setting is rendered in the settings window. Must point to a global function with signature `void SomeCallback()`. (Requires 1.27.0+)                                                                                                                                       |

#### Additional attributes for specific types:

| Types                         | Name       | Description                                                                                                                                |
| :---------------------------- | :--------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| `int`, `uint`, `float`, `double` | `min`      | The minimum possible value. When combined with `max`, turns the input field into a slider.                                                 |
| `int`, `uint`, `float`, `double` | `max`      | The maximum possible value. When combined with `min`, turns the input field into a slider.                                                 |
| `int`, `uint`, `float`, `double`, `vec2`, `vec3`, `vec4` | `drag` | Whether to make this a draggable setting (user can drag to change value) rather than requiring typed input.                                |
| `vec3`, `vec4`                | `color`    | Whether this is a color setting. Includes a color picker in the settings dialog.                                                           |
| `string`                      | `max`      | The maximum possible length of the string.                                                                                                 |
| `string`                      | `multiline`| Takes no value. Marks this string as being a multiline input field.                                                                      |
| `string`                      | `password` | Takes no value. Marks this string as being a password, masking the characters with asterisks in the settings dialog.                       |
| `int`, `uint`, `float`, `double` | `step`     | The step size for drag and input fields. (Requires 1.26.26+)                                                                             |

### Hidden settings

Settings can be made hidden using the `hidden` attribute. These will not appear in the Openplanet settings dialog, which is useful for programmatically storing certain settings. Avoid putting too much content into these.

```angelscript
[Setting hidden]
bool Setting_MyHiddenSetting;
```

### Settings tabs

You can create your own scripted settings tabs in the Openplanet settings dialog. To do this, mark a global function with `[SettingsTab]`:

```angelscript
[SettingsTab]
void RenderSettings()
{
  if (UI::Button("Click me!")) {
    print("You clicked the button");
  }
}
```

By default, the tab will be named `Script`. You can change this by passing the `name` attribute (e.g., `[SettingsTab name="Widgets"]`). You can also use a different icon with the `icon` attribute (e.g., `[SettingsTab name="Tags" icon="Tag"]`). As of 1.27.15, you can remove the icon entirely using `icon=""`.

You may also pass `order="n"` where `n` is a number to specify a specific order of tabs.

---

## Script imports

Openplanet comes with a number of optional scripts that you can import into your plugin.

| Script      | Description                                |
| :---------- | :----------------------------------------- |
| `Dialogs.as`| Simple dialog rendering framework.         |
| `Patch.as`  | Helper classes for applying memory patches.|

### Deprecated imports

Some imports have been deprecated and moved to Openplanet's main implementation for improved performance. This means you don't need to manually import these anymore as they will always exist.

*   `Icons.as`: See [Icons](#icons)
*   `Permissions.as`: See [Permissions](URL_TO_PERMISSIONS_DOC)
*   `Time.as`: See [Time](URL_TO_TIME_DOC)
*   `Formatting.as`: See [global namespace](URL_TO_GLOBAL_NAMESPACE_DOC)

### Subject to removal

Some of these imports might be removed in the future or implemented into Openplanet directly, depending on their usage. For example, `Dialogs.as` might disappear due to its low usage.

---

## The preprocessor

Openplanet's Angelscript compiler comes with a preprocessor (based on ccpp). You can use this to selectively omit specific lines of code from the actual script compilation. For example:

```angelscript
#if TMNEXT
  print("I am running on Trackmania (2020)");
#elif MP4
  print("I am running on Maniaplanet 4");
#else
  print("I am running on a different game");
#endif
```

Defines may be combined using the operators `&&` (and) and `||` (or). Note that currently these operators are very basic and do not adhere to any specific order of operations, and you can not group them using parenthesis. In other words: the conditions are tested from left to right no matter what.

### Available defines

The following is a list of all available preprocessor defines, including ones that are generally not available publicly:

| Define         | Defined when...                                    |
| :------------- | :------------------------------------------------- |
| `UNITED`       | The current game is Trackmania United              |
| `MP3`          | The current game is Maniaplanet 3                  |
| `TURBO`        | The current game is Trackmania Turbo               |
| `MP4`          | The current game is Maniaplanet 4 (includes 4.0 and 4.1) |
| `MP40`         | The current game is Maniaplanet 4.0                |
| `MP41`         | The current game is Maniaplanet 4.1                |
| `TMNEXT`       | The current game is Trackmania (2020)              |
| `LOGS`         | The current game is a Logs-configured build (e.g., Nadeo development builds or "logs" executables) |
| `HAS_DEV`      | The current game is a Nadeo development build      |
| `SERVER`       | The current game is a dedicated server build       |
| `MANIA64`      | The current game is a 64-bit build                 |
| `MANIA32`      | The current game is a 32-bit build                 |
| `WINDOWS`      | The current OS is Windows                          |
| `WINDOWS_WINE` | The current OS is Windows through WINE             |
| `LINUX`        | The current OS is Linux                            |
| `DEVELOPER`    | The current Openplanet build is a debug build      |

### Defines for signature modes

Signature modes have their own preprocessor defines. They are defined when the current signature level is equal to or below their respective level:

| Current / Define | `SIG_OFFICIAL` | `SIG_REGULAR` | `SIG_SCHOOL` | `SIG_DEVELOPER` |
| :--------------- | :------------- | :------------ | :----------- | :-------------- |
| Official         | ✅             | ❌            | ❌           | ❌              |
| Regular          | ✅             | ✅            | ❌           | ❌              |
| School           | ✅             | ✅            | ✅           | ❌              |
| Developer        | ✅             | ✅            | ✅           | ✅              |

### Defines for competition profiles

Competition profiles have a define with the `COMP_` prefix. For example, a competition with an ID of `BOB` would define `COMP_BOB`. Additional defines may be configured. If you need more defines for your competition profile, contact Openplanet developers.

---

## Icons

Many icons can be used in the UI by simply using the string constants in the `Icons` namespace. Here's a list of them:

| Icon | Code | Icon | Code | Icon | Code |
| :--- | :--- | :--- | :--- | :--- | :--- |
|  | `Icons::TikTok` |  | `Icons::TrackmaniaT` |  | `Icons::TrackmaniaM` |
|  | `Icons::Ubisoft` |  | `Icons::ManiaExchange` |  | `Icons::ItemExchange` |
|  | `Icons::ManiaPark` |  | `Icons::Evo` |  | `Icons::Dodecahedron` |
|  | `Icons::Glass` |  | `Icons::Music` |  | `Icons::Search` |
|  | `Icons::EnvelopeO` |  | `Icons::Heart` |  | `Icons::Star` |
|  | `Icons::StarO` |  | `Icons::User` |  | `Icons::Film` |
|  | `Icons::ThLarge` |  | `Icons::Th` |  | `Icons::ThList` |
|  | `Icons::Check` |  | `Icons::Times` |  | `Icons::SearchPlus` |
|  | `Icons::SearchMinus` |  | `Icons::PowerOff` |  | `Icons::Signal` |
|  | `Icons::Cog` |  | `Icons::TrashO` |  | `Icons::Home` |
|  | `Icons::FileO` |  | `Icons::ClockO` |  | `Icons::Road` |
|  | `Icons::Download` |  | `Icons::ArrowCircleODown` |  | `Icons::ArrowCircleOUp` |
|  | `Icons::Inbox` |  | `Icons::PlayCircleO` |  | `Icons::Repeat` |
|  | `Icons::Refresh` |  | `Icons::ListAlt` |  | `Icons::Lock` |
|  | `Icons::Flag` |  | `Icons::Headphones` |  | `Icons::VolumeOff` |
|  | `Icons::VolumeDown` |  | `Icons::VolumeUp` |  | `Icons::Qrcode` |
|  | `Icons::Barcode` |  | `Icons::Tag` |  | `Icons::Tags` |
|  | `Icons::Book` |  | `Icons::Bookmark` |  | `Icons::Print` |
|  | `Icons::Camera` |  | `Icons::Font` |  | `Icons::Bold` |
|  | `Icons::Italic` |  | `Icons::TextHeight` |  | `Icons::TextWidth` |
|  | `Icons::AlignLeft` |  | `Icons::AlignCenter` |  | `Icons::AlignRight` |
|  | `Icons::AlignJustify` |  | `Icons::List` |  | `Icons::Outdent` |
|  | `Icons::Indent` |  | `Icons::VideoCamera` |  | `Icons::PictureO` |
|  | `Icons::Pencil` |  | `Icons::MapMarker` |  | `Icons::Adjust` |
|  | `Icons::Tint` |  | `Icons::PencilSquareO` |  | `Icons::ShareSquareO` |
|  | `Icons::CheckSquareO` |  | `Icons::Arrows` |  | `Icons::StepBackward` |
|  | `Icons::FastBackward` |  | `Icons::Backward` |  | `Icons::Play` |
|  | `Icons::Pause` |  | `Icons::Stop` |  | `Icons::Forward` |
|  | `Icons::FastForward` |  | `Icons::StepForward` |  | `Icons::Eject` |
|  | `Icons::ChevronLeft` |  | `Icons::ChevronRight` |  | `Icons::PlusCircle` |
|  | `Icons::MinusCircle` |  | `Icons::TimesCircle` |  | `Icons::CheckCircle` |
|  | `Icons::QuestionCircle` |  | `Icons::InfoCircle` |  | `Icons::Crosshairs` |
|  | `Icons::TimesCircleO` |  | `Icons::CheckCircleO` |  | `Icons::Ban` |
|  | `Icons::ArrowLeft` |  | `Icons::ArrowRight` |  | `Icons::ArrowUp` |
|  | `Icons::ArrowDown` |  | `Icons::Share` |  | `Icons::Expand` |
|  | `Icons::Compress` |  | `Icons::Plus` |  | `Icons::Minus` |
|  | `Icons::Asterisk` |  | `Icons::ExclamationCircle` |  | `Icons::Gift` |
|  | `Icons::Leaf` |  | `Icons::Fire` |  | `Icons::Eye` |
|  | `Icons::EyeSlash` |  | `Icons::ExclamationTriangle` |  | `Icons::Plane` |
|  | `Icons::Calendar` |  | `Icons::Random` |  | `Icons::Comment` |
|  | `Icons::Magnet` |  | `Icons::ChevronUp` |  | `Icons::ChevronDown` |
|  | `Icons::Retweet` |  | `Icons::ShoppingCart` |  | `Icons::Folder` |
|  | `Icons::FolderOpen` |  | `Icons::ArrowsV` |  | `Icons::ArrowsH` |
|  | `Icons::BarChart` |  | `Icons::TwitterSquare` |  | `Icons::FacebookSquare` |
|  | `Icons::CameraRetro` |  | `Icons::Key` |  | `Icons::Cogs` |
|  | `Icons::Comments` |  | `Icons::ThumbsOUp` |  | `Icons::ThumbsODown` |
|  | `Icons::StarHalf` |  | `Icons::HeartO` |  | `Icons::SignOut` |
|  | `Icons::LinkedinSquare` |  | `Icons::ThumbTack` |  | `Icons::ExternalLink` |
|  | `Icons::SignIn` |  | `Icons::Trophy` |  | `Icons::GithubSquare` |
|  | `Icons::Upload` |  | `Icons::LemonO` |  | `Icons::Phone` |
|  | `Icons::SquareO` |  | `Icons::BookmarkO` |  | `Icons::PhoneSquare` |
|  | `Icons::Twitter` |  | `Icons::Facebook` |  | `Icons::Github` |
|  | `Icons::Unlock` |  | `Icons::CreditCard` |  | `Icons::Rss` |
|  | `Icons::HddO` |  | `Icons::Bullhorn` |  | `Icons::BellO` |
|  | `Icons::Certificate` |  | `Icons::HandORight` |  | `Icons::HandOLeft` |
|  | `Icons::HandOUp` |  | `Icons::HandODown` |  | `Icons::ArrowCircleLeft` |
|  | `Icons::ArrowCircleRight` |  | `Icons::ArrowCircleUp` |  | `Icons::ArrowCircleDown` |
|  | `Icons::Globe` |  | `Icons::GlobeE` |  | `Icons::GlobeW` |
|  | `Icons::Wrench` |  | `Icons::Tasks` |  | `Icons::Filter` |
|  | `Icons::Briefcase` |  | `Icons::ArrowsAlt` |  | `Icons::Users` |
|  | `Icons::Link` |  | `Icons::Cloud` |  | `Icons::Flask` |
|  | `Icons::Scissors` |  | `Icons::FilesO` |  | `Icons::Paperclip` |
|  | `Icons::FloppyO` |  | `Icons::Square` |  | `Icons::Bars` |
|  | `Icons::ListUl` |  | `Icons::ListOl` |  | `Icons::Strikethrough` |
|  | `Icons::Underline` |  | `Icons::Table` |  | `Icons::Magic` |
|  | `Icons::Truck` |  | `Icons::Pinterest` |  | `Icons::PinterestSquare` |
|  | `Icons::GooglePlusSquare` |  | `Icons::GooglePlus` |  | `Icons::Money` |
|  | `Icons::CaretDown` |  | `Icons::CaretUp` |  | `Icons::CaretLeft` |
|  | `Icons::CaretRight` |  | `Icons::Columns` |  | `Icons::Sort` |
|  | `Icons::SortDesc` |  | `Icons::SortAsc` |  | `Icons::Envelope` |
|  | `Icons::Linkedin` |  | `Icons::Undo` |  | `Icons::Gavel` |
|  | `Icons::Tachometer` |  | `Icons::CommentO` |  | `Icons::CommentsO` |
|  | `Icons::Bolt` |  | `Icons::Sitemap` |  | `Icons::Umbrella` |
|  | `Icons::Clipboard` |  | `Icons::LightbulbO` |  | `Icons::Exchange` |
|  | `Icons::CloudDownload` |  | `Icons::CloudUpload` |  | `Icons::UserMd` |
|  | `Icons::Stethoscope` |  | `Icons::Suitcase` |  | `Icons::Bell` |
|  | `Icons::Coffee` |  | `Icons::Cutlery` |  | `Icons::FileTextO` |
|  | `Icons::BuildingO` |  | `Icons::HospitalO` |  | `Icons::Ambulance` |
|  | `Icons::Medkit` |  | `Icons::FighterJet` |  | `Icons::Beer` |
|  | `Icons::HSquare` |  | `Icons::PlusSquare` |  | `Icons::AngleDoubleLeft` |
|  | `Icons::AngleDoubleRight` |  | `Icons::AngleDoubleUp` |  | `Icons::AngleDoubleDown` |
|  | `Icons::AngleLeft` |  | `Icons::AngleRight` |  | `Icons::AngleUp` |
|  | `Icons::AngleDown` |  | `Icons::Desktop` |  | `Icons::Laptop` |
|  | `Icons::Tablet` |  | `Icons::Mobile` |  | `Icons::CircleO` |
|  | `Icons::QuoteLeft` |  | `Icons::QuoteRight` |  | `Icons::Spinner` |
|  | `Icons::Circle` |  | `Icons::Reply` |  | `Icons::GithubAlt` |
|  | `Icons::FolderO` |  | `Icons::FolderOpenO` |  | `Icons::SmileO` |
|  | `Icons::FrownO` |  | `Icons::MehO` |  | `Icons::Gamepad` |
|  | `Icons::KeyboardO` |  | `Icons::FlagO` |  | `Icons::FlagCheckered` |
|  | `Icons::Terminal` |  | `Icons::Code` |  | `Icons::ReplyAll` |
|  | `Icons::StarHalfO` |  | `Icons::LocationArrow` |  | `Icons::Crop` |
|  | `Icons::CodeFork` |  | `Icons::ChainBroken` |  | `Icons::Question` |
|  | `Icons::Info` |  | `Icons::Exclamation` |  | `Icons::Superscript` |
|  | `Icons::Subscript` |  | `Icons::Eraser` |  | `Icons::PuzzlePiece` |
|  | `Icons::Microphone` |  | `Icons::MicrophoneSlash` |  | `Icons::Shield` |
|  | `Icons::CalendarO` |  | `Icons::FireExtinguisher` |  | `Icons::Rocket` |
|  | `Icons::Maxcdn` |  | `Icons::ChevronCircleLeft` |  | `Icons::ChevronCircleRight` |
|  | `Icons::ChevronCircleUp` |  | `Icons::ChevronCircleDown` |  | `Icons::Html5` |
|  | `Icons::Css3` |  | `Icons::Anchor` |  | `Icons::UnlockAlt` |
|  | `Icons::Bullseye` |  | `Icons::EllipsisH` |  | `Icons::EllipsisV` |
|  | `Icons::RssSquare` |  | `Icons::PlayCircle` |  | `Icons::Ticket` |
|  | `Icons::MinusSquare` |  | `Icons::MinusSquareO` |  | `Icons::LevelUp` |
|  | `Icons::LevelDown` |  | `Icons::CheckSquare` |  | `Icons::PencilSquare` |
|  | `Icons::ExternalLinkSquare` |  | `Icons::ShareSquare` |  | `Icons::Compass` |
|  | `Icons::CaretSquareODown` |  | `Icons::CaretSquareOUp` |  | `Icons::CaretSquareORight` |
|  | `Icons::Eur` |  | `Icons::Gbp` |  | `Icons::Usd` |
|  | `Icons::Inr` |  | `Icons::Jpy` |  | `Icons::Rub` |
|  | `Icons::Krw` |  | `Icons::Btc` |  | `Icons::File` |
|  | `Icons::FileText` |  | `Icons::SortAlphaAsc` |  | `Icons::SortAlphaDesc` |
|  | `Icons::SortAmountAsc` |  | `Icons::SortAmountDesc` |  | `Icons::SortNumericAsc` |
|  | `Icons::SortNumericDesc` |  | `Icons::ThumbsUp` |  | `Icons::ThumbsDown` |
|  | `Icons::YoutubeSquare` |  | `Icons::Youtube` |  | `Icons::Xing` |
|  | `Icons::XingSquare` |  | `Icons::YoutubePlay` |  | `Icons::Dropbox` |
|  | `Icons::StackOverflow` |  | `Icons::Instagram` |  | `Icons::Flickr` |
|  | `Icons::Adn` |  | `Icons::Bitbucket` |  | `Icons::BitbucketSquare` |
|  | `Icons::Tumblr` |  | `Icons::TumblrSquare` |  | `Icons::LongArrowDown` |
|  | `Icons::LongArrowUp` |  | `Icons::LongArrowLeft` |  | `Icons::LongArrowRight` |
|  | `Icons::Apple` |  | `Icons::Windows` |  | `Icons::Android` |
|  | `Icons::Linux` |  | `Icons::Dribbble` |  | `Icons::Skype` |
|  | `Icons::Foursquare` |  | `Icons::Trello` |  | `Icons::Female` |
|  | `Icons::Male` |  | `Icons::Gratipay` |  | `Icons::SunO` |
|  | `Icons::MoonO` |  | `Icons::Archive` |  | `Icons::Bug` |
|  | `Icons::Vk` |  | `Icons::Weibo` |  | `Icons::Renren` |
|  | `Icons::Pagelines` |  | `Icons::StackExchange` |  | `Icons::ArrowCircleORight` |
|  | `Icons::ArrowCircleOLeft` |  | `Icons::CaretSquareOLeft` |  | `Icons::DotCircleO` |
|  | `Icons::Wheelchair` |  | `Icons::VimeoSquare` |  | `Icons::Try` |
|  | `Icons::PlusSquareO` |  | `Icons::SpaceShuttle` |  | `Icons::Slack` |
|  | `Icons::EnvelopeSquare` |  | `Icons::Wordpress` |  | `Icons::Openid` |
|  | `Icons::University` |  | `Icons::GraduationCap` |  | `Icons::Yahoo` |
|  | `Icons::Google` |  | `Icons::Reddit` |  | `Icons::RedditSquare` |
|  | `Icons::StumbleuponCircle` |  | `Icons::Stumbleupon` |  | `Icons::Delicious` |
|  | `Icons::Digg` |  | `Icons::Drupal` |  | `Icons::Joomla` |
|  | `Icons::Language` |  | `Icons::Fax` |  | `Icons::Building` |
|  | `Icons::Child` |  | `Icons::Paw` |  | `Icons::Spoon` |
|  | `Icons::Cube` |  | `Icons::Cubes` |  | `Icons::Behance` |
|  | `Icons::BehanceSquare` |  | `Icons::Steam` |  | `Icons::SteamSquare` |
|  | `Icons::Recycle` |  | `Icons::Car` |  | `Icons::Taxi` |
|  | `Icons::Tree` |  | `Icons::Spotify` |  | `Icons::Deviantart` |
|  | `Icons::Soundcloud` |  | `Icons::Database` |  | `Icons::FilePdfO` |
|  | `Icons::FileWordO` |  | `Icons::FileExcelO` |  | `Icons::FilePowerpointO` |
|  | `Icons::FileImageO` |  | `Icons::FileArchiveO` |  | `Icons::FileAudioO` |
|  | `Icons::FileVideoO` |  | `Icons::FileCodeO` |  | `Icons::Vine` |
|  | `Icons::Codepen` |  | `Icons::Jsfiddle` |  | `Icons::LifeRing` |
|  | `Icons::CircleONotch` |  | `Icons::Rebel` |  | `Icons::Empire` |
|  | `Icons::GitSquare` |  | `Icons::Git` |  | `Icons::HackerNews` |
|  | `Icons::TencentWeibo` |  | `Icons::Qq` |  | `Icons::Weixin` |
|  | `Icons::PaperPlane` |  | `Icons::PaperPlaneO` |  | `Icons::History` |
|  | `Icons::CircleThin` |  | `Icons::Header` |  | `Icons::Paragraph` |
|  | `Icons::Sliders` |  | `Icons::ShareAlt` |  | `Icons::ShareAltSquare` |
|  | `Icons::Bomb` |  | `Icons::FutbolO` |  | `Icons::Tty` |
|  | `Icons::Binoculars` |  | `Icons::Plug` |  | `Icons::Slideshare` |
|  | `Icons::Twitch` |  | `Icons::Yelp` |  | `Icons::NewspaperO` |
|  | `Icons::Wifi` |  | `Icons::Calculator` |  | `Icons::Paypal` |
|  | `Icons::GoogleWallet` |  | `Icons::CcVisa` |  | `Icons::CcMastercard` |
|  | `Icons::CcDiscover` |  | `Icons::CcAmex` |  | `Icons::CcPaypal` |
|  | `Icons::CcStripe` |  | `Icons::BellSlash` |  | `Icons::BellSlashO` |
|  | `Icons::Trash` |  | `Icons::Copyright` |  | `Icons::At` |
|  | `Icons::Eyedropper` |  | `Icons::PaintBrush` |  | `Icons::BirthdayCake` |
|  | `Icons::AreaChart` |  | `Icons::PieChart` |  | `Icons::LineChart` |
|  | `Icons::Lastfm` |  | `Icons::LastfmSquare` |  | `Icons::ToggleOff` |
|  | `Icons::ToggleOn` |  | `Icons::Bicycle` |  | `Icons::Bus` |
|  | `Icons::Ioxhost` |  | `Icons::Angellist` |  | `Icons::Cc` |
|  | `Icons::Ils` |  | `Icons::Meanpath` |  | `Icons::Buysellads` |
|  | `Icons::Connectdevelop` |  | `Icons::Dashcube` |  | `Icons::Forumbee` |
|  | `Icons::Leanpub` |  | `Icons::Sellsy` |  | `Icons::Shirtsinbulk` |
|  | `Icons::Simplybuilt` |  | `Icons::Skyatlas` |  | `Icons::CartPlus` |
|  | `Icons::CartArrowDown` |  | `Icons::Diamond` |  | `Icons::Ship` |
|  | `Icons::UserSecret` |  | `Icons::Motorcycle` |  | `Icons::StreetView` |
|  | `Icons::Heartbeat` |  | `Icons::Venus` |  | `Icons::Mars` |
|  | `Icons::Mercury` |  | `Icons::Transgender` |  | `Icons::TransgenderAlt` |
|  | `Icons::VenusDouble` |  | `Icons::MarsDouble` |  | `Icons::VenusMars` |
|  | `Icons::MarsStroke` |  | `Icons::MarsStrokeV` |  | `Icons::MarsStrokeH` |
|  | `Icons::Neuter` |  | `Icons::Genderless` |  | `Icons::FacebookOfficial` |
|  | `Icons::PinterestP` |  | `Icons::Whatsapp` |  | `Icons::Server` |
|  | `Icons::UserPlus` |  | `Icons::UserTimes` |  | `Icons::Bed` |
|  | `Icons::Viacoin` |  | `Icons::Train` |  | `Icons::Subway` |
|  | `Icons::Medium` |  | `Icons::MediumSquare` |  | `Icons::YCombinator` |
|  | `Icons::OptinMonster` |  | `Icons::Opencart` |  | `Icons::Expeditedssl` |
|  | `Icons::BatteryFull` |  | `Icons::BatteryThreeQuarters` |  | `Icons::BatteryHalf` |
|  | `Icons::BatteryQuarter` |  | `Icons::BatteryEmpty` |  | `Icons::MousePointer` |
|  | `Icons::ICursor` |  | `Icons::ObjectGroup` |  | `Icons::ObjectUngroup` |
|  | `Icons::StickyNote` |  | `Icons::StickyNoteO` |  | `Icons::CcJcb` |
|  | `Icons::CcDinersClub` |  | `Icons::Clone` |  | `Icons::BalanceScale` |
|  | `Icons::HourglassO` |  | `Icons::HourglassStart` |  | `Icons::HourglassHalf` |
|  | `Icons::HourglassEnd` |  | `Icons::Hourglass` |  | `Icons::HandRockO` |
|  | `Icons::HandPaperO` |  | `Icons::HandScissorsO` |  | `Icons::HandLizardO` |
|  | `Icons::HandSpockO` |  | `Icons::HandPointerO` |  | `Icons::HandPeaceO` |
|  | `Icons::Trademark` |  | `Icons::Registered` |  | `Icons::CreativeCommons` |
|  | `Icons::Gg` |  | `Icons::GgCircle` |  | `Icons::Tripadvisor` |
|  | `Icons::Odnoklassniki` |  | `Icons::OdnoklassnikiSquare` |  | `Icons::GetPocket` |
|  | `Icons::WikipediaW` |  | `Icons::Safari` |  | `Icons::Chrome` |
|  | `Icons::Firefox` |  | `Icons::Opera` |  | `Icons::InternetExplorer` |
|  | `Icons::Television` |  | `Icons::Contao` |  | `Icons::The500px` |
|  | `Icons::Amazon` |  | `Icons::CalendarPlusO` |  | `Icons::CalendarMinusO` |
|  | `Icons::CalendarTimesO` |  | `Icons::CalendarCheckO` |  | `Icons::Industry` |
|  | `Icons::MapPin` |  | `Icons::MapSigns` |  | `Icons::MapO` |
|  | `Icons::Map` |  | `Icons::Commenting` |  | `Icons::CommentingO` |
|  | `Icons::Houzz` |  | `Icons::Vimeo` |  | `Icons::BlackTie` |
|  | `Icons::Fonticons` |  | `Icons::RedditAlien` |  | `Icons::Edge` |
|  | `Icons::CreditCardAlt` |  | `Icons::Codiepie` |  | `Icons::Modx` |
|  | `Icons::FortAwesome` |  | `Icons::Usb` |  | `Icons::ProductHunt` |
|  | `Icons::Mixcloud` |  | `Icons::Scribd` |  | `Icons::PauseCircle` |
|  | `Icons::PauseCircleO` |  | `Icons::StopCircle` |  | `Icons::StopCircleO` |
|  | `Icons::ShoppingBag` |  | `Icons::ShoppingBasket` |  | `Icons::Hashtag` |
|  | `Icons::Bluetooth` |  | `Icons::BluetoothB` |  | `Icons::Percent` |
|  | `Icons::Gitlab` |  | `Icons::Wpbeginner` |  | `Icons::Wpforms` |
|  | `Icons::Envira` |  | `Icons::UniversalAccess` |  | `Icons::WheelchairAlt` |
|  | `Icons::QuestionCircleO` |  | `Icons::Blind` |  | `Icons::AudioDescription` |
|  | `Icons::VolumeControlPhone` |  | `Icons::Braille` |  | `Icons::AssistiveListeningSystems` |
|  | `Icons::AmericanSignLanguageInterpreting` |  | `Icons::Deaf` |  | `Icons::Glide` |
|  | `Icons::GlideG` |  | `Icons::SignLanguage` |  | `Icons::LowVision` |
|  | `Icons::Viadeo` |  | `Icons::ViadeoSquare` |  | `Icons::Snapchat` |
|  | `Icons::SnapchatGhost` |  | `Icons::SnapchatSquare` |  | `Icons::FirstOrder` |
|  | `Icons::Yoast` |  | `Icons::Themeisle` |  | `Icons::GooglePlusOfficial` |
|  | `Icons::FontAwesome` |  | `Icons::HandshakeO` |  | `Icons::EnvelopeOpen` |
|  | `Icons::EnvelopeOpenO` |  | `Icons::Linode` |  | `Icons::AddressBook` |
|  | `Icons::AddressBookO` |  | `Icons::AddressCard` |  | `Icons::AddressCardO` |
|  | `Icons::UserCircle` |  | `Icons::UserCircleO` |  | `Icons::UserO` |
|  | `Icons::IdBadge` |  | `Icons::IdCard` |  | `Icons::IdCardO` |
|  | `Icons::Quora` |  | `Icons::FreeCodeCamp` |  | `Icons::Telegram` |
|  | `Icons::ThermometerFull` |  | `Icons::ThermometerThreeQuarters` |  | `Icons::ThermometerHalf` |
|  | `Icons::ThermometerQuarter` |  | `Icons::ThermometerEmpty` |  | `Icons::Shower` |
|  | `Icons::Bath` |  | `Icons::Podcast` |  | `Icons::WindowMaximize` |
|  | `Icons::WindowMinimize` |  | `Icons::WindowRestore` |  | `Icons::WindowClose` |
|  | `Icons::WindowCloseO` |  | `Icons::Bandcamp` |  | `Icons::Grav` |
|  | `Icons::Etsy` |  | `Icons::Imdb` |  | `Icons::Ravelry` |
|  | `Icons::Eercast` |  | `Icons::Microchip` |  | `Icons::SnowflakeO` |
|  | `Icons::Superpowers` |  | `Icons::Wpexplorer` |  | `Icons::Meetup` |
|  | `Icons::Mastodon` |  | `Icons::MastodonAlt` |  | `Icons::ForkAwesomeIcon` |
|  | `Icons::Peertube` |  | `Icons::Diaspora` |  | `Icons::Friendica` |
|  | `Icons::GnuSocial` |  | `Icons::LiberapaySquare` |  | `Icons::Liberapay` |
|  | `Icons::Scuttlebutt` |  | `Icons::Hubzilla` |  | `Icons::SocialHome` |
|  | `Icons::Artstation` |  | `Icons::Discord` |  | `Icons::DiscordAlt` |
|  | `Icons::Patreon` |  | `Icons::Snowdrift` |  | `Icons::Activitypub` |
|  | `Icons::Ethereum` |  | `Icons::Keybase` |  | `Icons::Shaarli` |
|  | `Icons::ShaarliO` |  | `Icons::KeyModern` |  | `Icons::Xmpp` |
|  | `Icons::ArchiveOrg` |  | `Icons::Freedombox` |  | `Icons::FacebookMessenger` |
|  | `Icons::Debian` |  | `Icons::MastodonSquare` |  | `Icons::Tipeee` |
|  | `Icons::React` |  | `Icons::Dogmazic` |  | `Icons::Zotero` |
|  | `Icons::Nodejs` |  | `Icons::Nextcloud` |  | `Icons::NextcloudSquare` |
|  | `Icons::Hackaday` |  | `Icons::Laravel` |  | `Icons::Signalapp` |
|  | `Icons::Gnupg` |  | `Icons::Php` |  | `Icons::Ffmpeg` |
|  | `Icons::Joplin` |  | `Icons::Syncthing` |  | `Icons::Inkscape` |
|  | `Icons::MatrixOrg` |  | `Icons::Pixelfed` |  | `Icons::Bootstrap` |
|  | `Icons::DevTo` |  | `Icons::Hashnode` |  | `Icons::Jirafeau` |
|  | `Icons::Emby` |  | `Icons::Wikidata` |  | `Icons::Gimp` |
|  | `Icons::C` |  | `Icons::Digitalocean` |  | `Icons::Att` |
|  | `Icons::Gitea` |  | `Icons::FileEpub` |  | `Icons::Python` |
|  | `Icons::Archlinux` |  | `Icons::Pleroma` |  | `Icons::Unsplash` |
|  | `Icons::Hackster` |  | `Icons::SpellCheck` |  | `Icons::Moon` |
|  | `Icons::Sun` |  | `Icons::FDroid` |  | `Icons::Biometric` |
|  | `Icons::Kenney::Home` |  | `Icons::Kenney::Adjust` |  | `Icons::Kenney::Wrench` |
|  | `Icons::Kenney::Cog` |  | `Icons::Kenney::Off` |  | `Icons::Kenney::Expand` |
|  | `Icons::Kenney::Reduce` |  | `Icons::Kenney::Movie` |  | `Icons::Kenney::Flap` |
|  | `Icons::Kenney::ShoppingCart` |  | `Icons::Kenney::ShoppingCase` |  | `Icons::Kenney::External` |
|  | `Icons::Kenney::Network` |  | `Icons::Kenney::Check` |  | `Icons::Kenney::Times` |
|  | `Icons::Kenney::TimesCircle` |  | `Icons::Kenney::Plus` |  | `Icons::Kenney::PlusCircle` |
|  | `Icons::Kenney::Minus` |  | `Icons::Kenney::MinusCircle` |  | `Icons::Kenney::Info` |
|  | `Icons::Kenney::InfoCircle` |  | `Icons::Kenney::Question` |  | `Icons::Kenney::QuestionCircle` |
|  | `Icons::Kenney::Exlamation` |  | `Icons::Kenney::ExclamationCircle` |  | `Icons::Kenney::ExclamationTriangle` |
|  | `Icons::Kenney::PaintBrush` |  | `Icons::Kenney::Pencil` |  | `Icons::Kenney::Checkbox` |
|  | `Icons::Kenney::CheckboxChecked` |  | `Icons::Kenney::Radio` |  | `Icons::Kenney::RadioChecked` |
|  | `Icons::Kenney::SortVertical` |  | `Icons::Kenney::SortHorizontal` |  | `Icons::Kenney::Grid` |
|  | `Icons::Kenney::List` |  | `Icons::Kenney::Rows` |  | `Icons::Kenney::Cells` |
|  | `Icons::Kenney::SignalLow` |  | `Icons::Kenney::SignalMedium` |  | `Icons::Kenney::SignalHigh` |
|  | `Icons::Kenney::Trash` |  | `Icons::Kenney::TrashAlt` |  | `Icons::Kenney::ReloadInverse` |
|  | `Icons::Kenney::Reload` |  | `Icons::Kenney::Top` |  | `Icons::Kenney::Bottom` |
|  | `Icons::Kenney::Upload` |  | `Icons::Kenney::Download` |  | `Icons::Kenney::Cloud` |
|  | `Icons::Kenney::CloudUpload` |  | `Icons::Kenney::CloudDownload` |  | `Icons::Kenney::Search` |
|  | `Icons::Kenney::SearchPlus` |  | `Icons::Kenney::SearchMinus` |  | `Icons::Kenney::SearchEqual` |
|  | `Icons::Kenney::Lock` |  | `Icons::Kenney::Unlock` |  | `Icons::Kenney::User` |
|  | `Icons::Kenney::Users` |  | `Icons::Kenney::UsersAlt` |  | `Icons::Kenney::SignIn` |
|  | `Icons::Kenney::SignInInverse` |  | `Icons::Kenney::SignOut` |  | `Icons::Kenney::SignOutInverse` |
|  | `Icons::Kenney::ArrowTop` |  | `Icons::Kenney::ArrowRight` |  | `Icons::Kenney::ArrowBottom` |
|  | `Icons::Kenney::ArrowLeft` |  | `Icons::Kenney::ArrowTopLeft` |  | `Icons::Kenney::ArrowTopRight` |
|  | `Icons::Kenney::ArrowBottomRight` |  | `Icons::Kenney::ArrowBottomLeft` |  | `Icons::Kenney::CaretTop` |
|  | `Icons::Kenney::CaretRight` |  | `Icons::Kenney::CaretBottom` |  | `Icons::Kenney::CaretLeft` |
|  | `Icons::Kenney::NextAlt` |  | `Icons::Kenney::Next` |  | `Icons::Kenney::Previous` |
|  | `Icons::Kenney::PreviousAlt` |  | `Icons::Kenney::Fill` |  | `Icons::Kenney::Eraser` |
|  | `Icons::Kenney::Save` |  | `Icons::Kenney::StepBackward` |  | `Icons::Kenney::Backward` |
|  | `Icons::Kenney::Pause` |  | `Icons::Kenney::Forward` |  | `Icons::Kenney::StepForward` |
|  | `Icons::Kenney::Stop` |  | `Icons::Kenney::Rec` |  | `Icons::Kenney::Cursor` |
|  | `Icons::Kenney::Pointer` |  | `Icons::Kenney::Exit` |  | `Icons::Kenney::Figure` |
|  | `Icons::Kenney::Car` |  | `Icons::Kenney::Coin` |  | `Icons::Kenney::Key` |
|  | `Icons::Kenney::Cub` |  | `Icons::Kenney::Diamond` |  | `Icons::Kenney::Badge` |
|  | `Icons::Kenney::BadgeAlt` |  | `Icons::Kenney::Podium` |  | `Icons::Kenney::PodiumAlt` |
|  | `Icons::Kenney::Flag` |  | `Icons::Kenney::Fist` |  | `Icons::Kenney::FistCircle` |
|  | `Icons::Kenney::Heart` |  | `Icons::Kenney::HeartHalf` |  | `Icons::Kenney::HeartHalfO` |
|  | `Icons::Kenney::HeartO` |  | `Icons::Kenney::Star` |  | `Icons::Kenney::StarHalf` |
|  | `Icons::Kenney::StarHalfO` |  | `Icons::Kenney::StarO` |  | `Icons::Kenney::ButtonB` |
|  | `Icons::Kenney::MusicOn` |  | `Icons::Kenney::MusicOff` |  | `Icons::Kenney::SoundOn` |
|  | `Icons::Kenney::SoundOff` |  | `Icons::Kenney::SoundOffAlt` |  | `Icons::Kenney::Robot` |
|  | `Icons::Kenney::Computer` |  | `Icons::Kenney::Tablet` |  | `Icons::Kenney::Smartphone` |
|  | `Icons::Kenney::Device` |  | `Icons::Kenney::DeviceTiltLeft` |  | `Icons::Kenney::DeviceTiltRight` |
|  | `Icons::Kenney::Gamepad` |  | `Icons::Kenney::GamepadAlt` |  | `Icons::Kenney::GamepadTiltLeft` |
|  | `Icons::Kenney::GamepadTiltRight` |  | `Icons::Kenney::PlayerOne` |  | `Icons::Kenney::PlayerTwo` |
|  | `Icons::Kenney::PlayerThree` |  | `Icons::Kenney::PlayerFour` |  | `Icons::Kenney::Joystick` |
|  | `Icons::Kenney::JoystickAlt` |  | `Icons::Kenney::JoystickLeft` |  | `Icons::Kenney::JoystickRight` |
|  | `Icons::Kenney::MouseAlt` |  | `Icons::Kenney::Mouse` |  | `Icons::Kenney::MouseLeftButton` |
|  | `Icons::Kenney::MouseRightButton` |  | `Icons::Kenney::ButtonOne` |  | `Icons::Kenney::ButtonTwo` |
|  | `Icons::Kenney::ButtonThree` |  | `Icons::Kenney::ButtonA` |  | `Icons::Kenney::ButtonX` |
|  | `Icons::Kenney::ButonY` |  | `Icons::Kenney::ButtonTimes` |  | `Icons::Kenney::ButtonSquare` |
|  | `Icons::Kenney::ButtonCircle` |  | `Icons::Kenney::ButtonTriangle` |  | `Icons::Kenney::ButtonLeft` |
|  | `Icons::Kenney::ButtonL` |  | `Icons::Kenney::ButtonL1` |  | `Icons::Kenney::ButtonL2` |
|  | `Icons::Kenney::ButtonLb` |  | `Icons::Kenney::ButtonLt` |  | `Icons::Kenney::ButtonRt` |
|  | `Icons::Kenney::ButtonRb` |  | `Icons::Kenney::ButtonR2` |  | `Icons::Kenney::ButtonR1` |
|  | `Icons::Kenney::ButtonR` |  | `Icons::Kenney::ButtonRight` |  | `Icons::Kenney::ButtonEmpty` |
|  | `Icons::Kenney::ButtonStart` |  | `Icons::Kenney::ButtonSelect` |  | `Icons::Kenney::Dpad` |
|  | `Icons::Kenney::DpadAlt` |  | `Icons::Kenney::DpadTop` |  | `Icons::Kenney::DpadRight` |
|  | `Icons::Kenney::DpadBottom` |  | `Icons::Kenney::DpadLeft` |  | `Icons::Kenney::KeyLarge` |
|  | `Icons::Kenney::KeyLarge3d` |  | `Icons::Kenney::KeySmall` |  | `Icons::Kenney::KeySmall3d` |
|  | `Icons::Kenney::StickLeftTop` |  | `Icons::Kenney::StickLeftSide` |  | `Icons::Kenney::StickRightSide` |
|  | `Icons::Kenney::StickRightTop` |  | `Icons::Kenney::StickSide` |  | `Icons::Kenney::StickTiltLeft` |
|  | `Icons::Kenney::StickTiltRight` |  | `Icons::Kenney::MoveBl` |  | `Icons::Kenney::MoveBr` |
|  | `Icons::Kenney::MoveBt` |  | `Icons::Kenney::MoveBtAlt` |  | `Icons::Kenney::MoveLb` |
|  | `Icons::Kenney::MoveLr` |  | `Icons::Kenney::MoveLrAlt` |  | `Icons::Kenney::MoveLt` |
|  | `Icons::Kenney::MoveRb` |  | `Icons::Kenney::MoveRl` |  | `Icons::Kenney::MoveRlAlt` |
|  | `Icons::Kenney::MoveRt` |  | `Icons::Kenney::MoveTb` |  | `Icons::Kenney::MoveTbAlt` |
|  | `Icons::Kenney::MoveTl` |  | `Icons::Kenney::MoveTr` |  | `Icons::Kenney::Github` |
|  | `Icons::Kenney::GithubAlt` |  | `Icons::Kenney::Twitter` |  | `Icons::Kenney::Facebook` |
|  | `Icons::Kenney::GooglePlus` |  | `Icons::Kenney::Youtube` |  | `Icons::Kenney::WeHeart` |
|  | `Icons::Kenney::Wolfcms` |  | `Icons::Kenney::WolfcmsAlt` | | |


---

# General Information

## Detecting Openplanet in ManiaScript

To detect Openplanet in ManiaScript, you check the value of `System.ExtraTool_Info` on the clientside. This will be a string containing "Openplanet" and its version.

Example functions:

```maniascript
#Include "TextLib" as TL

// Returns true if the user has Openplanet installed
Boolean HasOpenplanet() {
  return TL::RegexFind("^Openplanet ", System.ExtraTool_Info, "").count == 1;
}

// Returns the signature mode currently used in Openplanet
Text GetOpenplanetSignatureMode() {
  declare Text[] SignatureMode = TL::RegexMatch(" \\[([A-Z]*)\\]$", System.ExtraTool_Info, "");
  if (SignatureMode.count == 1) {
    return SignatureMode[0];
  }
  return "REGULAR";
}
```

The signature modes available with Openplanet by default are:

*   `OFFICIAL`: Only plugins shipped with Openplanet can run.
*   `REGULAR`: Only signed regular plugins can run.
*   `SCHOOL`: Only signed school mode and regular plugins can run.
*   `DEVMODE`: All signed and unsigned plugins can run.

Competition profiles can also be returned (e.g., `COMPETITION` if the TMWT competition profile is enabled).

The list of signature modes are "tiered," meaning that one signature mode allows its own set of plugins plus anything "above" it in the table below:

| Current / Define | OFFICIAL | REGULAR | SCHOOL | DEVMODE |
| :--------------- | :------- | :------ | :----- | :------ |
| Official         | ✅       | ❌      | ❌     | ❌      |
| Regular          | ✅       | ✅      | ❌     | ❌      |
| School           | ✅       | ✅      | ✅     | ❌      |
| Developer        | ✅       | ✅      | ✅     | ✅      |

> **Note:** This detection works only on the client where Openplanet is running. To check on the server if a client is running Openplanet, you need to send them a Manialink with the detection code and perform a network request/response.

---

## Temporarily disable Openplanet

You can temporarily disable Openplanet using the following steps:
1.  Start holding down the `Pause/Break` key on your keyboard. Do not release it yet.
2.  Click `Play` in Ubisoft Connect, the Epic Games Launcher, or Steam.
3.  When you see the game itself load (the window has opened), release the `Pause/Break` key.

If you don't have the `Pause/Break` key on your keyboard, you can also rename `dinput8.dll` in your game directory to something else (e.g., `dinput8.dll.bak`).

---

# Troubleshooting

Below are some common issues you might be having, and ways to solve them.

## The game doesn't start

You're likely missing the latest 64-bit version of the Visual Studio C++ runtime. **Do not skip this!** Don't assume you already have this installed on your system! If Openplanet doesn't work, this is very likely the cause. [Download it from here](https://aka.ms/vs/17/release/vc_redist.x64.exe).

Note that if you're trying to get Openplanet for TrackMania Turbo to work, you'll need to install the 32-bit version of the runtime, which you can [download here](https://aka.ms/vs/17/release/vc_redist.x86.exe).

After following the installer's instructions, you might have to restart your PC before it'll work.

## The game works but Openplanet doesn't start/can't be accessed

Almost all issues are caused by the following things - check these first:

*   **Did you start the game in offline mode?** Openplanet requires the game to connect to Ubisoft's servers during startup to check your access level and permissions. Ensure Ubisoft Connect is not in offline mode.
*   **Are you on a laptop and F3 doesn't seem to do anything?** Try pressing `Fn` and `F3` at the same time.
*   **Missing Visual Studio C++ runtime:** As mentioned above, this is the most common cause. Make sure you have the latest 64-bit version installed. [Download it from here](https://aka.ms/vs/17/release/vc_redist.x64.exe).
*   **Restart your computer**, especially right after installing the VS C++ runtime.
*   **Installation directory:** Openplanet needs to be installed in the same directory as the game executable. You can find the game's location by opening the Task Manager, right-clicking `Trackmania.exe`, and selecting "Open file location".

In the rare case that none of those apply to you, other causes can be:
*   Using an older unsupported version of Windows (e.g., Windows 7).
*   Interfering third-party applications like anti-virus, firewalls, or overlays (ReShade, MSI Afterburner, Overwolf, etc.). Try disabling them.
*   A corrupt installation of Openplanet.

### Further troubleshooting

First, check for an `OpenplanetHook.log` file in your Trackmania installation directory. A successful startup looks like this:

```log
[22:35:12] Finding libs path
[22:35:12] Updating PATH to add: 'D:\Games\Trackmania\Openplanet\Lib'
[22:35:12] Attaching DLL to: 'D:\Games\Trackmania\Trackmania.exe'
[22:35:12] Module handle: 00007FF9E2A50000
[22:35:14] DirectInput8Create
```

A failed startup could look like this (e.g., `error 126`):

```log
[22:36:05] Finding libs path
[22:36:05] Updating PATH to add: 'D:\Games\Trackmania\Openplanet\Lib'
[22:36:05] Attaching DLL to: 'D:\Games\Trackmania\Trackmania.exe'
[22:36:05] Failed to load Openplanet module, error 126
[22:36:05] Module handle: 0000000000000000
[22:36:05] DirectInput8Create
[22:36:05] Openplanet.dll is not loaded yet!
[22:36:05] Couldn't find DinputInit function!
```

Next, check your main Openplanet log file located at: `C:\Users\<Your Username>\OpenplanetNext\Openplanet.log` (folder name may vary, e.g., `Openplanet4` or `OpenplanetTurbo`). Look for obvious errors.

You can ask for additional help on the Openplanet Discord.

## Openplanet works on one of my Trackmania installations, but not on the other

If you have multiple Trackmania installations (e.g., Steam and Ubisoft Connect), updating can cause issues.
1.  Start the Trackmania installation where Openplanet doesn't work. An installer should pop up. If not, download the latest version manually.
2.  Follow the installer, but pay close attention to the installation path. Make sure it points to the correct Trackmania directory.
3.  Install the update and restart your game.

## Openplanet starts but plugins can't be installed

This is likely a folder permissions issue. If you see errors like `Unable to load plugin '...' because the zip file doesn't exist!` in your logs:
1.  In Windows Explorer, navigate to `C:\Users`.
2.  Right-click your user's directory and open its `Properties`.
3.  Go to the `Security` tab and ensure your user account has `Full control` over the directory.
4.  Restart Trackmania.

## Troubleshooting crashes

To troubleshoot crashes, download and install [this registry file](URL_TO_REGISTRY_FILE) to enable writing `.dmp` files for game crashes. After a crash, a `.dmp` file will be created in `C:\Users\Username\AppData\Local\CrashDumps\`.

> **NOTE:** Do not post `.dmp` files publicly! They may contain sensitive information. Only send them to Openplanet developers directly when you are asked to provide one.

## Compatibility

### Linux & Mac Compatibility
For information about compatibility on Linux (e.g., via Wine), check [this page](URL_TO_LINUX_PAGE). The guide for Mac should be similar. With Crossover, ensure you are using DXVK as the rendering engine.

### Game Compatibility
Openplanet is compatible with:
*   Trackmania (2020)
*   ManiaPlanet 4
*   TrackMania Turbo

### Reference: time-api

# Openplanet Time API Reference

Namespace: `Time`

## Properties

```
uint64 Time::Now        → Milliseconds since game started
int64  Time::Stamp      → Unix epoch timestamp in SECONDS
uint64 Time::FrameCount → Number of frames Openplanet has processed
```

## Time::Info Structure

Returned by `Time::Parse()` and `Time::ParseUTC()`. Fields:

| Field | Type | Description |
|-------|------|-------------|
| `year` | int | Full year (e.g., 2025) |
| `month` | int | 1-12 |
| `day` | int | 1-31 |
| `hour` | int | 0-23 |
| `minute` | int | 0-59 |
| `second` | int | 0-59 |
| `weekday` | int | 0=Sunday, 1=Monday, ..., 6=Saturday |
| `yearday` | int | 0-365 (day of year) |

## Functions

### Format string (strftime)

```angelscript
string Time::FormatString(const string&in format, int64 stamp = -1)
string Time::FormatStringUTC(const string&in format, int64 stamp = -1)
```

| Specifier | Output (example) |
|-----------|-----------------|
| `%Y` | 2025 |
| `%m` | 05 |
| `%d` | 26 |
| `%H` | 14 (24h) |
| `%I` | 02 (12h) |
| `%M` | 30 |
| `%S` | 45 |
| `%p` | AM/PM |
| `%A` | Monday (full weekday) |
| `%a` | Mon (abbreviated weekday) |
| `%B` | January (full month) |
| `%b` | Jan (abbreviated month) |
| `%c` | Mon May 26 14:30:45 2025 |
| `%x` | 05/26/2025 |
| `%X` | 14:30:45 |
| `%j` | 146 (day of year) |
| `%w` | 1 (weekday, 0=Sunday) |
| `%u` | 1 (weekday, 1=Monday) |

`stamp = -1` defaults to current time.

### Parse string to timestamp

```angelscript
int64 Time::ParseFormatString(const string&in format, const string&in stamp)
```

### Parse timestamp to Info

```angelscript
Time::Info Time::Parse(int64 stamp = -1)       // local time
Time::Info Time::ParseUTC(int64 stamp = -1)    // UTC
```

### Game time formatting

```angelscript
string Time::Format(uint64 time, bool fractions = true, bool forceMinutes = true, bool forceHours = false, bool short = false)
```

Formats game milliseconds to race time. Example: `Time::Format(61234)` → `"1:01.234"`.

## Common Patterns

```angelscript
// Current time as string
string now = Time::FormatString("%H:%M:%S", Time::Stamp);

// Today's date
string today = Time::FormatString("%Y-%m-%d", Time::Stamp);

// Parse an event date
int64 eventTs = Time::ParseFormatString("%Y-%m-%d %H:%M", "2025-06-01 18:00");

// Check if event is in the future
if (eventTs > Time::Stamp) { ... }

// Days until event
int64 diffSec = eventTs - Time::Stamp;
int days = int(diffSec / 86400);
int hours = int((diffSec % 86400) / 3600);
int minutes = int((diffSec % 3600) / 60);
```

### Reference: maniaplanet-feedback-extraction

