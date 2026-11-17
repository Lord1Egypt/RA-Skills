---
name: propertylist-xml
description: Provides usage details for PropertyList XML files, including property storage, expressions, conditions, and more.
---

# Components of the Property Tree

- **Nodes**: A node can hold a typed value as well as child nodes, and both can coexist at the same time.
* **Indices**: Sibling nodes sharing an identical identifier are organized as an indexed array using zero-based numerical offsets. Omitting brackets defaults to index `0` (e.g., `/sim/view` = `/sim/view[0]`). Deleting an indexed node does not re-index or shift subsequent elements, leaving the vacated slot available for reuse.
* **Aliases**: Allows a node to dynamically mirror another target node path, routing all read and write operations directly to the destination.
* **Node attributes**: Flags defining internal engine behaviors, including read/write permissions, runtime state preservation, logging triggers, and persistent serialization.


# The PropertyList format

The root element of each file is always named `<PropertyList>`. Tags are almost always found in pairs, with the closing tag having a slash prefixing the tag name, i.e `</PropertyList>`, just like in any other XML dialect.

## Minimal example

A minimal example of a complete property list encoded XML file, looks like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>

<PropertyList>
</PropertyList>
```

## Property node tags and attributes

Each node in a tree is specified using a single tag that can take attributes describing various things about it:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PropertyList>
 <welcome type="string">Welcome to FlightGear! This is a string as a property</welcome>
</PropertyList>
```

## Property type attributes

Property typing is optional, all properties are by default string/unspecified and are transparently converted by the property tree, but it never hurts, especially when including spaces around numbers:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PropertyList>
 <foo type="string">Hello</foo>
 <pi type="float"> 3.14 </pi>
 <boo type="bool">true</boo>
</PropertyList>
```

## Indexed nodes

Indexing happens implicitly for identically named properties:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PropertyList>
 <foo>Hello</foo> 
 <foo>Hello</foo>
 <foo>Hello</foo>
</PropertyList>
```

so that the three foo tags become `foo[0]`, `foo[1]`, `foo[2]` in the property tree, but you can also use explicit indexing by setting the **n** attribute of each tag:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PropertyList>
 <foo n="0">Hello</foo> 
 <foo n="1">Hello</foo>
 <foo n="2">Hello</foo>
</PropertyList>
```

Though the above two examples are equivalent, we tend often to include "n" anyway, just to help people keep track of where they are. That's most important when there are a lot of subproperties, not in a simple list like the above.

## Archived properties

To make property settings persistent in between FlightGear sessions, use the `userarchive` attribute:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PropertyList>
 <foo userarchive="y">Hello</foo> 
</PropertyList>
```

## Including external PropertyList files

We can also create new PropertyList files by subtyping existing ones using the `include` attribute. For example, if someone made a DC-3 model for JSBSim, we could subclass from the YASim config file like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PropertyList include="dc3-yasim-set.xml">
 <sim>
  <description>DC-3 (JSBSim).</description>
  <flight-model archive="y">jsb</flight-model>
 </sim>
</PropertyList>
```

## Aliased properties

Properties can alias other properties, in a similar way to symbolic links in Unix. When one of them changes the other one changes as well.

For example, this

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PropertyList>
 <foo>46</foo>
 <bar alias="/foo"/>
</PropertyList>
```

will be functionally identical to

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PropertyList>
 <foo>46</foo>
 <bar>46</bar>
</PropertyList>
```

except that `bar` and `foo` will always be identical.

A PropertyList file can begin with a property subtree that are aliased later in the file.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PropertyList>
 <params>
  <comm-freq-prop>/radios/comm1/frequencies/selected</comm-freq-prop>
  <nav-freq-prop>/radios/nav1/frequencies/selected</nav-freq-prop>
 </params>
 <chunk>
  <type>number-value</type>
  <property alias="/params/nav-freq-prop"/>
 </chunk>
</PropertyList>
```

## Aliasing combined with inclusion

