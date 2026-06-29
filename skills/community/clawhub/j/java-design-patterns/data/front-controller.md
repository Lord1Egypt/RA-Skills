[Skip to main content](https://java-design-patterns.com/patterns/front-controller/#main-content)

# Front Controller Pattern in Java: Centralizing Web Request Handling

ArchitecturalArchitectureDecouplingEnterprise patternsLayered architectureWeb developmentAbout 3 min

* * *

## [Also known as](https://java-design-patterns.com/patterns/front-controller/\#also-known-as)

- Centralized Request Handling

## [Intent of Front Controller Design Pattern](https://java-design-patterns.com/patterns/front-controller/\#intent-of-front-controller-design-pattern)

The Front Controller design pattern aims to provide a centralized entry point for handling all incoming web requests. This pattern ensures consistent and efficient request routing and management across a Java web application.

## [Detailed Explanation of Front Controller Pattern with Real-World Examples](https://java-design-patterns.com/patterns/front-controller/\#detailed-explanation-of-front-controller-pattern-with-real-world-examples)

Real-world example

> In a real-world scenario, a front desk in a hotel serves as the centralized request handling point, similar to how the Front Controller design pattern functions in web application architecture. This desk acts as the "front controller" of the hotel, responsible for receiving all inquiries, from room service orders to maintenance requests. The receptionist assesses each request and routes it to the appropriate department—housekeeping, the kitchen, or maintenance. This system centralizes request handling, ensuring that guest needs are addressed efficiently and consistently, similar to how a Front Controller in a software application manages all incoming requests and delegates them to specific handlers.

In plain words

> The Front Controller design pattern centralizes incoming web requests into a single handling point, allowing consistent processing and delegation across an application.

Wikipedia says

> The front controller software design pattern is listed in several pattern catalogs and is related to the design of web applications. It is "a controller that handles all requests for a website", which is a useful structure for web application developers to achieve flexibility and reuse without code redundancy.

Architecture diagram

![Front Controller Architecture Diagram](https://java-design-patterns.com/assets/img/front-controller-architecture-diagram.9a7632b7.png)

## [Programmatic Example of Front Controller Pattern in Java](https://java-design-patterns.com/patterns/front-controller/\#programmatic-example-of-front-controller-pattern-in-java)

The Front Controller design pattern is a pattern that provides a centralized entry point for handling all requests in a web application. It ensures that request handling is managed consistently and efficiently across an application.

In the provided code, we can see an example of the Front Controller pattern in the `App`, `FrontController` and `Dispatcher` classes.

The `App` class is the entry point of the application. It creates an instance of `FrontController` and uses it to handle various requests.

```java
public class App {

  public static void main(String[] args) {
    var controller = new FrontController();
    controller.handleRequest("Archer");
    controller.handleRequest("Catapult");
    controller.handleRequest("foobar");
  }
}
```

The `FrontController` class is the front controller in this example. It handles all requests and delegates them to the `Dispatcher`.

```java
public class FrontController {

    private final Dispatcher dispatcher;

    public FrontController() {
        this.dispatcher = new Dispatcher();
    }

    public void handleRequest(String request) {
        dispatcher.dispatch(request);
    }
}
```

The `Dispatcher` class is responsible for handling the dispatching of requests to the appropriate command. It retrieves the corresponding command based on the request and invokes the command's process method to handle the business logic.

```java
public class Dispatcher {

  public void dispatch(String request) {
    var command = getCommand(request);
    command.process();
  }

  Command getCommand(String request) {
    var commandClass = getCommandClass(request);
    try {
      return (Command) commandClass.getDeclaredConstructor().newInstance();
    } catch (Exception e) {
      throw new ApplicationException(e);
    }
  }

  static Class<?> getCommandClass(String request) {
    try {
      return Class.forName("com.iluwatar.front.controller." + request + "Command");
    } catch (ClassNotFoundException e) {
      return UnknownCommand.class;
    }
  }
}
```

In this example, when a request is received, the `FrontController` delegates the request to the `Dispatcher`, which creates a command object based on the request and calls its `process` method. The command object is responsible for handling the request and rendering the appropriate view.

This is a basic example of the Front Controller pattern, where all requests are handled by a single controller and dispatcher, ensuring consistent and efficient request handling.

## [When to Use the Front Controller Pattern in Java](https://java-design-patterns.com/patterns/front-controller/\#when-to-use-the-front-controller-pattern-in-java)

- The Front Controller design pattern is particularly useful for Java web applications that require a centralized mechanism for request handling.
- Systems that need a common processing point for all requests to perform tasks such as authentication, logging, and routing.

## [Real-World Applications of Front Controller Pattern in Java](https://java-design-patterns.com/patterns/front-controller/\#real-world-applications-of-front-controller-pattern-in-java)

- [Apache Struts](https://struts.apache.org/)
- Java web frameworks like Spring MVC and JavaServer Faces (JSF) implement the Front Controller pattern through their central dispatcher servlet, which manages web requests and delegates responsibilities.

## [Benefits and Trade-offs of Front Controller Pattern](https://java-design-patterns.com/patterns/front-controller/\#benefits-and-trade-offs-of-front-controller-pattern)

Benefits:

- The main benefit of the Front Controller design pattern is the centralization of request handling, which simplifies maintenance and ensures consistent behavior across the application.
- Eases the integration of services like security and user session management.
- Facilitates common behavior like routing, logging, and authentication across requests.

Trade-offs:

- Can become a bottleneck if not properly managed.
- Increases complexity in the dispatcher controller, requiring careful design to avoid tight coupling.

## [Related Java Design Patterns](https://java-design-patterns.com/patterns/front-controller/\#related-java-design-patterns)

- [Page Controller](https://java-design-patterns.com/patterns/page-controller/): Front Controller can delegate requests to Page Controllers, which handle specific page requests. This division supports the Single Responsibility Principle.
- [Model-View-Controller (MVC)](https://java-design-patterns.com/patterns/model-view-controller/): Front Controller acts as the controller, managing the flow between model and view.
- [Command](https://java-design-patterns.com/patterns/command/): Can be used to encapsulate a request as an object, which the Front Controller can manipulate and delegate.

## [References and Credits](https://java-design-patterns.com/patterns/front-controller/\#references-and-credits)

- [J2EE Design Patterns](https://amzn.to/4dpzgmx)
- [Patterns of Enterprise Application Architecture](https://amzn.to/3WfKBPR)