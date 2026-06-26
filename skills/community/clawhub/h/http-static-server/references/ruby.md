# Ruby HTTP Static Server

## ruby -run (Ruby 1.9.2+, recommended)

The simplest built-in option:

```bash
ruby -run -ehttpd . -p8000
```

Features:
- Directory listing: Yes
- No gem install needed
- Uses WEBrick under the hood

## WEBrick (explicit)

```bash
ruby -rwebrick -e'WEBrick::HTTPServer.new(:Port => 8000, :DocumentRoot => Dir.pwd).start'
```

Bind to all interfaces:

```bash
ruby -rwebrick -e'WEBrick::HTTPServer.new(:Port => 8000, :BindAddress => "0.0.0.0", :DocumentRoot => Dir.pwd).start'
```

Features:
- Directory listing: Yes
- Part of Ruby standard library
- Configurable via Ruby API

## adsf (A Dead Simple Fileserver)

Install:

```bash
gem install adsf
```

Run:

```bash
adsf -p 8000
```

Features:
- Directory listing: No
- Minimal and clean
- Uses Rack under the hood

## Sinatra

Install:

```bash
gem install sinatra
```

Run:

```bash
ruby -rsinatra -e'set :public_folder, "."; set :port, 8000'
```

Features:
- Directory listing: No
- Full Sinatra DSL available for customization
- Good for adding custom routes alongside static files
