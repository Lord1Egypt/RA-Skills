# Docker device access

`discover` receives `/dev` as a read-only bind mount solely to list stable
serial symlinks. It does not receive Docker `--device` access and cannot open
or control a printer.

`inspect`, `sd-files`, `record`, `home`, `send`, and `sd-print-monitor` require
an explicit path below `/dev/serial/by-id/`. The wrapper passes that exact path
through Docker `--device` and adds only that device's numeric group ID. It does
not pass the whole host device tree. Keep the printer connected through a
data-capable USB cable and ensure no other host program has claimed the serial
port.

`inspect`, `sd-files`, and `record` only read printer state. `home`, `send`,
and `sd-print-monitor` change physical printer state and require the operation-
specific confirmation flags plus direct current-turn approval. The SD monitor
also needs an operator at the machine and stops the selected SD job after its
observation window.

The default baud rate is 115200. Use `M115` from inspection to identify the
firmware before assuming that a setting or report command exists.
