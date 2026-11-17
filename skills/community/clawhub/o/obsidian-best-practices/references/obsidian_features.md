[[Introduction to Obsidian Sync|Obsidian Sync]] offers a headless client to sync vaults without using the desktop app. Useful for CI pipelines, agents, and automated workflows. Sync the latest changes or keep files continuously up to date.

Install [[Obsidian Headless]] **(open beta)** to interact with [[Introduction to Obsidian Sync|Obsidian Sync]] from the command line without the Obsidian desktop app. Headless Sync uses the same [[Security and privacy|encryption and privacy protections]] as the desktop app, including end-to-end encryption.

## Quick start

> [!error] Back up your data before you start
> 1. Always back up your data before you start in case anything unexpected happens.
> 2. Do not use *both* the desktop app Sync and Headless Sync on the same device, as it can cause data conflicts. Only use one sync method per device.

Install [[Obsidian Headless|Obsidian Headless]] **(open beta)**:

```shell
npm install -g obsidian-headless
```

You must have an active [[Plans and storage limits|Obsidian Sync subscription]].

```shell
# Login
ob login

# List your remote vaults
ob sync-list-remote

# Set up a vault for syncing
cd ~/vaults/my-vault
ob sync-setup --vault "My Vault"

# Run a one-time sync
ob sync

# Run continuous sync (watches for changes)
ob sync --continuous
```

## Commands

### `ob sync-list-remote`

List all remote vaults available to your account, including shared vaults.

### `ob sync-list-local`

List locally configured vaults and their paths.

### `ob sync-create-remote`

Create a new remote vault.

```
ob sync-create-remote --name "Vault Name" [--encryption <standard|e2ee>] [--password <password>] [--region <region>]
```

| Option | Description |
| --- | --- |
| `--name` | Vault name (required) |
| `--encryption` | `standard` for managed encryption, `e2ee` for end-to-end encryption |
| `--password` | End-to-end encryption password (prompted if omitted) |
| `--region` | Server [[Sync regions\|region]] (automatic if omitted) |

### `ob sync-setup`

Set up sync between a local vault and a remote vault.

```
ob sync-setup --vault <id-or-name> [--path <local-path>] [--password <password>] [--device-name <name>] [--config-dir <name>]
```

| Option | Description |
| --- | --- |
| `--vault` | Remote vault ID or name (required) |
| `--path` | Local directory (default: current directory) |
| `--password` | E2E encryption password (prompted if omitted) |
| `--device-name` | Device name shown in [[Version history\|sync version history]] |
| `--config-dir` | [[Configuration folder\|Config directory]] name (default: `.obsidian`) |

### `ob sync`

Run sync for a configured vault.

```
ob sync [--path <local-path>] [--continuous]
```

| Option | Description |
| --- | --- |
| `--path` | Local vault path (default: current directory) |
| `--continuous` | Run continuously, watching for changes |

### `ob sync-config`

View or change [[Sync settings and selective syncing|sync settings]] for a vault. Run with no options to display the current configuration.

```
ob sync-config [--path <local-path>] [options]
```