The combination of aliasing and inclusion allows for parameterization, which can be of great help both for debugging and maintenance. The above example could for example instead be split up into

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PropertyList>
 <params>
  <comm-freq-prop>/radios/comm1/frequencies/selected</comm-freq-prop>
  <nav-freq-prop>/radios/nav1/frequencies/selected</nav-freq-prop>
 </params>
</PropertyList>
```

and

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PropertyList>
 <params include="MyParams.xml"/>
 <chunk>
  <type>number-value</type>
  <property alias="/params/nav-freq-prop"/>
 </chunk>
</PropertyList>
```

The parameters can be overridden at inclusion:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PropertyList>
 <instrument include="../Instruments/navcomm.xml">
  <params>
   <comm-freq-prop>/radios/comm1/frequencies/selected</comm-freq-prop>
   <nav-freq-prop>/radios/nav1/frequencies/selected</nav-freq-prop>
  </params>
 </instrument>
</PropertyList>
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PropertyList>
 <instrument include="../Instruments/navcomm.xml">
  <params>
   <comm-freq-prop>/radios/comm2/frequencies/selected</comm-freq-prop>
   <nav-freq-prop>/radios/nav2/frequencies/selected</nav-freq-prop>
  </params>
 </instrument>
</PropertyList>
```

# CDATA

Whenever you need to embed text that isn't valid XML, because it may contain XML tokens, you need to wrap the whole section in a CDATA section, this is typically done with Nasal code, so that it doesn't need to escape XML entities:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PropertyList>
 <nasal>
  <![CDATA[
    # begin of code
    print("<!-- Hello World-->\n");
    # end of code
  ]]>
 </nasal>
</PropertyList>
```

# PropertyList-based configuration files

We have config files for totally different purposes, and the fact that they all use XML is simply a convenience for programmers and customizers.
Here are some of the conventions that we've come up with so far, partly ad-hoc (all paths relative to `$FG_ROOT`):

* `defaults.xml` - the top-level default preferences
* `joysticks.xml` - default joystick bindings, included by `defaults.xml`
* `keyboard.xml` - default keyboard bindings, included by `defaults.xml`
* `Aircraft/*-set.xml` - aircraft-specific settings, overriding the defaults in `defaults.xml` (and `joystick/keyboard.xml`)

Basically, these are the main files in the base package that affect FlightGear's main property tree. Other files use the property-file format for convenience to populate various data structures, but they do not touch the main tree and are not accessible through the property browser or through the command-line `--prop:` option; it's just a coincidence that they also use the property-list format:

* `materials.xml` - define the materials (textures, colour, lighting) for use in the scenery
* `HUDS/**/*.xml` - configuration files to define the various heads-up displays
* `Aircraft/*/*-sound.xml` - configuration files to define sounds played for various aircraft
* `Aircraft/*/Panels/*-panel.xml` - configuration files to define 2D panels for various aircraft.
* `Aircraft/*/Instruments/*.xml` - configuration files for individual instruments included by the 2D panels.
* `Aircraft/Instruments/*.xml` - ditto
* `Aircraft/*/Models/*.xml` - animation files for a `.ac` file, oodles of `<animation>` nodes!

We also use some XML-based formats that do not (yet?) follow the property-list conventions, including the following:

* `Aircraft/*/*.xml` - JSBSim aero model config files
* `Aircraft/Aircraft-yasim/*.xml` - YASim aero model config files
* `Engine/*.xml` - JSBSim engine and thruster config files

YASim and JSBSim each uses its own XML format, which is different from the XML format used by the rest of FlightGear.

# Expressions
Expressions (or `SGExpressions`) are a feature of the SimGear library and provide a nice way of implementing complex math formulas using XML syntax.

They are supported in many systems within the FlightGear code.

## Sample Expressions

This is a sample expression for `c = sqrt(a*a + b^2)`. Children/arguments are parsed in the order they appear in the file (or the order in which they are set via property methods).

```xml
<expression>
  <sqrt>
    <sum>
      <product>
        <property>/value/a</property>
        <property>/value/a</property>
      </product>
      <pow>
        <property>/value/b</property>
        <value>2</value>
      </pow>
    </sum>
  </sqrt>
</expression>
```

