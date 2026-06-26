# Perl HTTP Static Server

## Plack (recommended)

Install:

```bash
cpan Plack
```

Run:

```bash
plackup -MPlack::App::Directory -e 'Plack::App::Directory->new(root=>".");' -p 8000
```

Features:
- Directory listing: Yes
- Middleware ecosystem (Plack::Middleware::*)
- PSGI-compatible
- Multiple server backends

## HTTP::Server::Brick

Install:

```bash
cpan HTTP::Server::Brick
```

Run:

```bash
perl -MHTTP::Server::Brick -e '$s=HTTP::Server::Brick->new(port=>8000); $s->mount("/"=>{path=>"."}); $s->start'
```

Features:
- Directory listing: Yes
- Simple API
- Mountable paths

## Mojolicious::Lite

Install:

```bash
cpan Mojolicious::Lite
```

Run:

```bash
perl -MMojolicious::Lite -MCwd -e 'app->static->paths->[0]=getcwd; app->start' daemon -l http://*:8000
```

Features:
- Directory listing: No
- Full web framework available
- WebSocket support
- Hot reload in development mode
- Good for adding dynamic routes alongside static files