| Option                | Description                                                                                                                                                                                                    |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--path`              | Local vault path (default: current directory)                                                                                                                                                                  |
| `--mode`              | Sync mode: `bidirectional` (default), `pull-only` (only download, ignore local changes), or `mirror-remote` (only download, revert local changes)                                                              |
| `--conflict-strategy` | `merge` or `conflict`                                                                                                                                                                                          |
| `--file-types`        | Attachment types to sync: `image`, `audio`, `video`, `pdf`, `unsupported` (comma-separated, empty to clear)                                                                                                    |
| `--configs`           | Config categories to sync: `app`, `appearance`, `appearance-data`, `hotkey`, `core-plugin`, `core-plugin-data`, `community-plugin`, `community-plugin-data` (comma-separated, empty to disable config syncing) |
| `--excluded-folders`  | Folders to exclude (comma-separated, empty to clear)                                                                                                                                                           |
| `--device-name`       | Device name to identify this client in the sync version history                                                                                                                                                |
| `--config-dir`        | Config directory name (default: `.obsidian`)                                                                                                                                                                   |

### `ob sync-status`

Show sync status and configuration for a vault.

```
ob sync-status [--path <local-path>]
```

### `ob sync-unlink`

Disconnect a vault from sync and remove stored credentials.

```
ob sync-unlink [--path <local-path>]
```

## Native modules

Obsidian Headless includes a prebuilt native addon for setting file creation time (birthtime) on Windows and macOS. This preserves original creation timestamps when downloading files from the server.

The addon targets N-API version 3, so the compiled binaries are ABI-stable and work across Node.js versions without recompilation.

On Linux, birthtime is not supported — the addon is not included and sync operates normally without it.

Prebuilt binaries are included for:

- `win32-x64`
- `win32-arm64`
- `win32-ia32`
- `darwin-x64`
- `darwin-arm64`


---

## Sharpen your thinking.

The free and flexible app for your private thoughts.

[Get Obsidian for Windows](https://obsidian.md/download) [More platforms](https://obsidian.md/download)

## Spark ideas.

From personal notes to journaling, knowledge bases, and project management, Obsidian gives you the tools to come up with ideas and organize them.

Links

Create connections between your notes. Link anything and everything — ideas, people, places, books, and beyond. Invent your own personal Wikipedia.

Graph

Visualize the relationships between your notes. Find hidden patterns in your thinking through a visually engaging and interactive graph.

<svg viewBox="0 0 522 472" fill="none" xmlns="http://www.w3.org/2000/svg"><text x="90" y="305" fill="currentColor">Philosophy</text> <text x="250" y="180" fill="currentColor">Books</text> <text x="230" y="300" fill="currentColor">René Descartes</text></svg>[

Canvas

An infinite space to research, brainstorm, diagram, and lay out your ideas. Canvas is a limitless playground for your mind. Learn more.

](https://obsidian.md/canvas)[

Plugins

Build your ideal thinking space. With thousands of plugins and our open API, it’s easy to tailor Obsidian to fit your personal workflow. Learn more.

](https://community.obsidian.md/)

## Sync securely.

Access your notes on any device, secured with end-to-end encryption. [Learn more.](https://obsidian.md/sync)

**Version history.** Easily track changes between revisions, with one year of version history for every note.

**Collaboration.** Work with your team on shared files without compromising your private data.

**Fine-grained control.** Decide which files and preferences you want to sync to which devices.

## Publish instantly.

Turn your notes into an online wiki, knowledge base, documentation, or digital garden. [Learn more.](https://obsidian.md/publish)

Seamless editing

Publish your notes instantly from the Obsidian app, and make it easy for readers to explore your web of ideas.

Customization

Control the look and feel of your site with themes, custom domains, password protection, and more.

Optimized for performance

Obsidian Publish sites are fast, mobile-friendly, and optimized for SEO, no configuration required.

![Example of Obsidian Help site powered by Obsidian Publish](https://obsidian.md/images/publish-example-dark.png)

Explore the [Obsidian Help](https://obsidian.md/help/) site, powered by [Obsidian Publish](https://obsidian.md/publish).

## It’s your time to shine.

[Get Obsidian](https://obsidian.md/download)


---

## Flexible and intuitive

Canvas is packed with functionality. This collection of tips will help you discover how you can use Canvas to its fullest.

<video controls="" src="https://obsidian.md/videos/01-create-canvas-from-ribbon.mp4"></video>

Create a canvas (3 tips)

From ribbon

Create in folder

From command palette

Card types (6 tips)

Text card

Markdown file embed

Image & video

PDF file

Webpage

Nested canvas

Create cards (10 tips)

Click toolbar to create text card

Click toolbar to create note card

Double click to create

Drag from toolbar to create

Right click to create

Connect and create

Paste text to create

Create website by pasting URL

Create YouTube embed

Bulk create cards from folder

Modify cards (7 tips)

Swap file for card

Convert text card to file

Narrow down to headings

Change URL of webpage card

Smart auto-resize cards

Manually resize cards

Delete card

Connections (7 tips)

Connect two cards

Add label to connection

Remove label from connection

Add color to connection

Connect to a group

Update connection target

Delete connection

Pan and scroll (4 tips)

Scroll up and down

Hold Shift to scroll left and right

Hold Space and drag to pan

Hold middle or right click to pan

Zoom (6 tips)

Hold Ctrl or Cmd and scroll

Hold Space and scroll

Zoom to fit all cards

Zoom to fit all cards with hotkey

Zoom to selection

Zoom to selection with hotkey

Select cards (5 tips)

Select a single card

Drag to select multiple cards

Add or remove one card from selection

Add or remove multiple cards from selection

Select all cards in the canvas

Arrange cards (10 tips)

Move cards

Duplicate cards

Move card along an axis

Snap card to grid

Snap card to align with other cards

Move card without aligning

Align selected cards on one end

Align selected cards on both ends

Bulk arrange selected cards

Spread selected cards evenly

Group cards (6 tips)

Right click to create group

Create group of a certain size

Create group around cards

Rename a group

Select a group

Nest groups

Colors (6 tips)

Add color to card

Add color to group

Add color to connection

Pick a custom color

Remove color

Export (2 tips)

Export what you see to image

Export entire canvas to image

## Community demos

Explore how members of the Obsidian community are using Canvas for the personal life and at work.

![](https://www.youtube.com/watch?v=rPescoJzcFA)
![](https://www.youtube.com/watch?v=HFK3D7zeyTA)
![](https://www.youtube.com/watch?v=eHI-Szjpafk)
![](https://www.youtube.com/watch?v=vLBd_ADeKIw)


---

Welcome to the official Obsidian Help site, where you can find tips and guides on how to use [Obsidian](https://obsidian.md). For API documentation visit the [Obsidian Developer Docs](https://docs.obsidian.md/).

## Get started

Learn the basics of note-taking with Obsidian:

1. [[Download and install Obsidian]]
2. [[Create a vault]]
3. [[Create your first note]]
4. [[Link notes]]
5. [[Import notes]]
6. [[Sync your notes across devices]]

## Extend Obsidian

With thousands of plugins and themes, you can shape Obsidian to fit your way of thinking.

- [[Core plugins]]
	- Choose which built-in features of Obsidian you want to turn on or off.
- [[Community plugins]]
	- Enable more workflows and capabilities with features built by Obsidian users.
- [[Themes]]
	- Customize the look and feel of Obsidian with community-made color schemes.
- [[CSS snippets]]
	- Make small changes to the interface on top of your Obsidian theme.
- [[Introduction to Obsidian Web Clipper|Web Clipper]]
	- Highlight web pages and save content to Obsidian using our browser extension.
- [[Obsidian CLI]]
	- Control Obsidian from your terminal using the command line interface.

## Add-on services

- [[Introduction to Obsidian Sync|Obsidian Sync]]
	- A safe and secure way to synchronize your notes across any device and OS.
- [[Introduction to Obsidian Publish|Obsidian Publish]]
	- Publish your notes as a wiki, knowledge base, documentation, or digital garden.

## Contribute

If you find any mistakes or missing information on this site, you can contribute improvements and translations via [the GitHub repo](https://github.com/obsidianmd/obsidian-docs/).

If you want to contribute to Obsidian financially, consider a [[Catalyst license]] which offers early access to beta versions, or a [[Commercial license]] to show your organization's support.

See the [[Credits]] to get to know all the amazing people who make Obsidian possible.


---

