---
name: "actor-model"
description: "Actor Model Actor 模型 -- Concurrency设计模式。Explore the Actor Model pattern in Java with real-world examples and practical implementation. Learn how to build scalable, message-driven systems usi"
url: "https://java-design-patterns.com/patterns/actor-model/"
category: "concurrency"
tags: [Actor Model, Distributed Systems, Asynchronous, Isolation, Messaging, Concurrency]
---

# Actor Model Actor 模型模式

> 官方文档: https://java-design-patterns.com/patterns/actor-model/
> 分类: Concurrency (concurrency)
> 标签: Actor Model, Distributed Systems, Asynchronous, Isolation, Messaging, Concurrency

ConcurrencyConcurrencyMessagingIsolationAsynchronousDistributed SystemsActor ModelAbout 2 min

* * *

## [Also Known As](https://java-design-patterns.com/patterns/actor-model/#also-known-as)

- Message-passing concurrency
- Actor-based concurrency

* * *

## [Intent of Actor Model Pattern](https://java-design-patterns.com/patterns/actor-model/#intent-of-actor-model-pattern)

The Actor Model pattern enables the construction of highly concurrent, distributed, and fault-tolerant systems by using isolated components (actors) that interact exclusively through asynchronous message passing.

* * *

## [Detailed Explanation of Actor Model Pattern with Real-World Examples](https://java-design-patterns.com/patterns/actor-model/#detailed-explanation-of-actor-model-pattern-with-real-world-examples)

### [📦 Real-world Example](https://java-design-patterns.com/patterns/actor-model/#%F0%9F%93%A6-real-world-example)

Imagine a customer service system:

- Each **customer support agent** is an **actor**.
- Customers **send questions (messages)** to agents.
- Each agent handles one request at a time and can **respond asynchronously** without interfering with other agents.

* * *

### [🧠 In Plain Words](https://java-design-patterns.com/patterns/actor-model/#%F0%9F%A7%A0-in-plain-words)

> "Actors are like independent workers that never share memory and only communicate through messages."

* * *

### [📖 Wikipedia Says](https://java-design-patterns.com/patterns/actor-model/#%F0%9F%93%96-wikipedia-says)

