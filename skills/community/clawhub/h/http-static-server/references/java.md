# Java HTTP Static Server

## jwebserver (Java 18+, recommended)

The simplest option, built into JDK 18+:

```bash
jwebserver -d . -b 0.0.0.0 -p 8000
```

Serve with default settings (port 8000, localhost only):

```bash
jwebserver
```

Custom directory:

```bash
jwebserver -d /path/to/dir -p 8000
```

Features:
- Directory listing: Yes
- Built into JDK 18+
- No dependencies needed
- Verbose output: `-o verbose`

## jdk.httpserver module

```bash
java -m jdk.httpserver -d . -b 0.0.0.0 -p 8000
```

This is equivalent to `jwebserver` but invoked via the module system.

## Inline Java (any version with JDK)

For older Java versions, create `Server.java`:

```java
import com.sun.net.httpserver.*;
import java.net.InetSocketAddress;
import java.nio.file.*;

public class Server {
    public static void main(String[] args) throws Exception {
        var server = HttpServer.create(new InetSocketAddress(8000), 0);
        server.createContext("/", exchange -> {
            var path = Path.of("." + exchange.getRequestURI().getPath());
            var bytes = Files.readAllBytes(path);
            exchange.sendResponseHeaders(200, bytes.length);
            exchange.getResponseBody().write(bytes);
            exchange.close();
        });
        server.start();
    }
}
```

```bash
java Server.java
```

Note: `jwebserver` is the recommended approach for Java 18+.
