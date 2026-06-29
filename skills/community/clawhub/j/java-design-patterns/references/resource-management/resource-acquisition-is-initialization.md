---
name: "resource-acquisition-is-initialization"
description: "Resource Acquisition Is Initialization in Java: Ensuring Safe Resource Management RAII -- Resource management设计模式。Discover how the RAII (Resource Acquisition Is Initialization) pattern can streamline resource management in Java. Learn to implement RAII with practi"
url: "https://java-design-patterns.com/patterns/resource-acquisition-is-initialization/"
category: "resource-management"
tags: [Resource management, Memory management, Encapsulation]
---

# Resource Acquisition Is Initialization in Java: Ensuring Safe Resource Management RAII模式

> 官方文档: https://java-design-patterns.com/patterns/resource-acquisition-is-initialization/
> 分类: Resource management (resource-management)
> 标签: Resource management, Memory management, Encapsulation

Resource managementEncapsulationMemory managementResource managementAbout 3 min

* * *

## [Also known as](https://java-design-patterns.com/patterns/resource-acquisition-is-initialization/#also-known-as)

- RAII
- Scope-based Resource Management

## [Intent of Resource Acquisition Is Initialization Design Pattern](https://java-design-patterns.com/patterns/resource-acquisition-is-initialization/#intent-of-resource-acquisition-is-initialization-design-pattern)

Ensure efficient Java resource management by tying the resource lifecycle to object lifetime, utilizing the RAII pattern.

## [Detailed Explanation of Resource Acquisition Is Initialization Pattern with Real-World Examples](https://java-design-patterns.com/patterns/resource-acquisition-is-initialization/#detailed-explanation-of-resource-acquisition-is-initialization-pattern-with-real-world-examples)

Real-world example

> In a car rental service, each car represents a resource. Using the RAII pattern, when a customer rents a car (acquires the resource), the car is marked as rented. When the customer returns the car (the object goes out of scope), the car is automatically made available for the next customer. This ensures that cars are properly managed and available without manual intervention for checking availability or returns.

In plain words

> The RAII pattern in Java allows for exception-safe resource management, ensuring robust handling of critical resources.

Wikipedia says

> Resource acquisition is initialization (RAII) is a programming idiom used in several object-oriented, statically typed programming languages to describe a particular language behavior. Resource allocation (or acquisition) is done during object creation (specifically initialization), by the constructor, while resource deallocation (release) is done during object destruction (specifically finalization), by the destructor.

Sequence diagram