## Supported elements

```xml
<abs> <!-- also: fabs -->
<acos>
<asin>
<atan>
<atan2>
<ceil>
<clip> <!-- <clipMin> <clipMax> -->
<cos>
<cosh>
<difference> <!-- Subtract the second and subsequent child nodes from the first child node. More than two child nodes are allowed. Also: dif -->
<div> <!-- Divide the first child node by the second child node. -->
<exp>
<floor>
<log> <!-- ln -->
<log10>
<max> <!-- More than two child nodes are allowed. -->
<min> <!-- More than two child nodes are allowed. -->
<mod> <!-- The first node modulo the second node. -->
<pow> <!-- The two nodes are the base and the exponent, respectively. -->
<product> <!-- More than two child nodes are allowed. Also: prod -->
<property> <!-- <prop> cannot be used. -->
<rad2deg>
<deg2rad>
<sin>
<sinh>
<sqr>
<sqrt>
<sum> <!-- More than two child nodes are allowed. -->
<table> <!-- <entry><ind> value </ind><dep> value </dep></entry> -->
<tan>
<tanh>
<value>
```

### Table

The table expression uses the following syntax, similarly to the `<interpolation>` element:

```xml
<table>
	<!-- put an input element here, this can be <property> or any other operation -->
	<entry>
		<ind>0.0</ind> <!-- the value of the input (independent value) -->
		<dep>0.0</dep> <!-- the value of the output (dependent value) -->
	</entry>
        ... <!-- you can put as many entries as you want -->
</table>
```

The entries must be sorted by the independent (input) variable strictly ascending. If input is outside the range of the table, output will be determined from the first / last table row.

#### Example

The table:

| Input (`ind`) | Output (`dep`) |
| --- | --- |
| 0.0 | 5.0 |
| 0.5 | 7.5 |
| 0.9 | -5.0 |
| 1.0 | 25.0 |

translates to the following code:

```xml
<table>
	<!-- put an input element here, this can be a <property> or any other operation -->
	<entry>
		<ind>0.0</ind>
		<dep>5.0</dep>
	</entry>
	<entry>
		<ind>0.5</ind>
		<dep>7.5</dep>
	</entry>
	<entry>
		<ind>0.9</ind>
		<dep>-5.0</dep>
	</entry>
	<entry>
		<ind>1.0</ind>
		<dep>25.0</dep>
	</entry>
</table>
```

### Clip

An expression to limit e.g. rotation:

```xml
  <expression>
    <clip>
      <clipMin>-45</clipMin>
      <clipMax>45</clipMax>
      <property>orientation/pitch-deg</property>
    </clip>
  </expression>
```

## Hints and tips

### Rounding

While there is no element for rounding, this workaround can be used for that:

```xml
<expression>
  <floor>
    <sum>
      <property>your/property/here</property>
      <value>0.5</value>
    </sum>
  </floor>
</expression>
```

# Conditions
## Sample conditions

This is a sample expression for checking if the throttle on the first engine is above half:

```xml
<condition>
  <greater-than>
    <property>/controls/engines/engine[0]/throttle</property>
    <value type="double">0.5</value>
  </greater-than>
</condition>
```

## Supported elements

Each comparison (like `less-than` or `greater-than-equals`) requires either two `<property>` elements (the first with index=0 and the second with index=1) or a `<property>` (considered first) and `<value>` (considered second); booleans compare each of their child conditions. A `<condition>` element itself functions as an `<and>` element; that is, it can have several children, all of which must be true to make the whole condition true. Instead of `<property>` or `<value>` you can also use an `<expression>`.

```xml
<and>
<or>
<not> <!-- acts like logical inverse of <and>, i.e. accepts child conditions -->
<equals>
<not-equals>
<less-than>
<greater-than>
<less-than-equals>
<greater-than-equals>
<property> <!-- evaluates boolean value of specified property -->
<false/> <!-- static false value (<value> does NOT work in conditions !)-->
<true/><!-- static true value -->
```
