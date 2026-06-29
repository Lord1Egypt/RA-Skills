[Skip to main content](https://java-design-patterns.com/patterns/monad/#main-content)

# Monad Pattern in Java: Mastering Functional Programming Paradigms

FunctionalAbstractionAccumulationDecouplingEncapsulationFunctional decompositionGenericIdiomInstantiationInterfaceLayered architectureObject compositionAbout 3 min

* * *

## [Also known as](https://java-design-patterns.com/patterns/monad/\#also-known-as)

- Computation Wrapper
- Monadic Interface

## [Intent of Monad Design Pattern](https://java-design-patterns.com/patterns/monad/\#intent-of-monad-design-pattern)

The Monad design pattern in Java provides a mechanism for encapsulating computations or side effects, enabling the chaining of operations while managing context and data flow in a side-effect-free manner.

## [Detailed Explanation of Monad Pattern with Real-World Examples](https://java-design-patterns.com/patterns/monad/\#detailed-explanation-of-monad-pattern-with-real-world-examples)

Real-world example

> Consider a real-world example of a monad in Java with a restaurant meal ordering process. This encapsulation and chaining allow for a clean, error-managed progression, similar to how monads handle data and operations in functional programming. In this scenario, each step of selecting a dish, adding sides, and choosing a drink can be thought of as a monadic operation. Each operation encapsulates the current state of the order (e.g., main dish chosen) and allows for the next choice (e.g., selecting a side) without exposing the complexity of the entire order's details to the customer.
>
> Just like in a functional monad, if any step fails (like an unavailable dish), the entire process can be halted or redirected without throwing exceptions, maintaining a smooth flow. This encapsulation and chaining allow for a clean, error-managed progression from choosing the main dish to completing the full meal order, akin to how monads handle data and operations in functional programming. This approach ensures a consistent experience, where every choice builds on the previous one in a controlled manner.

In plain words

> Monad pattern ensures that each operation is executed regardless of the success or failure of previous ones.

Wikipedia says

> In functional programming, a monad is a structure that combines program fragments (functions) and wraps their return values in a type with additional computation. In addition to defining a wrapping monadic type, monads define two operators: one to wrap a value in the monad type, and another to compose together functions that output values of the monad type (these are known as monadic functions). General-purpose languages use monads to reduce boilerplate code needed for common operations (such as dealing with undefined values or fallible functions, or encapsulating bookkeeping code). Functional languages use monads to turn complicated sequences of functions into succinct pipelines that abstract away control flow, and side effects.

Flowchart

![Monad flowchart](https://java-design-patterns.com/assets/img/monad-flowchart.b02d0e48.png)

## [Programmatic Example of Monad Pattern in Java](https://java-design-patterns.com/patterns/monad/\#programmatic-example-of-monad-pattern-in-java)

Here’s the Monad implementation in Java. The `Validator` class encapsulates an object and performs validation steps in a monadic fashion, showcasing the benefits of using the Monad pattern for error handling and state management.

```java
public class Validator<T> {
  private final T obj;
  private final List<Throwable> exceptions = new ArrayList<>();

   private Validator(T obj) {
    this.obj = obj;
  }
  public static <T> Validator<T> of(T t) {
    return new Validator<>(Objects.requireNonNull(t));
  }

  public Validator<T> validate(Predicate<? super T> validation, String message) {
    if (!validation.test(obj)) {
      exceptions.add(new IllegalStateException(message));
    }
    return this;
  }

  public <U> Validator<T> validate(
      Function<? super T, ? extends U> projection,
      Predicate<? super U> validation,
      String message
  ) {
    return validate(projection.andThen(validation::test)::apply, message);
  }

  public T get() throws IllegalStateException {
    if (exceptions.isEmpty()) {
      return obj;
    }
    var e = new IllegalStateException();
    exceptions.forEach(e::addSuppressed);
    throw e;
  }
}
```

Next we define an enum `Sex`.

```java
public enum Sex {
  MALE, FEMALE
}
```

Now we can introduce the `User`.

```java
public record User(String name, int age, Sex sex, String email) {
}
```

And finally, a `User` object is validated for its name, email, and age using the `Validator` monad.

```java
public static void main(String[] args) {
    var user = new User("user", 24, Sex.FEMALE, "foobar.com");
    LOGGER.info(Validator.of(user).validate(User::name, Objects::nonNull, "name is null")
        .validate(User::name, name -> !name.isEmpty(), "name is empty")
        .validate(User::email, email -> !email.contains("@"), "email doesn't contains '@'")
        .validate(User::age, age -> age > 20 && age < 30, "age isn't between...").get()
        .toString());
}
```

Console output:

```
15:06:17.679 [main] INFO com.iluwatar.monad.App -- User[name=user, age=24, sex=FEMALE, email=foobar.com]
```

## [When to Use the Monad Pattern in Java](https://java-design-patterns.com/patterns/monad/\#when-to-use-the-monad-pattern-in-java)

The Monad design pattern is applicable when

- Consistent and unified error handling is required without relying on exceptions, particularly in functional programming paradigms.
- Asynchronous computations need clear and maintainable chaining.
- State needs to be managed and encapsulated within functional flows.
- Dependencies and lazy evaluations are to be handled cleanly and efficiently.

## [Monad Pattern Java Tutorials](https://java-design-patterns.com/patterns/monad/\#monad-pattern-java-tutorials)

- [Design Pattern Reloaded (Remi Forax)](https://youtu.be/-k2X7guaArU)

## [Real-World Applications of Monad Pattern in Java](https://java-design-patterns.com/patterns/monad/\#real-world-applications-of-monad-pattern-in-java)

- Optional in Java's standard library for handling potential absence of values.
- Stream for constructing functional pipelines to operate on collections.
- Frameworks like Vavr enhance functional programming in Java by providing monadic constructs for better code maintainability.

## [Benefits and Trade-offs of Monad Pattern](https://java-design-patterns.com/patterns/monad/\#benefits-and-trade-offs-of-monad-pattern)

Benefits:

- Increases code readability and reduces boilerplate.
- Encourages a declarative programming style.
- Promotes immutability and thread safety.
- Simplifies complex error handling and state management.

Trade-offs:

- Can be challenging for developers new to functional programming.
- May introduce performance overhead due to additional abstraction layers.
- Debugging can be difficult due to less transparent operational flow.

## [Related Java Design Patterns](https://java-design-patterns.com/patterns/monad/\#related-java-design-patterns)

Related design patterns to monads in Java include

- [Factory Method](https://java-design-patterns.com/patterns/factory-method/): Similar in that it helps instantiate monads, encapsulating object creation logic.
- [Command](https://java-design-patterns.com/patterns/command/): Also encapsulates operations, but monads add context management to the mix.
- [Decorator](https://java-design-patterns.com/patterns/decorator/): Dynamically enhances functionalities, whereas monads use static typing for consistent composability.

## [References and Credits](https://java-design-patterns.com/patterns/monad/\#references-and-credits)

- [Functional Programming in Java](https://amzn.to/3JUIc5Q)
- [Java 8 in Action: Lambdas, Streams, and functional-style programming](https://amzn.to/3QCmGXs)
- [Real-World Software Development: A Project-Driven Guide to Fundamentals in Java](https://amzn.to/4btoN7U)
- [Monad (functional programming) (Wikipedia)](https://en.wikipedia.org/wiki/Monad_(functional_programming))