![Resource Acquisition Is Initialization sequence diagram](https://java-design-patterns.com/assets/img/raii-sequence-diagram.fc3d918b.png)

## [Programmatic Example of RAII Pattern in Java](https://java-design-patterns.com/patterns/resource-acquisition-is-initialization/#programmatic-example-of-raii-pattern-in-java)

The RAII pattern is a common idiom used in software design where the acquisition of a resource is done during object creation (initialization), and the release of the resource is done during object destruction. This pattern is particularly useful in dealing with resource leaks and is critical in writing exception-safe code in C++. In Java, RAII is achieved with try-with-resources statement and interfaces `java.io.Closeable` and `AutoCloseable`.

```java
// This is an example of a resource class that implements the AutoCloseable interface.
// The resource is acquired in the constructor and released in the close method.

@Slf4j
public class SlidingDoor implements AutoCloseable {

  public SlidingDoor() {
    LOGGER.info("Sliding door opens."); // Resource acquisition is done here
  }

  @Override
  public void close() {
    LOGGER.info("Sliding door closes."); // Resource release is done here
  }
}
```

In the above code, `SlidingDoor` is a resource that implements the `AutoCloseable` interface. The resource (in this case, a door) is "acquired" in the constructor (the door is opened), and "released" in the `close` method (the door is closed).

```java
// This is another example of a resource class that implements the Closeable interface.
// The resource is acquired in the constructor and released in the close method.

@Slf4j
public class TreasureChest implements Closeable {

  public TreasureChest() {
    LOGGER.info("Treasure chest opens."); // Resource acquisition is done here
  }

  @Override
  public void close() {
    LOGGER.info("Treasure chest closes."); // Resource release is done here
  }
}
```

Similarly, `TreasureChest` is another resource that implements the `Closeable` interface. The resource (a treasure chest) is "acquired" in the constructor (the chest is opened), and "released" in the `close` method (the chest is closed).

```java
// This is an example of how to use the RAII pattern in Java using the try-with-resources statement.

@Slf4j
public class App {

  public static void main(String[] args) {

    try (var ignored = new SlidingDoor()) {
      LOGGER.info("Walking in.");
    }

    try (var ignored = new TreasureChest()) {
      LOGGER.info("Looting contents.");
    }
  }
}
```

In the `main` method of the `App` class, we see the RAII pattern in action. The `try-with-resources` statement is used to ensure that each resource is closed at the end of the statement. This is where the `AutoCloseable` or `Closeable` interfaces come into play. When the `try` block is exited (either normally or via an exception), the `close` method of the resource is automatically called, thus ensuring the resource is properly released.

The console output:

```
10:07:14.833 [main] INFO com.iluwatar.resource.acquisition.is.initialization.SlidingDoor -- Sliding door opens.
10:07:14.835 [main] INFO com.iluwatar.resource.acquisition.is.initialization.App -- Walking in.
10:07:14.835 [main] INFO com.iluwatar.resource.acquisition.is.initialization.SlidingDoor -- Sliding door closes.
10:07:14.835 [main] INFO com.iluwatar.resource.acquisition.is.initialization.TreasureChest -- Treasure chest opens.
10:07:14.835 [main] INFO com.iluwatar.resource.acquisition.is.initialization.App -- Looting contents.
10:07:14.835 [main] INFO com.iluwatar.resource.acquisition.is.initialization.TreasureChest -- Treasure chest closes.
```

## [When to Use the Resource Acquisition Is Initialization Pattern in Java](https://java-design-patterns.com/patterns/resource-acquisition-is-initialization/#when-to-use-the-resource-acquisition-is-initialization-pattern-in-java)

- Implement RAII in Java applications to manage essential resources such as file handles, network connections, and memory seamlessly.
- Suitable in environments where deterministic resource management is crucial, such as real-time systems or applications with strict resource constraints.

## [Real-World Applications of RAII Pattern in Java](https://java-design-patterns.com/patterns/resource-acquisition-is-initialization/#real-world-applications-of-raii-pattern-in-java)

- Java `try-with-resources` statement: Ensures that resources are closed automatically at the end of the statement.
- Database connections: Using connection pools where the connection is obtained at the beginning of a scope and released at the end.
- File I/O: Automatically closing files using `try-with-resources`.

## [Benefits and Trade-offs of Resource Acquisition Is Initialization Pattern](https://java-design-patterns.com/patterns/resource-acquisition-is-initialization/#benefits-and-trade-offs-of-resource-acquisition-is-initialization-pattern)

Benefits:

- Automatic and deterministic resource management.
- Reduces the likelihood of resource leaks.
- Enhances code readability and maintainability by clearly defining the scope of resource usage.

Trade-offs:

- May introduce complexity in understanding object lifetimes.
- Requires careful design to ensure all resources are correctly encapsulated.

## [Related Java Design Patterns](https://java-design-patterns.com/patterns/resource-acquisition-is-initialization/#related-java-design-patterns)

- [Object Pool](https://java-design-patterns.com/patterns/object-pool/): Manages a pool of reusable objects to optimize resource allocation and performance, often used for resources that are expensive to create and manage.

## [References and Credits](https://java-design-patterns.com/patterns/resource-acquisition-is-initialization/#references-and-credits)

- [Effective Java](https://amzn.to/4cGk2Jz)
- [Design Patterns: Elements of Reusable Object-Oriented Software](https://amzn.to/3w0pvKI)
- [Resource acquisition is initialization](https://en.wikipedia.org/wiki/Resource_acquisition_is_initialization)