> [Actor model](https://en.wikipedia.org/wiki/Actor_model) is a mathematical model of concurrent computation that treats "actors" as the universal primitives of concurrent computation.

* * *

### [🧹 Architecture Diagram](https://java-design-patterns.com/patterns/actor-model/#%F0%9F%A7%B9-architecture-diagram)

![UML Class Diagram](https://java-design-patterns.com/assets/img/Actor_Model_UML_Class_Diagram.818a6b21.png)

* * *

## [Programmatic Example of Actor Model Pattern in Java](https://java-design-patterns.com/patterns/actor-model/#programmatic-example-of-actor-model-pattern-in-java)

### [Actor.java](https://java-design-patterns.com/patterns/actor-model/#actor-java)

```java
public abstract class Actor implements Runnable {

    @Setter @Getter private String actorId;
    private final BlockingQueue<Message> mailbox = new LinkedBlockingQueue<>();
    private volatile boolean active = true;

    public void send(Message message) {
        mailbox.add(message);
    }

    public void stop() {
        active = false;
    }

    @Override
    public void run() {

    }

    protected abstract void onReceive(Message message);
}
```

### [Message.java](https://java-design-patterns.com/patterns/actor-model/#message-java)

```java

@AllArgsConstructor
@Getter
@Setter
public class Message {
    private final String content;
    private final String senderId;
}
```

### [ActorSystem.java](https://java-design-patterns.com/patterns/actor-model/#actorsystem-java)

```java
public class ActorSystem {
    public void startActor(Actor actor) {
        String actorId = "actor-" + idCounter.incrementAndGet(); // Generate a new and unique ID
        actor.setActorId(actorId); // assign the actor it's ID
        actorRegister.put(actorId, actor); // Register and save the actor with it's ID
        executor.submit(actor); // Run the actor in a thread
    }
    public Actor getActorById(String actorId) {
        return actorRegister.get(actorId); //  Find by Id
    }

    public void shutdown() {
        executor.shutdownNow(); // Stop all threads
    }
}
```

### [App.java](https://java-design-patterns.com/patterns/actor-model/#app-java)

```java
public class App {
  public static void main(String[] args) {
    ActorSystem system = new ActorSystem();
      Actor srijan = new ExampleActor(system);
      Actor ansh = new ExampleActor2(system);

      system.startActor(srijan);
      system.startActor(ansh);
      ansh.send(new Message("Hello ansh", srijan.getActorId()));
      srijan.send(new Message("Hello srijan!", ansh.getActorId()));

      Thread.sleep(1000); // Give time for messages to process

      srijan.stop(); // Stop the actor gracefully
      ansh.stop();
      system.shutdown(); // Stop the actor system
  }
}
```

* * *

## [When to Use the Actor Model Pattern in Java](https://java-design-patterns.com/patterns/actor-model/#when-to-use-the-actor-model-pattern-in-java)

- When building **concurrent or distributed systems**
- When you want **no shared mutable state**
- When you need **asynchronous, message-driven communication**
- When components should be **isolated and loosely coupled**

* * *

## [Actor Model Pattern Java Tutorials](https://java-design-patterns.com/patterns/actor-model/#actor-model-pattern-java-tutorials)

- [Baeldung – Akka with Java](https://www.baeldung.com/java-akka)
- [Vaughn Vernon – Reactive Messaging Patterns](https://vaughnvernon.co/?p=1143)

* * *

## [Real-World Applications of Actor Model Pattern in Java](https://java-design-patterns.com/patterns/actor-model/#real-world-applications-of-actor-model-pattern-in-java)

- [Akka Framework](https://akka.io/)
- [Erlang and Elixir concurrency](https://www.erlang.org/)
- [Microsoft Orleans](https://learn.microsoft.com/en-us/dotnet/orleans/)
- JVM-based game engines and simulators

* * *

## [Benefits and Trade-offs of Actor Model Pattern](https://java-design-patterns.com/patterns/actor-model/#benefits-and-trade-offs-of-actor-model-pattern)

### [✅ Benefits](https://java-design-patterns.com/patterns/actor-model/#%E2%9C%85-benefits)

- High concurrency support
- Easy scaling across threads or machines
- Fault isolation and recovery
- Message ordering within actors

### [⚠️ Trade-offs](https://java-design-patterns.com/patterns/actor-model/#%E2%9A%A0%EF%B8%8F-trade-offs)

- Harder to debug due to asynchronous behavior
- Slight performance overhead due to message queues
- More complex to design than simple method calls

* * *

## [Related Java Design Patterns](https://java-design-patterns.com/patterns/actor-model/#related-java-design-patterns)

- [Command Pattern](https://java-design-patterns.com/patterns/command)
- [Mediator Pattern](https://java-design-patterns.com/patterns/mediator)
- [Event-Driven Architecture](https://java-design-patterns.com/patterns/event-driven-architecture)
- [Observer Pattern](https://java-design-patterns.com/patterns/observer)

* * *

## [References and Credits](https://java-design-patterns.com/patterns/actor-model/#references-and-credits)

- _Programming Erlang_, Joe Armstrong
- _Reactive Design Patterns_, Roland Kuhn
- _The Actor Model in 10 Minutes_, [InfoQ Article](https://www.infoq.com/articles/actor-model/)
- [Akka Documentation](https://doc.akka.io/docs/akka/current/index.html)

giscus

#### 0 reactions

#### 0 comments

WritePreview

[Styling with Markdown is supported](https://guides.github.com/features/mastering-markdown/ "Styling with Markdown is supported")

[Sign in with GitHub](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjava-design-patterns.com%2Fpatterns%2Factor-model%2F)
