# Stock macOS Apache Layout

On modern macOS, the built-in Apache is still the simplest base for a local PHP staging server.

Important paths:

- binary: `/usr/sbin/httpd`
- control: `apachectl`
- main config: `/etc/apache2/httpd.conf`
- extra vhosts: `/etc/apache2/extra/httpd-vhosts.conf`
- logs: `/private/var/log/apache2/`

Important defaults:

- vhosts are typically commented out by default
- Apache runs as the stock macOS service, not a Homebrew service
- PHP from Homebrew can be loaded with:
  - `/opt/homebrew/opt/php/lib/httpd/modules/libphp.so`

For local development, the common pattern is:

- enable PHP module
- enable vhosts
- create one `.test` or `.local` host per project
- keep MariaDB bound to localhost
