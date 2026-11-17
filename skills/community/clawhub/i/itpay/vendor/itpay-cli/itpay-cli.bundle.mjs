#!/usr/bin/env node
import{createRequire as __cr}from'node:module';const require=__cr(import.meta.url);
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __require = /* @__PURE__ */ ((x) => typeof require !== "undefined" ? require : typeof Proxy !== "undefined" ? new Proxy(x, {
  get: (a, b) => (typeof require !== "undefined" ? require : a)[b]
}) : x)(function(x) {
  if (typeof require !== "undefined") return require.apply(this, arguments);
  throw Error('Dynamic require of "' + x + '" is not supported');
});
var __commonJS = (cb, mod) => function __require2() {
  try {
    return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
  } catch (e) {
    throw mod = 0, e;
  }
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/commander/lib/error.js
var require_error = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/commander/lib/error.js"(exports) {
    var CommanderError2 = class extends Error {
      /**
       * Constructs the CommanderError class
       * @param {number} exitCode suggested exit code which could be used with process.exit
       * @param {string} code an id string representing the error
       * @param {string} message human-readable description of the error
       */
      constructor(exitCode, code, message) {
        super(message);
        Error.captureStackTrace(this, this.constructor);
        this.name = this.constructor.name;
        this.code = code;
        this.exitCode = exitCode;
        this.nestedError = void 0;
      }
    };
    var InvalidArgumentError2 = class extends CommanderError2 {
      /**
       * Constructs the InvalidArgumentError class
       * @param {string} [message] explanation of why argument is invalid
       */
      constructor(message) {
        super(1, "commander.invalidArgument", message);
        Error.captureStackTrace(this, this.constructor);
        this.name = this.constructor.name;
      }
    };
    exports.CommanderError = CommanderError2;
    exports.InvalidArgumentError = InvalidArgumentError2;
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/commander/lib/argument.js
var require_argument = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/commander/lib/argument.js"(exports) {
    var { InvalidArgumentError: InvalidArgumentError2 } = require_error();
    var Argument2 = class {
      /**
       * Initialize a new command argument with the given name and description.
       * The default is that the argument is required, and you can explicitly
       * indicate this with <> around the name. Put [] around the name for an optional argument.
       *
       * @param {string} name
       * @param {string} [description]
       */
      constructor(name, description) {
        this.description = description || "";
        this.variadic = false;
        this.parseArg = void 0;
        this.defaultValue = void 0;
        this.defaultValueDescription = void 0;
        this.argChoices = void 0;
        switch (name[0]) {
          case "<":
            this.required = true;
            this._name = name.slice(1, -1);
            break;
          case "[":
            this.required = false;
            this._name = name.slice(1, -1);
            break;
          default:
            this.required = true;
            this._name = name;
            break;
        }
        if (this._name.length > 3 && this._name.slice(-3) === "...") {
          this.variadic = true;
          this._name = this._name.slice(0, -3);
        }
      }
      /**
       * Return argument name.
       *
       * @return {string}
       */
      name() {
        return this._name;
      }
      /**
       * @package
       */
      _concatValue(value, previous) {
        if (previous === this.defaultValue || !Array.isArray(previous)) {
          return [value];
        }
        return previous.concat(value);
      }
      /**
       * Set the default value, and optionally supply the description to be displayed in the help.
       *
       * @param {*} value
       * @param {string} [description]
       * @return {Argument}
       */
      default(value, description) {
        this.defaultValue = value;
        this.defaultValueDescription = description;
        return this;
      }
      /**
       * Set the custom handler for processing CLI command arguments into argument values.
       *
       * @param {Function} [fn]
       * @return {Argument}
       */
      argParser(fn) {
        this.parseArg = fn;
        return this;
      }
      /**
       * Only allow argument value to be one of choices.
       *
       * @param {string[]} values
       * @return {Argument}
       */
      choices(values) {
        this.argChoices = values.slice();
        this.parseArg = (arg, previous) => {
          if (!this.argChoices.includes(arg)) {
            throw new InvalidArgumentError2(
              `Allowed choices are ${this.argChoices.join(", ")}.`
            );
          }
          if (this.variadic) {
            return this._concatValue(arg, previous);
          }
          return arg;
        };
        return this;
      }
      /**
       * Make argument required.
       *
       * @returns {Argument}
       */
      argRequired() {
        this.required = true;
        return this;
      }
      /**
       * Make argument optional.
       *
       * @returns {Argument}
       */
      argOptional() {
        this.required = false;
        return this;
      }
    };
    function humanReadableArgName(arg) {
      const nameOutput = arg.name() + (arg.variadic === true ? "..." : "");
      return arg.required ? "<" + nameOutput + ">" : "[" + nameOutput + "]";
    }
    exports.Argument = Argument2;
    exports.humanReadableArgName = humanReadableArgName;
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/commander/lib/help.js
var require_help = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/commander/lib/help.js"(exports) {
    var { humanReadableArgName } = require_argument();
    var Help2 = class {
      constructor() {
        this.helpWidth = void 0;
        this.sortSubcommands = false;
        this.sortOptions = false;
        this.showGlobalOptions = false;
      }
      /**
       * Get an array of the visible subcommands. Includes a placeholder for the implicit help command, if there is one.
       *
       * @param {Command} cmd
       * @returns {Command[]}
       */
      visibleCommands(cmd) {
        const visibleCommands = cmd.commands.filter((cmd2) => !cmd2._hidden);
        const helpCommand = cmd._getHelpCommand();
        if (helpCommand && !helpCommand._hidden) {
          visibleCommands.push(helpCommand);
        }
        if (this.sortSubcommands) {
          visibleCommands.sort((a, b) => {
            return a.name().localeCompare(b.name());
          });
        }
        return visibleCommands;
      }
      /**
       * Compare options for sort.
       *
       * @param {Option} a
       * @param {Option} b
       * @returns {number}
       */
      compareOptions(a, b) {
        const getSortKey = (option) => {
          return option.short ? option.short.replace(/^-/, "") : option.long.replace(/^--/, "");
        };
        return getSortKey(a).localeCompare(getSortKey(b));
      }
      /**
       * Get an array of the visible options. Includes a placeholder for the implicit help option, if there is one.
       *
       * @param {Command} cmd
       * @returns {Option[]}
       */
      visibleOptions(cmd) {
        const visibleOptions = cmd.options.filter((option) => !option.hidden);
        const helpOption = cmd._getHelpOption();
        if (helpOption && !helpOption.hidden) {
          const removeShort = helpOption.short && cmd._findOption(helpOption.short);
          const removeLong = helpOption.long && cmd._findOption(helpOption.long);
          if (!removeShort && !removeLong) {
            visibleOptions.push(helpOption);
          } else if (helpOption.long && !removeLong) {
            visibleOptions.push(
              cmd.createOption(helpOption.long, helpOption.description)
            );
          } else if (helpOption.short && !removeShort) {
            visibleOptions.push(
              cmd.createOption(helpOption.short, helpOption.description)
            );
          }
        }
        if (this.sortOptions) {
          visibleOptions.sort(this.compareOptions);
        }
        return visibleOptions;
      }
      /**
       * Get an array of the visible global options. (Not including help.)
       *
       * @param {Command} cmd
       * @returns {Option[]}
       */
      visibleGlobalOptions(cmd) {
        if (!this.showGlobalOptions) return [];
        const globalOptions = [];
        for (let ancestorCmd = cmd.parent; ancestorCmd; ancestorCmd = ancestorCmd.parent) {
          const visibleOptions = ancestorCmd.options.filter(
            (option) => !option.hidden
          );
          globalOptions.push(...visibleOptions);
        }
        if (this.sortOptions) {
          globalOptions.sort(this.compareOptions);
        }
        return globalOptions;
      }
      /**
       * Get an array of the arguments if any have a description.
       *
       * @param {Command} cmd
       * @returns {Argument[]}
       */
      visibleArguments(cmd) {
        if (cmd._argsDescription) {
          cmd.registeredArguments.forEach((argument) => {
            argument.description = argument.description || cmd._argsDescription[argument.name()] || "";
          });
        }
        if (cmd.registeredArguments.find((argument) => argument.description)) {
          return cmd.registeredArguments;
        }
        return [];
      }
      /**
       * Get the command term to show in the list of subcommands.
       *
       * @param {Command} cmd
       * @returns {string}
       */
      subcommandTerm(cmd) {
        const args = cmd.registeredArguments.map((arg) => humanReadableArgName(arg)).join(" ");
        return cmd._name + (cmd._aliases[0] ? "|" + cmd._aliases[0] : "") + (cmd.options.length ? " [options]" : "") + // simplistic check for non-help option
        (args ? " " + args : "");
      }
      /**
       * Get the option term to show in the list of options.
       *
       * @param {Option} option
       * @returns {string}
       */
      optionTerm(option) {
        return option.flags;
      }
      /**
       * Get the argument term to show in the list of arguments.
       *
       * @param {Argument} argument
       * @returns {string}
       */
      argumentTerm(argument) {
        return argument.name();
      }
      /**
       * Get the longest command term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      longestSubcommandTermLength(cmd, helper) {
        return helper.visibleCommands(cmd).reduce((max, command) => {
          return Math.max(max, helper.subcommandTerm(command).length);
        }, 0);
      }
      /**
       * Get the longest option term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      longestOptionTermLength(cmd, helper) {
        return helper.visibleOptions(cmd).reduce((max, option) => {
          return Math.max(max, helper.optionTerm(option).length);
        }, 0);
      }
      /**
       * Get the longest global option term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      longestGlobalOptionTermLength(cmd, helper) {
        return helper.visibleGlobalOptions(cmd).reduce((max, option) => {
          return Math.max(max, helper.optionTerm(option).length);
        }, 0);
      }
      /**
       * Get the longest argument term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      longestArgumentTermLength(cmd, helper) {
        return helper.visibleArguments(cmd).reduce((max, argument) => {
          return Math.max(max, helper.argumentTerm(argument).length);
        }, 0);
      }
      /**
       * Get the command usage to be displayed at the top of the built-in help.
       *
       * @param {Command} cmd
       * @returns {string}
       */
      commandUsage(cmd) {
        let cmdName = cmd._name;
        if (cmd._aliases[0]) {
          cmdName = cmdName + "|" + cmd._aliases[0];
        }
        let ancestorCmdNames = "";
        for (let ancestorCmd = cmd.parent; ancestorCmd; ancestorCmd = ancestorCmd.parent) {
          ancestorCmdNames = ancestorCmd.name() + " " + ancestorCmdNames;
        }
        return ancestorCmdNames + cmdName + " " + cmd.usage();
      }
      /**
       * Get the description for the command.
       *
       * @param {Command} cmd
       * @returns {string}
       */
      commandDescription(cmd) {
        return cmd.description();
      }
      /**
       * Get the subcommand summary to show in the list of subcommands.
       * (Fallback to description for backwards compatibility.)
       *
       * @param {Command} cmd
       * @returns {string}
       */
      subcommandDescription(cmd) {
        return cmd.summary() || cmd.description();
      }
      /**
       * Get the option description to show in the list of options.
       *
       * @param {Option} option
       * @return {string}
       */
      optionDescription(option) {
        const extraInfo = [];
        if (option.argChoices) {
          extraInfo.push(
            // use stringify to match the display of the default value
            `choices: ${option.argChoices.map((choice) => JSON.stringify(choice)).join(", ")}`
          );
        }
        if (option.defaultValue !== void 0) {
          const showDefault = option.required || option.optional || option.isBoolean() && typeof option.defaultValue === "boolean";
          if (showDefault) {
            extraInfo.push(
              `default: ${option.defaultValueDescription || JSON.stringify(option.defaultValue)}`
            );
          }
        }
        if (option.presetArg !== void 0 && option.optional) {
          extraInfo.push(`preset: ${JSON.stringify(option.presetArg)}`);
        }
        if (option.envVar !== void 0) {
          extraInfo.push(`env: ${option.envVar}`);
        }
        if (extraInfo.length > 0) {
          return `${option.description} (${extraInfo.join(", ")})`;
        }
        return option.description;
      }
      /**
       * Get the argument description to show in the list of arguments.
       *
       * @param {Argument} argument
       * @return {string}
       */
      argumentDescription(argument) {
        const extraInfo = [];
        if (argument.argChoices) {
          extraInfo.push(
            // use stringify to match the display of the default value
            `choices: ${argument.argChoices.map((choice) => JSON.stringify(choice)).join(", ")}`
          );
        }
        if (argument.defaultValue !== void 0) {
          extraInfo.push(
            `default: ${argument.defaultValueDescription || JSON.stringify(argument.defaultValue)}`
          );
        }
        if (extraInfo.length > 0) {
          const extraDescripton = `(${extraInfo.join(", ")})`;
          if (argument.description) {
            return `${argument.description} ${extraDescripton}`;
          }
          return extraDescripton;
        }
        return argument.description;
      }
      /**
       * Generate the built-in help text.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {string}
       */
      formatHelp(cmd, helper) {
        const termWidth = helper.padWidth(cmd, helper);
        const helpWidth = helper.helpWidth || 80;
        const itemIndentWidth = 2;
        const itemSeparatorWidth = 2;
        function formatItem(term, description) {
          if (description) {
            const fullText = `${term.padEnd(termWidth + itemSeparatorWidth)}${description}`;
            return helper.wrap(
              fullText,
              helpWidth - itemIndentWidth,
              termWidth + itemSeparatorWidth
            );
          }
          return term;
        }
        function formatList(textArray) {
          return textArray.join("\n").replace(/^/gm, " ".repeat(itemIndentWidth));
        }
        let output = [`Usage: ${helper.commandUsage(cmd)}`, ""];
        const commandDescription = helper.commandDescription(cmd);
        if (commandDescription.length > 0) {
          output = output.concat([
            helper.wrap(commandDescription, helpWidth, 0),
            ""
          ]);
        }
        const argumentList = helper.visibleArguments(cmd).map((argument) => {
          return formatItem(
            helper.argumentTerm(argument),
            helper.argumentDescription(argument)
          );
        });
        if (argumentList.length > 0) {
          output = output.concat(["Arguments:", formatList(argumentList), ""]);
        }
        const optionList = helper.visibleOptions(cmd).map((option) => {
          return formatItem(
            helper.optionTerm(option),
            helper.optionDescription(option)
          );
        });
        if (optionList.length > 0) {
          output = output.concat(["Options:", formatList(optionList), ""]);
        }
        if (this.showGlobalOptions) {
          const globalOptionList = helper.visibleGlobalOptions(cmd).map((option) => {
            return formatItem(
              helper.optionTerm(option),
              helper.optionDescription(option)
            );
          });
          if (globalOptionList.length > 0) {
            output = output.concat([
              "Global Options:",
              formatList(globalOptionList),
              ""
            ]);
          }
        }
        const commandList = helper.visibleCommands(cmd).map((cmd2) => {
          return formatItem(
            helper.subcommandTerm(cmd2),
            helper.subcommandDescription(cmd2)
          );
        });
        if (commandList.length > 0) {
          output = output.concat(["Commands:", formatList(commandList), ""]);
        }
        return output.join("\n");
      }
      /**
       * Calculate the pad width from the maximum term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      padWidth(cmd, helper) {
        return Math.max(
          helper.longestOptionTermLength(cmd, helper),
          helper.longestGlobalOptionTermLength(cmd, helper),
          helper.longestSubcommandTermLength(cmd, helper),
          helper.longestArgumentTermLength(cmd, helper)
        );
      }
      /**
       * Wrap the given string to width characters per line, with lines after the first indented.
       * Do not wrap if insufficient room for wrapping (minColumnWidth), or string is manually formatted.
       *
       * @param {string} str
       * @param {number} width
       * @param {number} indent
       * @param {number} [minColumnWidth=40]
       * @return {string}
       *
       */
      wrap(str, width, indent, minColumnWidth = 40) {
        const indents = " \\f\\t\\v\xA0\u1680\u2000-\u200A\u202F\u205F\u3000\uFEFF";
        const manualIndent = new RegExp(`[\\n][${indents}]+`);
        if (str.match(manualIndent)) return str;
        const columnWidth = width - indent;
        if (columnWidth < minColumnWidth) return str;
        const leadingStr = str.slice(0, indent);
        const columnText = str.slice(indent).replace("\r\n", "\n");
        const indentString = " ".repeat(indent);
        const zeroWidthSpace = "\u200B";
        const breaks = `\\s${zeroWidthSpace}`;
        const regex = new RegExp(
          `
|.{1,${columnWidth - 1}}([${breaks}]|$)|[^${breaks}]+?([${breaks}]|$)`,
          "g"
        );
        const lines = columnText.match(regex) || [];
        return leadingStr + lines.map((line, i) => {
          if (line === "\n") return "";
          return (i > 0 ? indentString : "") + line.trimEnd();
        }).join("\n");
      }
    };
    exports.Help = Help2;
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/commander/lib/option.js
var require_option = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/commander/lib/option.js"(exports) {
    var { InvalidArgumentError: InvalidArgumentError2 } = require_error();
    var Option2 = class {
      /**
       * Initialize a new `Option` with the given `flags` and `description`.
       *
       * @param {string} flags
       * @param {string} [description]
       */
      constructor(flags, description) {
        this.flags = flags;
        this.description = description || "";
        this.required = flags.includes("<");
        this.optional = flags.includes("[");
        this.variadic = /\w\.\.\.[>\]]$/.test(flags);
        this.mandatory = false;
        const optionFlags = splitOptionFlags(flags);
        this.short = optionFlags.shortFlag;
        this.long = optionFlags.longFlag;
        this.negate = false;
        if (this.long) {
          this.negate = this.long.startsWith("--no-");
        }
        this.defaultValue = void 0;
        this.defaultValueDescription = void 0;
        this.presetArg = void 0;
        this.envVar = void 0;
        this.parseArg = void 0;
        this.hidden = false;
        this.argChoices = void 0;
        this.conflictsWith = [];
        this.implied = void 0;
      }
      /**
       * Set the default value, and optionally supply the description to be displayed in the help.
       *
       * @param {*} value
       * @param {string} [description]
       * @return {Option}
       */
      default(value, description) {
        this.defaultValue = value;
        this.defaultValueDescription = description;
        return this;
      }
      /**
       * Preset to use when option used without option-argument, especially optional but also boolean and negated.
       * The custom processing (parseArg) is called.
       *
       * @example
       * new Option('--color').default('GREYSCALE').preset('RGB');
       * new Option('--donate [amount]').preset('20').argParser(parseFloat);
       *
       * @param {*} arg
       * @return {Option}
       */
      preset(arg) {
        this.presetArg = arg;
        return this;
      }
      /**
       * Add option name(s) that conflict with this option.
       * An error will be displayed if conflicting options are found during parsing.
       *
       * @example
       * new Option('--rgb').conflicts('cmyk');
       * new Option('--js').conflicts(['ts', 'jsx']);
       *
       * @param {(string | string[])} names
       * @return {Option}
       */
      conflicts(names) {
        this.conflictsWith = this.conflictsWith.concat(names);
        return this;
      }
      /**
       * Specify implied option values for when this option is set and the implied options are not.
       *
       * The custom processing (parseArg) is not called on the implied values.
       *
       * @example
       * program
       *   .addOption(new Option('--log', 'write logging information to file'))
       *   .addOption(new Option('--trace', 'log extra details').implies({ log: 'trace.txt' }));
       *
       * @param {object} impliedOptionValues
       * @return {Option}
       */
      implies(impliedOptionValues) {
        let newImplied = impliedOptionValues;
        if (typeof impliedOptionValues === "string") {
          newImplied = { [impliedOptionValues]: true };
        }
        this.implied = Object.assign(this.implied || {}, newImplied);
        return this;
      }
      /**
       * Set environment variable to check for option value.
       *
       * An environment variable is only used if when processed the current option value is
       * undefined, or the source of the current value is 'default' or 'config' or 'env'.
       *
       * @param {string} name
       * @return {Option}
       */
      env(name) {
        this.envVar = name;
        return this;
      }
      /**
       * Set the custom handler for processing CLI option arguments into option values.
       *
       * @param {Function} [fn]
       * @return {Option}
       */
      argParser(fn) {
        this.parseArg = fn;
        return this;
      }
      /**
       * Whether the option is mandatory and must have a value after parsing.
       *
       * @param {boolean} [mandatory=true]
       * @return {Option}
       */
      makeOptionMandatory(mandatory = true) {
        this.mandatory = !!mandatory;
        return this;
      }
      /**
       * Hide option in help.
       *
       * @param {boolean} [hide=true]
       * @return {Option}
       */
      hideHelp(hide = true) {
        this.hidden = !!hide;
        return this;
      }
      /**
       * @package
       */
      _concatValue(value, previous) {
        if (previous === this.defaultValue || !Array.isArray(previous)) {
          return [value];
        }
        return previous.concat(value);
      }
      /**
       * Only allow option value to be one of choices.
       *
       * @param {string[]} values
       * @return {Option}
       */
      choices(values) {
        this.argChoices = values.slice();
        this.parseArg = (arg, previous) => {
          if (!this.argChoices.includes(arg)) {
            throw new InvalidArgumentError2(
              `Allowed choices are ${this.argChoices.join(", ")}.`
            );
          }
          if (this.variadic) {
            return this._concatValue(arg, previous);
          }
          return arg;
        };
        return this;
      }
      /**
       * Return option name.
       *
       * @return {string}
       */
      name() {
        if (this.long) {
          return this.long.replace(/^--/, "");
        }
        return this.short.replace(/^-/, "");
      }
      /**
       * Return option name, in a camelcase format that can be used
       * as a object attribute key.
       *
       * @return {string}
       */
      attributeName() {
        return camelcase(this.name().replace(/^no-/, ""));
      }
      /**
       * Check if `arg` matches the short or long flag.
       *
       * @param {string} arg
       * @return {boolean}
       * @package
       */
      is(arg) {
        return this.short === arg || this.long === arg;
      }
      /**
       * Return whether a boolean option.
       *
       * Options are one of boolean, negated, required argument, or optional argument.
       *
       * @return {boolean}
       * @package
       */
      isBoolean() {
        return !this.required && !this.optional && !this.negate;
      }
    };
    var DualOptions = class {
      /**
       * @param {Option[]} options
       */
      constructor(options) {
        this.positiveOptions = /* @__PURE__ */ new Map();
        this.negativeOptions = /* @__PURE__ */ new Map();
        this.dualOptions = /* @__PURE__ */ new Set();
        options.forEach((option) => {
          if (option.negate) {
            this.negativeOptions.set(option.attributeName(), option);
          } else {
            this.positiveOptions.set(option.attributeName(), option);
          }
        });
        this.negativeOptions.forEach((value, key) => {
          if (this.positiveOptions.has(key)) {
            this.dualOptions.add(key);
          }
        });
      }
      /**
       * Did the value come from the option, and not from possible matching dual option?
       *
       * @param {*} value
       * @param {Option} option
       * @returns {boolean}
       */
      valueFromOption(value, option) {
        const optionKey = option.attributeName();
        if (!this.dualOptions.has(optionKey)) return true;
        const preset = this.negativeOptions.get(optionKey).presetArg;
        const negativeValue = preset !== void 0 ? preset : false;
        return option.negate === (negativeValue === value);
      }
    };
    function camelcase(str) {
      return str.split("-").reduce((str2, word) => {
        return str2 + word[0].toUpperCase() + word.slice(1);
      });
    }
    function splitOptionFlags(flags) {
      let shortFlag;
      let longFlag;
      const flagParts = flags.split(/[ |,]+/);
      if (flagParts.length > 1 && !/^[[<]/.test(flagParts[1]))
        shortFlag = flagParts.shift();
      longFlag = flagParts.shift();
      if (!shortFlag && /^-[^-]$/.test(longFlag)) {
        shortFlag = longFlag;
        longFlag = void 0;
      }
      return { shortFlag, longFlag };
    }
    exports.Option = Option2;
    exports.DualOptions = DualOptions;
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/commander/lib/suggestSimilar.js
var require_suggestSimilar = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/commander/lib/suggestSimilar.js"(exports) {
    var maxDistance = 3;
    function editDistance(a, b) {
      if (Math.abs(a.length - b.length) > maxDistance)
        return Math.max(a.length, b.length);
      const d = [];
      for (let i = 0; i <= a.length; i++) {
        d[i] = [i];
      }
      for (let j = 0; j <= b.length; j++) {
        d[0][j] = j;
      }
      for (let j = 1; j <= b.length; j++) {
        for (let i = 1; i <= a.length; i++) {
          let cost = 1;
          if (a[i - 1] === b[j - 1]) {
            cost = 0;
          } else {
            cost = 1;
          }
          d[i][j] = Math.min(
            d[i - 1][j] + 1,
            // deletion
            d[i][j - 1] + 1,
            // insertion
            d[i - 1][j - 1] + cost
            // substitution
          );
          if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) {
            d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1);
          }
        }
      }
      return d[a.length][b.length];
    }
    function suggestSimilar(word, candidates) {
      if (!candidates || candidates.length === 0) return "";
      candidates = Array.from(new Set(candidates));
      const searchingOptions = word.startsWith("--");
      if (searchingOptions) {
        word = word.slice(2);
        candidates = candidates.map((candidate) => candidate.slice(2));
      }
      let similar = [];
      let bestDistance = maxDistance;
      const minSimilarity = 0.4;
      candidates.forEach((candidate) => {
        if (candidate.length <= 1) return;
        const distance = editDistance(word, candidate);
        const length = Math.max(word.length, candidate.length);
        const similarity = (length - distance) / length;
        if (similarity > minSimilarity) {
          if (distance < bestDistance) {
            bestDistance = distance;
            similar = [candidate];
          } else if (distance === bestDistance) {
            similar.push(candidate);
          }
        }
      });
      similar.sort((a, b) => a.localeCompare(b));
      if (searchingOptions) {
        similar = similar.map((candidate) => `--${candidate}`);
      }
      if (similar.length > 1) {
        return `
(Did you mean one of ${similar.join(", ")}?)`;
      }
      if (similar.length === 1) {
        return `
(Did you mean ${similar[0]}?)`;
      }
      return "";
    }
    exports.suggestSimilar = suggestSimilar;
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/commander/lib/command.js
var require_command = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/commander/lib/command.js"(exports) {
    var EventEmitter = __require("node:events").EventEmitter;
    var childProcess = __require("node:child_process");
    var path3 = __require("node:path");
    var fs2 = __require("node:fs");
    var process2 = __require("node:process");
    var { Argument: Argument2, humanReadableArgName } = require_argument();
    var { CommanderError: CommanderError2 } = require_error();
    var { Help: Help2 } = require_help();
    var { Option: Option2, DualOptions } = require_option();
    var { suggestSimilar } = require_suggestSimilar();
    var Command2 = class _Command extends EventEmitter {
      /**
       * Initialize a new `Command`.
       *
       * @param {string} [name]
       */
      constructor(name) {
        super();
        this.commands = [];
        this.options = [];
        this.parent = null;
        this._allowUnknownOption = false;
        this._allowExcessArguments = true;
        this.registeredArguments = [];
        this._args = this.registeredArguments;
        this.args = [];
        this.rawArgs = [];
        this.processedArgs = [];
        this._scriptPath = null;
        this._name = name || "";
        this._optionValues = {};
        this._optionValueSources = {};
        this._storeOptionsAsProperties = false;
        this._actionHandler = null;
        this._executableHandler = false;
        this._executableFile = null;
        this._executableDir = null;
        this._defaultCommandName = null;
        this._exitCallback = null;
        this._aliases = [];
        this._combineFlagAndOptionalValue = true;
        this._description = "";
        this._summary = "";
        this._argsDescription = void 0;
        this._enablePositionalOptions = false;
        this._passThroughOptions = false;
        this._lifeCycleHooks = {};
        this._showHelpAfterError = false;
        this._showSuggestionAfterError = true;
        this._outputConfiguration = {
          writeOut: (str) => process2.stdout.write(str),
          writeErr: (str) => process2.stderr.write(str),
          getOutHelpWidth: () => process2.stdout.isTTY ? process2.stdout.columns : void 0,
          getErrHelpWidth: () => process2.stderr.isTTY ? process2.stderr.columns : void 0,
          outputError: (str, write) => write(str)
        };
        this._hidden = false;
        this._helpOption = void 0;
        this._addImplicitHelpCommand = void 0;
        this._helpCommand = void 0;
        this._helpConfiguration = {};
      }
      /**
       * Copy settings that are useful to have in common across root command and subcommands.
       *
       * (Used internally when adding a command using `.command()` so subcommands inherit parent settings.)
       *
       * @param {Command} sourceCommand
       * @return {Command} `this` command for chaining
       */
      copyInheritedSettings(sourceCommand) {
        this._outputConfiguration = sourceCommand._outputConfiguration;
        this._helpOption = sourceCommand._helpOption;
        this._helpCommand = sourceCommand._helpCommand;
        this._helpConfiguration = sourceCommand._helpConfiguration;
        this._exitCallback = sourceCommand._exitCallback;
        this._storeOptionsAsProperties = sourceCommand._storeOptionsAsProperties;
        this._combineFlagAndOptionalValue = sourceCommand._combineFlagAndOptionalValue;
        this._allowExcessArguments = sourceCommand._allowExcessArguments;
        this._enablePositionalOptions = sourceCommand._enablePositionalOptions;
        this._showHelpAfterError = sourceCommand._showHelpAfterError;
        this._showSuggestionAfterError = sourceCommand._showSuggestionAfterError;
        return this;
      }
      /**
       * @returns {Command[]}
       * @private
       */
      _getCommandAndAncestors() {
        const result = [];
        for (let command = this; command; command = command.parent) {
          result.push(command);
        }
        return result;
      }
      /**
       * Define a command.
       *
       * There are two styles of command: pay attention to where to put the description.
       *
       * @example
       * // Command implemented using action handler (description is supplied separately to `.command`)
       * program
       *   .command('clone <source> [destination]')
       *   .description('clone a repository into a newly created directory')
       *   .action((source, destination) => {
       *     console.log('clone command called');
       *   });
       *
       * // Command implemented using separate executable file (description is second parameter to `.command`)
       * program
       *   .command('start <service>', 'start named service')
       *   .command('stop [service]', 'stop named service, or all if no name supplied');
       *
       * @param {string} nameAndArgs - command name and arguments, args are `<required>` or `[optional]` and last may also be `variadic...`
       * @param {(object | string)} [actionOptsOrExecDesc] - configuration options (for action), or description (for executable)
       * @param {object} [execOpts] - configuration options (for executable)
       * @return {Command} returns new command for action handler, or `this` for executable command
       */
      command(nameAndArgs, actionOptsOrExecDesc, execOpts) {
        let desc = actionOptsOrExecDesc;
        let opts = execOpts;
        if (typeof desc === "object" && desc !== null) {
          opts = desc;
          desc = null;
        }
        opts = opts || {};
        const [, name, args] = nameAndArgs.match(/([^ ]+) *(.*)/);
        const cmd = this.createCommand(name);
        if (desc) {
          cmd.description(desc);
          cmd._executableHandler = true;
        }
        if (opts.isDefault) this._defaultCommandName = cmd._name;
        cmd._hidden = !!(opts.noHelp || opts.hidden);
        cmd._executableFile = opts.executableFile || null;
        if (args) cmd.arguments(args);
        this._registerCommand(cmd);
        cmd.parent = this;
        cmd.copyInheritedSettings(this);
        if (desc) return this;
        return cmd;
      }
      /**
       * Factory routine to create a new unattached command.
       *
       * See .command() for creating an attached subcommand, which uses this routine to
       * create the command. You can override createCommand to customise subcommands.
       *
       * @param {string} [name]
       * @return {Command} new command
       */
      createCommand(name) {
        return new _Command(name);
      }
      /**
       * You can customise the help with a subclass of Help by overriding createHelp,
       * or by overriding Help properties using configureHelp().
       *
       * @return {Help}
       */
      createHelp() {
        return Object.assign(new Help2(), this.configureHelp());
      }
      /**
       * You can customise the help by overriding Help properties using configureHelp(),
       * or with a subclass of Help by overriding createHelp().
       *
       * @param {object} [configuration] - configuration options
       * @return {(Command | object)} `this` command for chaining, or stored configuration
       */
      configureHelp(configuration) {
        if (configuration === void 0) return this._helpConfiguration;
        this._helpConfiguration = configuration;
        return this;
      }
      /**
       * The default output goes to stdout and stderr. You can customise this for special
       * applications. You can also customise the display of errors by overriding outputError.
       *
       * The configuration properties are all functions:
       *
       *     // functions to change where being written, stdout and stderr
       *     writeOut(str)
       *     writeErr(str)
       *     // matching functions to specify width for wrapping help
       *     getOutHelpWidth()
       *     getErrHelpWidth()
       *     // functions based on what is being written out
       *     outputError(str, write) // used for displaying errors, and not used for displaying help
       *
       * @param {object} [configuration] - configuration options
       * @return {(Command | object)} `this` command for chaining, or stored configuration
       */
      configureOutput(configuration) {
        if (configuration === void 0) return this._outputConfiguration;
        Object.assign(this._outputConfiguration, configuration);
        return this;
      }
      /**
       * Display the help or a custom message after an error occurs.
       *
       * @param {(boolean|string)} [displayHelp]
       * @return {Command} `this` command for chaining
       */
      showHelpAfterError(displayHelp = true) {
        if (typeof displayHelp !== "string") displayHelp = !!displayHelp;
        this._showHelpAfterError = displayHelp;
        return this;
      }
      /**
       * Display suggestion of similar commands for unknown commands, or options for unknown options.
       *
       * @param {boolean} [displaySuggestion]
       * @return {Command} `this` command for chaining
       */
      showSuggestionAfterError(displaySuggestion = true) {
        this._showSuggestionAfterError = !!displaySuggestion;
        return this;
      }
      /**
       * Add a prepared subcommand.
       *
       * See .command() for creating an attached subcommand which inherits settings from its parent.
       *
       * @param {Command} cmd - new subcommand
       * @param {object} [opts] - configuration options
       * @return {Command} `this` command for chaining
       */
      addCommand(cmd, opts) {
        if (!cmd._name) {
          throw new Error(`Command passed to .addCommand() must have a name
- specify the name in Command constructor or using .name()`);
        }
        opts = opts || {};
        if (opts.isDefault) this._defaultCommandName = cmd._name;
        if (opts.noHelp || opts.hidden) cmd._hidden = true;
        this._registerCommand(cmd);
        cmd.parent = this;
        cmd._checkForBrokenPassThrough();
        return this;
      }
      /**
       * Factory routine to create a new unattached argument.
       *
       * See .argument() for creating an attached argument, which uses this routine to
       * create the argument. You can override createArgument to return a custom argument.
       *
       * @param {string} name
       * @param {string} [description]
       * @return {Argument} new argument
       */
      createArgument(name, description) {
        return new Argument2(name, description);
      }
      /**
       * Define argument syntax for command.
       *
       * The default is that the argument is required, and you can explicitly
       * indicate this with <> around the name. Put [] around the name for an optional argument.
       *
       * @example
       * program.argument('<input-file>');
       * program.argument('[output-file]');
       *
       * @param {string} name
       * @param {string} [description]
       * @param {(Function|*)} [fn] - custom argument processing function
       * @param {*} [defaultValue]
       * @return {Command} `this` command for chaining
       */
      argument(name, description, fn, defaultValue) {
        const argument = this.createArgument(name, description);
        if (typeof fn === "function") {
          argument.default(defaultValue).argParser(fn);
        } else {
          argument.default(fn);
        }
        this.addArgument(argument);
        return this;
      }
      /**
       * Define argument syntax for command, adding multiple at once (without descriptions).
       *
       * See also .argument().
       *
       * @example
       * program.arguments('<cmd> [env]');
       *
       * @param {string} names
       * @return {Command} `this` command for chaining
       */
      arguments(names) {
        names.trim().split(/ +/).forEach((detail) => {
          this.argument(detail);
        });
        return this;
      }
      /**
       * Define argument syntax for command, adding a prepared argument.
       *
       * @param {Argument} argument
       * @return {Command} `this` command for chaining
       */
      addArgument(argument) {
        const previousArgument = this.registeredArguments.slice(-1)[0];
        if (previousArgument && previousArgument.variadic) {
          throw new Error(
            `only the last argument can be variadic '${previousArgument.name()}'`
          );
        }
        if (argument.required && argument.defaultValue !== void 0 && argument.parseArg === void 0) {
          throw new Error(
            `a default value for a required argument is never used: '${argument.name()}'`
          );
        }
        this.registeredArguments.push(argument);
        return this;
      }
      /**
       * Customise or override default help command. By default a help command is automatically added if your command has subcommands.
       *
       * @example
       *    program.helpCommand('help [cmd]');
       *    program.helpCommand('help [cmd]', 'show help');
       *    program.helpCommand(false); // suppress default help command
       *    program.helpCommand(true); // add help command even if no subcommands
       *
       * @param {string|boolean} enableOrNameAndArgs - enable with custom name and/or arguments, or boolean to override whether added
       * @param {string} [description] - custom description
       * @return {Command} `this` command for chaining
       */
      helpCommand(enableOrNameAndArgs, description) {
        if (typeof enableOrNameAndArgs === "boolean") {
          this._addImplicitHelpCommand = enableOrNameAndArgs;
          return this;
        }
        enableOrNameAndArgs = enableOrNameAndArgs ?? "help [command]";
        const [, helpName, helpArgs] = enableOrNameAndArgs.match(/([^ ]+) *(.*)/);
        const helpDescription = description ?? "display help for command";
        const helpCommand = this.createCommand(helpName);
        helpCommand.helpOption(false);
        if (helpArgs) helpCommand.arguments(helpArgs);
        if (helpDescription) helpCommand.description(helpDescription);
        this._addImplicitHelpCommand = true;
        this._helpCommand = helpCommand;
        return this;
      }
      /**
       * Add prepared custom help command.
       *
       * @param {(Command|string|boolean)} helpCommand - custom help command, or deprecated enableOrNameAndArgs as for `.helpCommand()`
       * @param {string} [deprecatedDescription] - deprecated custom description used with custom name only
       * @return {Command} `this` command for chaining
       */
      addHelpCommand(helpCommand, deprecatedDescription) {
        if (typeof helpCommand !== "object") {
          this.helpCommand(helpCommand, deprecatedDescription);
          return this;
        }
        this._addImplicitHelpCommand = true;
        this._helpCommand = helpCommand;
        return this;
      }
      /**
       * Lazy create help command.
       *
       * @return {(Command|null)}
       * @package
       */
      _getHelpCommand() {
        const hasImplicitHelpCommand = this._addImplicitHelpCommand ?? (this.commands.length && !this._actionHandler && !this._findCommand("help"));
        if (hasImplicitHelpCommand) {
          if (this._helpCommand === void 0) {
            this.helpCommand(void 0, void 0);
          }
          return this._helpCommand;
        }
        return null;
      }
      /**
       * Add hook for life cycle event.
       *
       * @param {string} event
       * @param {Function} listener
       * @return {Command} `this` command for chaining
       */
      hook(event, listener) {
        const allowedValues = ["preSubcommand", "preAction", "postAction"];
        if (!allowedValues.includes(event)) {
          throw new Error(`Unexpected value for event passed to hook : '${event}'.
Expecting one of '${allowedValues.join("', '")}'`);
        }
        if (this._lifeCycleHooks[event]) {
          this._lifeCycleHooks[event].push(listener);
        } else {
          this._lifeCycleHooks[event] = [listener];
        }
        return this;
      }
      /**
       * Register callback to use as replacement for calling process.exit.
       *
       * @param {Function} [fn] optional callback which will be passed a CommanderError, defaults to throwing
       * @return {Command} `this` command for chaining
       */
      exitOverride(fn) {
        if (fn) {
          this._exitCallback = fn;
        } else {
          this._exitCallback = (err) => {
            if (err.code !== "commander.executeSubCommandAsync") {
              throw err;
            } else {
            }
          };
        }
        return this;
      }
      /**
       * Call process.exit, and _exitCallback if defined.
       *
       * @param {number} exitCode exit code for using with process.exit
       * @param {string} code an id string representing the error
       * @param {string} message human-readable description of the error
       * @return never
       * @private
       */
      _exit(exitCode, code, message) {
        if (this._exitCallback) {
          this._exitCallback(new CommanderError2(exitCode, code, message));
        }
        process2.exit(exitCode);
      }
      /**
       * Register callback `fn` for the command.
       *
       * @example
       * program
       *   .command('serve')
       *   .description('start service')
       *   .action(function() {
       *      // do work here
       *   });
       *
       * @param {Function} fn
       * @return {Command} `this` command for chaining
       */
      action(fn) {
        const listener = (args) => {
          const expectedArgsCount = this.registeredArguments.length;
          const actionArgs = args.slice(0, expectedArgsCount);
          if (this._storeOptionsAsProperties) {
            actionArgs[expectedArgsCount] = this;
          } else {
            actionArgs[expectedArgsCount] = this.opts();
          }
          actionArgs.push(this);
          return fn.apply(this, actionArgs);
        };
        this._actionHandler = listener;
        return this;
      }
      /**
       * Factory routine to create a new unattached option.
       *
       * See .option() for creating an attached option, which uses this routine to
       * create the option. You can override createOption to return a custom option.
       *
       * @param {string} flags
       * @param {string} [description]
       * @return {Option} new option
       */
      createOption(flags, description) {
        return new Option2(flags, description);
      }
      /**
       * Wrap parseArgs to catch 'commander.invalidArgument'.
       *
       * @param {(Option | Argument)} target
       * @param {string} value
       * @param {*} previous
       * @param {string} invalidArgumentMessage
       * @private
       */
      _callParseArg(target, value, previous, invalidArgumentMessage) {
        try {
          return target.parseArg(value, previous);
        } catch (err) {
          if (err.code === "commander.invalidArgument") {
            const message = `${invalidArgumentMessage} ${err.message}`;
            this.error(message, { exitCode: err.exitCode, code: err.code });
          }
          throw err;
        }
      }
      /**
       * Check for option flag conflicts.
       * Register option if no conflicts found, or throw on conflict.
       *
       * @param {Option} option
       * @private
       */
      _registerOption(option) {
        const matchingOption = option.short && this._findOption(option.short) || option.long && this._findOption(option.long);
        if (matchingOption) {
          const matchingFlag = option.long && this._findOption(option.long) ? option.long : option.short;
          throw new Error(`Cannot add option '${option.flags}'${this._name && ` to command '${this._name}'`} due to conflicting flag '${matchingFlag}'
-  already used by option '${matchingOption.flags}'`);
        }
        this.options.push(option);
      }
      /**
       * Check for command name and alias conflicts with existing commands.
       * Register command if no conflicts found, or throw on conflict.
       *
       * @param {Command} command
       * @private
       */
      _registerCommand(command) {
        const knownBy = (cmd) => {
          return [cmd.name()].concat(cmd.aliases());
        };
        const alreadyUsed = knownBy(command).find(
          (name) => this._findCommand(name)
        );
        if (alreadyUsed) {
          const existingCmd = knownBy(this._findCommand(alreadyUsed)).join("|");
          const newCmd = knownBy(command).join("|");
          throw new Error(
            `cannot add command '${newCmd}' as already have command '${existingCmd}'`
          );
        }
        this.commands.push(command);
      }
      /**
       * Add an option.
       *
       * @param {Option} option
       * @return {Command} `this` command for chaining
       */
      addOption(option) {
        this._registerOption(option);
        const oname = option.name();
        const name = option.attributeName();
        if (option.negate) {
          const positiveLongFlag = option.long.replace(/^--no-/, "--");
          if (!this._findOption(positiveLongFlag)) {
            this.setOptionValueWithSource(
              name,
              option.defaultValue === void 0 ? true : option.defaultValue,
              "default"
            );
          }
        } else if (option.defaultValue !== void 0) {
          this.setOptionValueWithSource(name, option.defaultValue, "default");
        }
        const handleOptionValue = (val, invalidValueMessage, valueSource) => {
          if (val == null && option.presetArg !== void 0) {
            val = option.presetArg;
          }
          const oldValue = this.getOptionValue(name);
          if (val !== null && option.parseArg) {
            val = this._callParseArg(option, val, oldValue, invalidValueMessage);
          } else if (val !== null && option.variadic) {
            val = option._concatValue(val, oldValue);
          }
          if (val == null) {
            if (option.negate) {
              val = false;
            } else if (option.isBoolean() || option.optional) {
              val = true;
            } else {
              val = "";
            }
          }
          this.setOptionValueWithSource(name, val, valueSource);
        };
        this.on("option:" + oname, (val) => {
          const invalidValueMessage = `error: option '${option.flags}' argument '${val}' is invalid.`;
          handleOptionValue(val, invalidValueMessage, "cli");
        });
        if (option.envVar) {
          this.on("optionEnv:" + oname, (val) => {
            const invalidValueMessage = `error: option '${option.flags}' value '${val}' from env '${option.envVar}' is invalid.`;
            handleOptionValue(val, invalidValueMessage, "env");
          });
        }
        return this;
      }
      /**
       * Internal implementation shared by .option() and .requiredOption()
       *
       * @return {Command} `this` command for chaining
       * @private
       */
      _optionEx(config, flags, description, fn, defaultValue) {
        if (typeof flags === "object" && flags instanceof Option2) {
          throw new Error(
            "To add an Option object use addOption() instead of option() or requiredOption()"
          );
        }
        const option = this.createOption(flags, description);
        option.makeOptionMandatory(!!config.mandatory);
        if (typeof fn === "function") {
          option.default(defaultValue).argParser(fn);
        } else if (fn instanceof RegExp) {
          const regex = fn;
          fn = (val, def) => {
            const m = regex.exec(val);
            return m ? m[0] : def;
          };
          option.default(defaultValue).argParser(fn);
        } else {
          option.default(fn);
        }
        return this.addOption(option);
      }
      /**
       * Define option with `flags`, `description`, and optional argument parsing function or `defaultValue` or both.
       *
       * The `flags` string contains the short and/or long flags, separated by comma, a pipe or space. A required
       * option-argument is indicated by `<>` and an optional option-argument by `[]`.
       *
       * See the README for more details, and see also addOption() and requiredOption().
       *
       * @example
       * program
       *     .option('-p, --pepper', 'add pepper')
       *     .option('-p, --pizza-type <TYPE>', 'type of pizza') // required option-argument
       *     .option('-c, --cheese [CHEESE]', 'add extra cheese', 'mozzarella') // optional option-argument with default
       *     .option('-t, --tip <VALUE>', 'add tip to purchase cost', parseFloat) // custom parse function
       *
       * @param {string} flags
       * @param {string} [description]
       * @param {(Function|*)} [parseArg] - custom option processing function or default value
       * @param {*} [defaultValue]
       * @return {Command} `this` command for chaining
       */
      option(flags, description, parseArg, defaultValue) {
        return this._optionEx({}, flags, description, parseArg, defaultValue);
      }
      /**
       * Add a required option which must have a value after parsing. This usually means
       * the option must be specified on the command line. (Otherwise the same as .option().)
       *
       * The `flags` string contains the short and/or long flags, separated by comma, a pipe or space.
       *
       * @param {string} flags
       * @param {string} [description]
       * @param {(Function|*)} [parseArg] - custom option processing function or default value
       * @param {*} [defaultValue]
       * @return {Command} `this` command for chaining
       */
      requiredOption(flags, description, parseArg, defaultValue) {
        return this._optionEx(
          { mandatory: true },
          flags,
          description,
          parseArg,
          defaultValue
        );
      }
      /**
       * Alter parsing of short flags with optional values.
       *
       * @example
       * // for `.option('-f,--flag [value]'):
       * program.combineFlagAndOptionalValue(true);  // `-f80` is treated like `--flag=80`, this is the default behaviour
       * program.combineFlagAndOptionalValue(false) // `-fb` is treated like `-f -b`
       *
       * @param {boolean} [combine] - if `true` or omitted, an optional value can be specified directly after the flag.
       * @return {Command} `this` command for chaining
       */
      combineFlagAndOptionalValue(combine = true) {
        this._combineFlagAndOptionalValue = !!combine;
        return this;
      }
      /**
       * Allow unknown options on the command line.
       *
       * @param {boolean} [allowUnknown] - if `true` or omitted, no error will be thrown for unknown options.
       * @return {Command} `this` command for chaining
       */
      allowUnknownOption(allowUnknown = true) {
        this._allowUnknownOption = !!allowUnknown;
        return this;
      }
      /**
       * Allow excess command-arguments on the command line. Pass false to make excess arguments an error.
       *
       * @param {boolean} [allowExcess] - if `true` or omitted, no error will be thrown for excess arguments.
       * @return {Command} `this` command for chaining
       */
      allowExcessArguments(allowExcess = true) {
        this._allowExcessArguments = !!allowExcess;
        return this;
      }
      /**
       * Enable positional options. Positional means global options are specified before subcommands which lets
       * subcommands reuse the same option names, and also enables subcommands to turn on passThroughOptions.
       * The default behaviour is non-positional and global options may appear anywhere on the command line.
       *
       * @param {boolean} [positional]
       * @return {Command} `this` command for chaining
       */
      enablePositionalOptions(positional = true) {
        this._enablePositionalOptions = !!positional;
        return this;
      }
      /**
       * Pass through options that come after command-arguments rather than treat them as command-options,
       * so actual command-options come before command-arguments. Turning this on for a subcommand requires
       * positional options to have been enabled on the program (parent commands).
       * The default behaviour is non-positional and options may appear before or after command-arguments.
       *
       * @param {boolean} [passThrough] for unknown options.
       * @return {Command} `this` command for chaining
       */
      passThroughOptions(passThrough = true) {
        this._passThroughOptions = !!passThrough;
        this._checkForBrokenPassThrough();
        return this;
      }
      /**
       * @private
       */
      _checkForBrokenPassThrough() {
        if (this.parent && this._passThroughOptions && !this.parent._enablePositionalOptions) {
          throw new Error(
            `passThroughOptions cannot be used for '${this._name}' without turning on enablePositionalOptions for parent command(s)`
          );
        }
      }
      /**
       * Whether to store option values as properties on command object,
       * or store separately (specify false). In both cases the option values can be accessed using .opts().
       *
       * @param {boolean} [storeAsProperties=true]
       * @return {Command} `this` command for chaining
       */
      storeOptionsAsProperties(storeAsProperties = true) {
        if (this.options.length) {
          throw new Error("call .storeOptionsAsProperties() before adding options");
        }
        if (Object.keys(this._optionValues).length) {
          throw new Error(
            "call .storeOptionsAsProperties() before setting option values"
          );
        }
        this._storeOptionsAsProperties = !!storeAsProperties;
        return this;
      }
      /**
       * Retrieve option value.
       *
       * @param {string} key
       * @return {object} value
       */
      getOptionValue(key) {
        if (this._storeOptionsAsProperties) {
          return this[key];
        }
        return this._optionValues[key];
      }
      /**
       * Store option value.
       *
       * @param {string} key
       * @param {object} value
       * @return {Command} `this` command for chaining
       */
      setOptionValue(key, value) {
        return this.setOptionValueWithSource(key, value, void 0);
      }
      /**
       * Store option value and where the value came from.
       *
       * @param {string} key
       * @param {object} value
       * @param {string} source - expected values are default/config/env/cli/implied
       * @return {Command} `this` command for chaining
       */
      setOptionValueWithSource(key, value, source) {
        if (this._storeOptionsAsProperties) {
          this[key] = value;
        } else {
          this._optionValues[key] = value;
        }
        this._optionValueSources[key] = source;
        return this;
      }
      /**
       * Get source of option value.
       * Expected values are default | config | env | cli | implied
       *
       * @param {string} key
       * @return {string}
       */
      getOptionValueSource(key) {
        return this._optionValueSources[key];
      }
      /**
       * Get source of option value. See also .optsWithGlobals().
       * Expected values are default | config | env | cli | implied
       *
       * @param {string} key
       * @return {string}
       */
      getOptionValueSourceWithGlobals(key) {
        let source;
        this._getCommandAndAncestors().forEach((cmd) => {
          if (cmd.getOptionValueSource(key) !== void 0) {
            source = cmd.getOptionValueSource(key);
          }
        });
        return source;
      }
      /**
       * Get user arguments from implied or explicit arguments.
       * Side-effects: set _scriptPath if args included script. Used for default program name, and subcommand searches.
       *
       * @private
       */
      _prepareUserArgs(argv, parseOptions) {
        if (argv !== void 0 && !Array.isArray(argv)) {
          throw new Error("first parameter to parse must be array or undefined");
        }
        parseOptions = parseOptions || {};
        if (argv === void 0 && parseOptions.from === void 0) {
          if (process2.versions?.electron) {
            parseOptions.from = "electron";
          }
          const execArgv = process2.execArgv ?? [];
          if (execArgv.includes("-e") || execArgv.includes("--eval") || execArgv.includes("-p") || execArgv.includes("--print")) {
            parseOptions.from = "eval";
          }
        }
        if (argv === void 0) {
          argv = process2.argv;
        }
        this.rawArgs = argv.slice();
        let userArgs;
        switch (parseOptions.from) {
          case void 0:
          case "node":
            this._scriptPath = argv[1];
            userArgs = argv.slice(2);
            break;
          case "electron":
            if (process2.defaultApp) {
              this._scriptPath = argv[1];
              userArgs = argv.slice(2);
            } else {
              userArgs = argv.slice(1);
            }
            break;
          case "user":
            userArgs = argv.slice(0);
            break;
          case "eval":
            userArgs = argv.slice(1);
            break;
          default:
            throw new Error(
              `unexpected parse option { from: '${parseOptions.from}' }`
            );
        }
        if (!this._name && this._scriptPath)
          this.nameFromFilename(this._scriptPath);
        this._name = this._name || "program";
        return userArgs;
      }
      /**
       * Parse `argv`, setting options and invoking commands when defined.
       *
       * Use parseAsync instead of parse if any of your action handlers are async.
       *
       * Call with no parameters to parse `process.argv`. Detects Electron and special node options like `node --eval`. Easy mode!
       *
       * Or call with an array of strings to parse, and optionally where the user arguments start by specifying where the arguments are `from`:
       * - `'node'`: default, `argv[0]` is the application and `argv[1]` is the script being run, with user arguments after that
       * - `'electron'`: `argv[0]` is the application and `argv[1]` varies depending on whether the electron application is packaged
       * - `'user'`: just user arguments
       *
       * @example
       * program.parse(); // parse process.argv and auto-detect electron and special node flags
       * program.parse(process.argv); // assume argv[0] is app and argv[1] is script
       * program.parse(my-args, { from: 'user' }); // just user supplied arguments, nothing special about argv[0]
       *
       * @param {string[]} [argv] - optional, defaults to process.argv
       * @param {object} [parseOptions] - optionally specify style of options with from: node/user/electron
       * @param {string} [parseOptions.from] - where the args are from: 'node', 'user', 'electron'
       * @return {Command} `this` command for chaining
       */
      parse(argv, parseOptions) {
        const userArgs = this._prepareUserArgs(argv, parseOptions);
        this._parseCommand([], userArgs);
        return this;
      }
      /**
       * Parse `argv`, setting options and invoking commands when defined.
       *
       * Call with no parameters to parse `process.argv`. Detects Electron and special node options like `node --eval`. Easy mode!
       *
       * Or call with an array of strings to parse, and optionally where the user arguments start by specifying where the arguments are `from`:
       * - `'node'`: default, `argv[0]` is the application and `argv[1]` is the script being run, with user arguments after that
       * - `'electron'`: `argv[0]` is the application and `argv[1]` varies depending on whether the electron application is packaged
       * - `'user'`: just user arguments
       *
       * @example
       * await program.parseAsync(); // parse process.argv and auto-detect electron and special node flags
       * await program.parseAsync(process.argv); // assume argv[0] is app and argv[1] is script
       * await program.parseAsync(my-args, { from: 'user' }); // just user supplied arguments, nothing special about argv[0]
       *
       * @param {string[]} [argv]
       * @param {object} [parseOptions]
       * @param {string} parseOptions.from - where the args are from: 'node', 'user', 'electron'
       * @return {Promise}
       */
      async parseAsync(argv, parseOptions) {
        const userArgs = this._prepareUserArgs(argv, parseOptions);
        await this._parseCommand([], userArgs);
        return this;
      }
      /**
       * Execute a sub-command executable.
       *
       * @private
       */
      _executeSubCommand(subcommand, args) {
        args = args.slice();
        let launchWithNode = false;
        const sourceExt = [".js", ".ts", ".tsx", ".mjs", ".cjs"];
        function findFile(baseDir, baseName) {
          const localBin = path3.resolve(baseDir, baseName);
          if (fs2.existsSync(localBin)) return localBin;
          if (sourceExt.includes(path3.extname(baseName))) return void 0;
          const foundExt = sourceExt.find(
            (ext) => fs2.existsSync(`${localBin}${ext}`)
          );
          if (foundExt) return `${localBin}${foundExt}`;
          return void 0;
        }
        this._checkForMissingMandatoryOptions();
        this._checkForConflictingOptions();
        let executableFile = subcommand._executableFile || `${this._name}-${subcommand._name}`;
        let executableDir = this._executableDir || "";
        if (this._scriptPath) {
          let resolvedScriptPath;
          try {
            resolvedScriptPath = fs2.realpathSync(this._scriptPath);
          } catch (err) {
            resolvedScriptPath = this._scriptPath;
          }
          executableDir = path3.resolve(
            path3.dirname(resolvedScriptPath),
            executableDir
          );
        }
        if (executableDir) {
          let localFile = findFile(executableDir, executableFile);
          if (!localFile && !subcommand._executableFile && this._scriptPath) {
            const legacyName = path3.basename(
              this._scriptPath,
              path3.extname(this._scriptPath)
            );
            if (legacyName !== this._name) {
              localFile = findFile(
                executableDir,
                `${legacyName}-${subcommand._name}`
              );
            }
          }
          executableFile = localFile || executableFile;
        }
        launchWithNode = sourceExt.includes(path3.extname(executableFile));
        let proc;
        if (process2.platform !== "win32") {
          if (launchWithNode) {
            args.unshift(executableFile);
            args = incrementNodeInspectorPort(process2.execArgv).concat(args);
            proc = childProcess.spawn(process2.argv[0], args, { stdio: "inherit" });
          } else {
            proc = childProcess.spawn(executableFile, args, { stdio: "inherit" });
          }
        } else {
          args.unshift(executableFile);
          args = incrementNodeInspectorPort(process2.execArgv).concat(args);
          proc = childProcess.spawn(process2.execPath, args, { stdio: "inherit" });
        }
        if (!proc.killed) {
          const signals = ["SIGUSR1", "SIGUSR2", "SIGTERM", "SIGINT", "SIGHUP"];
          signals.forEach((signal) => {
            process2.on(signal, () => {
              if (proc.killed === false && proc.exitCode === null) {
                proc.kill(signal);
              }
            });
          });
        }
        const exitCallback = this._exitCallback;
        proc.on("close", (code) => {
          code = code ?? 1;
          if (!exitCallback) {
            process2.exit(code);
          } else {
            exitCallback(
              new CommanderError2(
                code,
                "commander.executeSubCommandAsync",
                "(close)"
              )
            );
          }
        });
        proc.on("error", (err) => {
          if (err.code === "ENOENT") {
            const executableDirMessage = executableDir ? `searched for local subcommand relative to directory '${executableDir}'` : "no directory for search for local subcommand, use .executableDir() to supply a custom directory";
            const executableMissing = `'${executableFile}' does not exist
 - if '${subcommand._name}' is not meant to be an executable command, remove description parameter from '.command()' and use '.description()' instead
 - if the default executable name is not suitable, use the executableFile option to supply a custom name or path
 - ${executableDirMessage}`;
            throw new Error(executableMissing);
          } else if (err.code === "EACCES") {
            throw new Error(`'${executableFile}' not executable`);
          }
          if (!exitCallback) {
            process2.exit(1);
          } else {
            const wrappedError = new CommanderError2(
              1,
              "commander.executeSubCommandAsync",
              "(error)"
            );
            wrappedError.nestedError = err;
            exitCallback(wrappedError);
          }
        });
        this.runningCommand = proc;
      }
      /**
       * @private
       */
      _dispatchSubcommand(commandName, operands, unknown) {
        const subCommand = this._findCommand(commandName);
        if (!subCommand) this.help({ error: true });
        let promiseChain;
        promiseChain = this._chainOrCallSubCommandHook(
          promiseChain,
          subCommand,
          "preSubcommand"
        );
        promiseChain = this._chainOrCall(promiseChain, () => {
          if (subCommand._executableHandler) {
            this._executeSubCommand(subCommand, operands.concat(unknown));
          } else {
            return subCommand._parseCommand(operands, unknown);
          }
        });
        return promiseChain;
      }
      /**
       * Invoke help directly if possible, or dispatch if necessary.
       * e.g. help foo
       *
       * @private
       */
      _dispatchHelpCommand(subcommandName) {
        if (!subcommandName) {
          this.help();
        }
        const subCommand = this._findCommand(subcommandName);
        if (subCommand && !subCommand._executableHandler) {
          subCommand.help();
        }
        return this._dispatchSubcommand(
          subcommandName,
          [],
          [this._getHelpOption()?.long ?? this._getHelpOption()?.short ?? "--help"]
        );
      }
      /**
       * Check this.args against expected this.registeredArguments.
       *
       * @private
       */
      _checkNumberOfArguments() {
        this.registeredArguments.forEach((arg, i) => {
          if (arg.required && this.args[i] == null) {
            this.missingArgument(arg.name());
          }
        });
        if (this.registeredArguments.length > 0 && this.registeredArguments[this.registeredArguments.length - 1].variadic) {
          return;
        }
        if (this.args.length > this.registeredArguments.length) {
          this._excessArguments(this.args);
        }
      }
      /**
       * Process this.args using this.registeredArguments and save as this.processedArgs!
       *
       * @private
       */
      _processArguments() {
        const myParseArg = (argument, value, previous) => {
          let parsedValue = value;
          if (value !== null && argument.parseArg) {
            const invalidValueMessage = `error: command-argument value '${value}' is invalid for argument '${argument.name()}'.`;
            parsedValue = this._callParseArg(
              argument,
              value,
              previous,
              invalidValueMessage
            );
          }
          return parsedValue;
        };
        this._checkNumberOfArguments();
        const processedArgs = [];
        this.registeredArguments.forEach((declaredArg, index) => {
          let value = declaredArg.defaultValue;
          if (declaredArg.variadic) {
            if (index < this.args.length) {
              value = this.args.slice(index);
              if (declaredArg.parseArg) {
                value = value.reduce((processed, v) => {
                  return myParseArg(declaredArg, v, processed);
                }, declaredArg.defaultValue);
              }
            } else if (value === void 0) {
              value = [];
            }
          } else if (index < this.args.length) {
            value = this.args[index];
            if (declaredArg.parseArg) {
              value = myParseArg(declaredArg, value, declaredArg.defaultValue);
            }
          }
          processedArgs[index] = value;
        });
        this.processedArgs = processedArgs;
      }
      /**
       * Once we have a promise we chain, but call synchronously until then.
       *
       * @param {(Promise|undefined)} promise
       * @param {Function} fn
       * @return {(Promise|undefined)}
       * @private
       */
      _chainOrCall(promise, fn) {
        if (promise && promise.then && typeof promise.then === "function") {
          return promise.then(() => fn());
        }
        return fn();
      }
      /**
       *
       * @param {(Promise|undefined)} promise
       * @param {string} event
       * @return {(Promise|undefined)}
       * @private
       */
      _chainOrCallHooks(promise, event) {
        let result = promise;
        const hooks = [];
        this._getCommandAndAncestors().reverse().filter((cmd) => cmd._lifeCycleHooks[event] !== void 0).forEach((hookedCommand) => {
          hookedCommand._lifeCycleHooks[event].forEach((callback) => {
            hooks.push({ hookedCommand, callback });
          });
        });
        if (event === "postAction") {
          hooks.reverse();
        }
        hooks.forEach((hookDetail) => {
          result = this._chainOrCall(result, () => {
            return hookDetail.callback(hookDetail.hookedCommand, this);
          });
        });
        return result;
      }
      /**
       *
       * @param {(Promise|undefined)} promise
       * @param {Command} subCommand
       * @param {string} event
       * @return {(Promise|undefined)}
       * @private
       */
      _chainOrCallSubCommandHook(promise, subCommand, event) {
        let result = promise;
        if (this._lifeCycleHooks[event] !== void 0) {
          this._lifeCycleHooks[event].forEach((hook) => {
            result = this._chainOrCall(result, () => {
              return hook(this, subCommand);
            });
          });
        }
        return result;
      }
      /**
       * Process arguments in context of this command.
       * Returns action result, in case it is a promise.
       *
       * @private
       */
      _parseCommand(operands, unknown) {
        const parsed = this.parseOptions(unknown);
        this._parseOptionsEnv();
        this._parseOptionsImplied();
        operands = operands.concat(parsed.operands);
        unknown = parsed.unknown;
        this.args = operands.concat(unknown);
        if (operands && this._findCommand(operands[0])) {
          return this._dispatchSubcommand(operands[0], operands.slice(1), unknown);
        }
        if (this._getHelpCommand() && operands[0] === this._getHelpCommand().name()) {
          return this._dispatchHelpCommand(operands[1]);
        }
        if (this._defaultCommandName) {
          this._outputHelpIfRequested(unknown);
          return this._dispatchSubcommand(
            this._defaultCommandName,
            operands,
            unknown
          );
        }
        if (this.commands.length && this.args.length === 0 && !this._actionHandler && !this._defaultCommandName) {
          this.help({ error: true });
        }
        this._outputHelpIfRequested(parsed.unknown);
        this._checkForMissingMandatoryOptions();
        this._checkForConflictingOptions();
        const checkForUnknownOptions = () => {
          if (parsed.unknown.length > 0) {
            this.unknownOption(parsed.unknown[0]);
          }
        };
        const commandEvent = `command:${this.name()}`;
        if (this._actionHandler) {
          checkForUnknownOptions();
          this._processArguments();
          let promiseChain;
          promiseChain = this._chainOrCallHooks(promiseChain, "preAction");
          promiseChain = this._chainOrCall(
            promiseChain,
            () => this._actionHandler(this.processedArgs)
          );
          if (this.parent) {
            promiseChain = this._chainOrCall(promiseChain, () => {
              this.parent.emit(commandEvent, operands, unknown);
            });
          }
          promiseChain = this._chainOrCallHooks(promiseChain, "postAction");
          return promiseChain;
        }
        if (this.parent && this.parent.listenerCount(commandEvent)) {
          checkForUnknownOptions();
          this._processArguments();
          this.parent.emit(commandEvent, operands, unknown);
        } else if (operands.length) {
          if (this._findCommand("*")) {
            return this._dispatchSubcommand("*", operands, unknown);
          }
          if (this.listenerCount("command:*")) {
            this.emit("command:*", operands, unknown);
          } else if (this.commands.length) {
            this.unknownCommand();
          } else {
            checkForUnknownOptions();
            this._processArguments();
          }
        } else if (this.commands.length) {
          checkForUnknownOptions();
          this.help({ error: true });
        } else {
          checkForUnknownOptions();
          this._processArguments();
        }
      }
      /**
       * Find matching command.
       *
       * @private
       * @return {Command | undefined}
       */
      _findCommand(name) {
        if (!name) return void 0;
        return this.commands.find(
          (cmd) => cmd._name === name || cmd._aliases.includes(name)
        );
      }
      /**
       * Return an option matching `arg` if any.
       *
       * @param {string} arg
       * @return {Option}
       * @package
       */
      _findOption(arg) {
        return this.options.find((option) => option.is(arg));
      }
      /**
       * Display an error message if a mandatory option does not have a value.
       * Called after checking for help flags in leaf subcommand.
       *
       * @private
       */
      _checkForMissingMandatoryOptions() {
        this._getCommandAndAncestors().forEach((cmd) => {
          cmd.options.forEach((anOption) => {
            if (anOption.mandatory && cmd.getOptionValue(anOption.attributeName()) === void 0) {
              cmd.missingMandatoryOptionValue(anOption);
            }
          });
        });
      }
      /**
       * Display an error message if conflicting options are used together in this.
       *
       * @private
       */
      _checkForConflictingLocalOptions() {
        const definedNonDefaultOptions = this.options.filter((option) => {
          const optionKey = option.attributeName();
          if (this.getOptionValue(optionKey) === void 0) {
            return false;
          }
          return this.getOptionValueSource(optionKey) !== "default";
        });
        const optionsWithConflicting = definedNonDefaultOptions.filter(
          (option) => option.conflictsWith.length > 0
        );
        optionsWithConflicting.forEach((option) => {
          const conflictingAndDefined = definedNonDefaultOptions.find(
            (defined) => option.conflictsWith.includes(defined.attributeName())
          );
          if (conflictingAndDefined) {
            this._conflictingOption(option, conflictingAndDefined);
          }
        });
      }
      /**
       * Display an error message if conflicting options are used together.
       * Called after checking for help flags in leaf subcommand.
       *
       * @private
       */
      _checkForConflictingOptions() {
        this._getCommandAndAncestors().forEach((cmd) => {
          cmd._checkForConflictingLocalOptions();
        });
      }
      /**
       * Parse options from `argv` removing known options,
       * and return argv split into operands and unknown arguments.
       *
       * Examples:
       *
       *     argv => operands, unknown
       *     --known kkk op => [op], []
       *     op --known kkk => [op], []
       *     sub --unknown uuu op => [sub], [--unknown uuu op]
       *     sub -- --unknown uuu op => [sub --unknown uuu op], []
       *
       * @param {string[]} argv
       * @return {{operands: string[], unknown: string[]}}
       */
      parseOptions(argv) {
        const operands = [];
        const unknown = [];
        let dest = operands;
        const args = argv.slice();
        function maybeOption(arg) {
          return arg.length > 1 && arg[0] === "-";
        }
        let activeVariadicOption = null;
        while (args.length) {
          const arg = args.shift();
          if (arg === "--") {
            if (dest === unknown) dest.push(arg);
            dest.push(...args);
            break;
          }
          if (activeVariadicOption && !maybeOption(arg)) {
            this.emit(`option:${activeVariadicOption.name()}`, arg);
            continue;
          }
          activeVariadicOption = null;
          if (maybeOption(arg)) {
            const option = this._findOption(arg);
            if (option) {
              if (option.required) {
                const value = args.shift();
                if (value === void 0) this.optionMissingArgument(option);
                this.emit(`option:${option.name()}`, value);
              } else if (option.optional) {
                let value = null;
                if (args.length > 0 && !maybeOption(args[0])) {
                  value = args.shift();
                }
                this.emit(`option:${option.name()}`, value);
              } else {
                this.emit(`option:${option.name()}`);
              }
              activeVariadicOption = option.variadic ? option : null;
              continue;
            }
          }
          if (arg.length > 2 && arg[0] === "-" && arg[1] !== "-") {
            const option = this._findOption(`-${arg[1]}`);
            if (option) {
              if (option.required || option.optional && this._combineFlagAndOptionalValue) {
                this.emit(`option:${option.name()}`, arg.slice(2));
              } else {
                this.emit(`option:${option.name()}`);
                args.unshift(`-${arg.slice(2)}`);
              }
              continue;
            }
          }
          if (/^--[^=]+=/.test(arg)) {
            const index = arg.indexOf("=");
            const option = this._findOption(arg.slice(0, index));
            if (option && (option.required || option.optional)) {
              this.emit(`option:${option.name()}`, arg.slice(index + 1));
              continue;
            }
          }
          if (maybeOption(arg)) {
            dest = unknown;
          }
          if ((this._enablePositionalOptions || this._passThroughOptions) && operands.length === 0 && unknown.length === 0) {
            if (this._findCommand(arg)) {
              operands.push(arg);
              if (args.length > 0) unknown.push(...args);
              break;
            } else if (this._getHelpCommand() && arg === this._getHelpCommand().name()) {
              operands.push(arg);
              if (args.length > 0) operands.push(...args);
              break;
            } else if (this._defaultCommandName) {
              unknown.push(arg);
              if (args.length > 0) unknown.push(...args);
              break;
            }
          }
          if (this._passThroughOptions) {
            dest.push(arg);
            if (args.length > 0) dest.push(...args);
            break;
          }
          dest.push(arg);
        }
        return { operands, unknown };
      }
      /**
       * Return an object containing local option values as key-value pairs.
       *
       * @return {object}
       */
      opts() {
        if (this._storeOptionsAsProperties) {
          const result = {};
          const len = this.options.length;
          for (let i = 0; i < len; i++) {
            const key = this.options[i].attributeName();
            result[key] = key === this._versionOptionName ? this._version : this[key];
          }
          return result;
        }
        return this._optionValues;
      }
      /**
       * Return an object containing merged local and global option values as key-value pairs.
       *
       * @return {object}
       */
      optsWithGlobals() {
        return this._getCommandAndAncestors().reduce(
          (combinedOptions, cmd) => Object.assign(combinedOptions, cmd.opts()),
          {}
        );
      }
      /**
       * Display error message and exit (or call exitOverride).
       *
       * @param {string} message
       * @param {object} [errorOptions]
       * @param {string} [errorOptions.code] - an id string representing the error
       * @param {number} [errorOptions.exitCode] - used with process.exit
       */
      error(message, errorOptions) {
        this._outputConfiguration.outputError(
          `${message}
`,
          this._outputConfiguration.writeErr
        );
        if (typeof this._showHelpAfterError === "string") {
          this._outputConfiguration.writeErr(`${this._showHelpAfterError}
`);
        } else if (this._showHelpAfterError) {
          this._outputConfiguration.writeErr("\n");
          this.outputHelp({ error: true });
        }
        const config = errorOptions || {};
        const exitCode = config.exitCode || 1;
        const code = config.code || "commander.error";
        this._exit(exitCode, code, message);
      }
      /**
       * Apply any option related environment variables, if option does
       * not have a value from cli or client code.
       *
       * @private
       */
      _parseOptionsEnv() {
        this.options.forEach((option) => {
          if (option.envVar && option.envVar in process2.env) {
            const optionKey = option.attributeName();
            if (this.getOptionValue(optionKey) === void 0 || ["default", "config", "env"].includes(
              this.getOptionValueSource(optionKey)
            )) {
              if (option.required || option.optional) {
                this.emit(`optionEnv:${option.name()}`, process2.env[option.envVar]);
              } else {
                this.emit(`optionEnv:${option.name()}`);
              }
            }
          }
        });
      }
      /**
       * Apply any implied option values, if option is undefined or default value.
       *
       * @private
       */
      _parseOptionsImplied() {
        const dualHelper = new DualOptions(this.options);
        const hasCustomOptionValue = (optionKey) => {
          return this.getOptionValue(optionKey) !== void 0 && !["default", "implied"].includes(this.getOptionValueSource(optionKey));
        };
        this.options.filter(
          (option) => option.implied !== void 0 && hasCustomOptionValue(option.attributeName()) && dualHelper.valueFromOption(
            this.getOptionValue(option.attributeName()),
            option
          )
        ).forEach((option) => {
          Object.keys(option.implied).filter((impliedKey) => !hasCustomOptionValue(impliedKey)).forEach((impliedKey) => {
            this.setOptionValueWithSource(
              impliedKey,
              option.implied[impliedKey],
              "implied"
            );
          });
        });
      }
      /**
       * Argument `name` is missing.
       *
       * @param {string} name
       * @private
       */
      missingArgument(name) {
        const message = `error: missing required argument '${name}'`;
        this.error(message, { code: "commander.missingArgument" });
      }
      /**
       * `Option` is missing an argument.
       *
       * @param {Option} option
       * @private
       */
      optionMissingArgument(option) {
        const message = `error: option '${option.flags}' argument missing`;
        this.error(message, { code: "commander.optionMissingArgument" });
      }
      /**
       * `Option` does not have a value, and is a mandatory option.
       *
       * @param {Option} option
       * @private
       */
      missingMandatoryOptionValue(option) {
        const message = `error: required option '${option.flags}' not specified`;
        this.error(message, { code: "commander.missingMandatoryOptionValue" });
      }
      /**
       * `Option` conflicts with another option.
       *
       * @param {Option} option
       * @param {Option} conflictingOption
       * @private
       */
      _conflictingOption(option, conflictingOption) {
        const findBestOptionFromValue = (option2) => {
          const optionKey = option2.attributeName();
          const optionValue = this.getOptionValue(optionKey);
          const negativeOption = this.options.find(
            (target) => target.negate && optionKey === target.attributeName()
          );
          const positiveOption = this.options.find(
            (target) => !target.negate && optionKey === target.attributeName()
          );
          if (negativeOption && (negativeOption.presetArg === void 0 && optionValue === false || negativeOption.presetArg !== void 0 && optionValue === negativeOption.presetArg)) {
            return negativeOption;
          }
          return positiveOption || option2;
        };
        const getErrorMessage = (option2) => {
          const bestOption = findBestOptionFromValue(option2);
          const optionKey = bestOption.attributeName();
          const source = this.getOptionValueSource(optionKey);
          if (source === "env") {
            return `environment variable '${bestOption.envVar}'`;
          }
          return `option '${bestOption.flags}'`;
        };
        const message = `error: ${getErrorMessage(option)} cannot be used with ${getErrorMessage(conflictingOption)}`;
        this.error(message, { code: "commander.conflictingOption" });
      }
      /**
       * Unknown option `flag`.
       *
       * @param {string} flag
       * @private
       */
      unknownOption(flag) {
        if (this._allowUnknownOption) return;
        let suggestion = "";
        if (flag.startsWith("--") && this._showSuggestionAfterError) {
          let candidateFlags = [];
          let command = this;
          do {
            const moreFlags = command.createHelp().visibleOptions(command).filter((option) => option.long).map((option) => option.long);
            candidateFlags = candidateFlags.concat(moreFlags);
            command = command.parent;
          } while (command && !command._enablePositionalOptions);
          suggestion = suggestSimilar(flag, candidateFlags);
        }
        const message = `error: unknown option '${flag}'${suggestion}`;
        this.error(message, { code: "commander.unknownOption" });
      }
      /**
       * Excess arguments, more than expected.
       *
       * @param {string[]} receivedArgs
       * @private
       */
      _excessArguments(receivedArgs) {
        if (this._allowExcessArguments) return;
        const expected = this.registeredArguments.length;
        const s = expected === 1 ? "" : "s";
        const forSubcommand = this.parent ? ` for '${this.name()}'` : "";
        const message = `error: too many arguments${forSubcommand}. Expected ${expected} argument${s} but got ${receivedArgs.length}.`;
        this.error(message, { code: "commander.excessArguments" });
      }
      /**
       * Unknown command.
       *
       * @private
       */
      unknownCommand() {
        const unknownName = this.args[0];
        let suggestion = "";
        if (this._showSuggestionAfterError) {
          const candidateNames = [];
          this.createHelp().visibleCommands(this).forEach((command) => {
            candidateNames.push(command.name());
            if (command.alias()) candidateNames.push(command.alias());
          });
          suggestion = suggestSimilar(unknownName, candidateNames);
        }
        const message = `error: unknown command '${unknownName}'${suggestion}`;
        this.error(message, { code: "commander.unknownCommand" });
      }
      /**
       * Get or set the program version.
       *
       * This method auto-registers the "-V, --version" option which will print the version number.
       *
       * You can optionally supply the flags and description to override the defaults.
       *
       * @param {string} [str]
       * @param {string} [flags]
       * @param {string} [description]
       * @return {(this | string | undefined)} `this` command for chaining, or version string if no arguments
       */
      version(str, flags, description) {
        if (str === void 0) return this._version;
        this._version = str;
        flags = flags || "-V, --version";
        description = description || "output the version number";
        const versionOption = this.createOption(flags, description);
        this._versionOptionName = versionOption.attributeName();
        this._registerOption(versionOption);
        this.on("option:" + versionOption.name(), () => {
          this._outputConfiguration.writeOut(`${str}
`);
          this._exit(0, "commander.version", str);
        });
        return this;
      }
      /**
       * Set the description.
       *
       * @param {string} [str]
       * @param {object} [argsDescription]
       * @return {(string|Command)}
       */
      description(str, argsDescription) {
        if (str === void 0 && argsDescription === void 0)
          return this._description;
        this._description = str;
        if (argsDescription) {
          this._argsDescription = argsDescription;
        }
        return this;
      }
      /**
       * Set the summary. Used when listed as subcommand of parent.
       *
       * @param {string} [str]
       * @return {(string|Command)}
       */
      summary(str) {
        if (str === void 0) return this._summary;
        this._summary = str;
        return this;
      }
      /**
       * Set an alias for the command.
       *
       * You may call more than once to add multiple aliases. Only the first alias is shown in the auto-generated help.
       *
       * @param {string} [alias]
       * @return {(string|Command)}
       */
      alias(alias) {
        if (alias === void 0) return this._aliases[0];
        let command = this;
        if (this.commands.length !== 0 && this.commands[this.commands.length - 1]._executableHandler) {
          command = this.commands[this.commands.length - 1];
        }
        if (alias === command._name)
          throw new Error("Command alias can't be the same as its name");
        const matchingCommand = this.parent?._findCommand(alias);
        if (matchingCommand) {
          const existingCmd = [matchingCommand.name()].concat(matchingCommand.aliases()).join("|");
          throw new Error(
            `cannot add alias '${alias}' to command '${this.name()}' as already have command '${existingCmd}'`
          );
        }
        command._aliases.push(alias);
        return this;
      }
      /**
       * Set aliases for the command.
       *
       * Only the first alias is shown in the auto-generated help.
       *
       * @param {string[]} [aliases]
       * @return {(string[]|Command)}
       */
      aliases(aliases) {
        if (aliases === void 0) return this._aliases;
        aliases.forEach((alias) => this.alias(alias));
        return this;
      }
      /**
       * Set / get the command usage `str`.
       *
       * @param {string} [str]
       * @return {(string|Command)}
       */
      usage(str) {
        if (str === void 0) {
          if (this._usage) return this._usage;
          const args = this.registeredArguments.map((arg) => {
            return humanReadableArgName(arg);
          });
          return [].concat(
            this.options.length || this._helpOption !== null ? "[options]" : [],
            this.commands.length ? "[command]" : [],
            this.registeredArguments.length ? args : []
          ).join(" ");
        }
        this._usage = str;
        return this;
      }
      /**
       * Get or set the name of the command.
       *
       * @param {string} [str]
       * @return {(string|Command)}
       */
      name(str) {
        if (str === void 0) return this._name;
        this._name = str;
        return this;
      }
      /**
       * Set the name of the command from script filename, such as process.argv[1],
       * or require.main.filename, or __filename.
       *
       * (Used internally and public although not documented in README.)
       *
       * @example
       * program.nameFromFilename(require.main.filename);
       *
       * @param {string} filename
       * @return {Command}
       */
      nameFromFilename(filename) {
        this._name = path3.basename(filename, path3.extname(filename));
        return this;
      }
      /**
       * Get or set the directory for searching for executable subcommands of this command.
       *
       * @example
       * program.executableDir(__dirname);
       * // or
       * program.executableDir('subcommands');
       *
       * @param {string} [path]
       * @return {(string|null|Command)}
       */
      executableDir(path4) {
        if (path4 === void 0) return this._executableDir;
        this._executableDir = path4;
        return this;
      }
      /**
       * Return program help documentation.
       *
       * @param {{ error: boolean }} [contextOptions] - pass {error:true} to wrap for stderr instead of stdout
       * @return {string}
       */
      helpInformation(contextOptions) {
        const helper = this.createHelp();
        if (helper.helpWidth === void 0) {
          helper.helpWidth = contextOptions && contextOptions.error ? this._outputConfiguration.getErrHelpWidth() : this._outputConfiguration.getOutHelpWidth();
        }
        return helper.formatHelp(this, helper);
      }
      /**
       * @private
       */
      _getHelpContext(contextOptions) {
        contextOptions = contextOptions || {};
        const context = { error: !!contextOptions.error };
        let write;
        if (context.error) {
          write = (arg) => this._outputConfiguration.writeErr(arg);
        } else {
          write = (arg) => this._outputConfiguration.writeOut(arg);
        }
        context.write = contextOptions.write || write;
        context.command = this;
        return context;
      }
      /**
       * Output help information for this command.
       *
       * Outputs built-in help, and custom text added using `.addHelpText()`.
       *
       * @param {{ error: boolean } | Function} [contextOptions] - pass {error:true} to write to stderr instead of stdout
       */
      outputHelp(contextOptions) {
        let deprecatedCallback;
        if (typeof contextOptions === "function") {
          deprecatedCallback = contextOptions;
          contextOptions = void 0;
        }
        const context = this._getHelpContext(contextOptions);
        this._getCommandAndAncestors().reverse().forEach((command) => command.emit("beforeAllHelp", context));
        this.emit("beforeHelp", context);
        let helpInformation = this.helpInformation(context);
        if (deprecatedCallback) {
          helpInformation = deprecatedCallback(helpInformation);
          if (typeof helpInformation !== "string" && !Buffer.isBuffer(helpInformation)) {
            throw new Error("outputHelp callback must return a string or a Buffer");
          }
        }
        context.write(helpInformation);
        if (this._getHelpOption()?.long) {
          this.emit(this._getHelpOption().long);
        }
        this.emit("afterHelp", context);
        this._getCommandAndAncestors().forEach(
          (command) => command.emit("afterAllHelp", context)
        );
      }
      /**
       * You can pass in flags and a description to customise the built-in help option.
       * Pass in false to disable the built-in help option.
       *
       * @example
       * program.helpOption('-?, --help' 'show help'); // customise
       * program.helpOption(false); // disable
       *
       * @param {(string | boolean)} flags
       * @param {string} [description]
       * @return {Command} `this` command for chaining
       */
      helpOption(flags, description) {
        if (typeof flags === "boolean") {
          if (flags) {
            this._helpOption = this._helpOption ?? void 0;
          } else {
            this._helpOption = null;
          }
          return this;
        }
        flags = flags ?? "-h, --help";
        description = description ?? "display help for command";
        this._helpOption = this.createOption(flags, description);
        return this;
      }
      /**
       * Lazy create help option.
       * Returns null if has been disabled with .helpOption(false).
       *
       * @returns {(Option | null)} the help option
       * @package
       */
      _getHelpOption() {
        if (this._helpOption === void 0) {
          this.helpOption(void 0, void 0);
        }
        return this._helpOption;
      }
      /**
       * Supply your own option to use for the built-in help option.
       * This is an alternative to using helpOption() to customise the flags and description etc.
       *
       * @param {Option} option
       * @return {Command} `this` command for chaining
       */
      addHelpOption(option) {
        this._helpOption = option;
        return this;
      }
      /**
       * Output help information and exit.
       *
       * Outputs built-in help, and custom text added using `.addHelpText()`.
       *
       * @param {{ error: boolean }} [contextOptions] - pass {error:true} to write to stderr instead of stdout
       */
      help(contextOptions) {
        this.outputHelp(contextOptions);
        let exitCode = process2.exitCode || 0;
        if (exitCode === 0 && contextOptions && typeof contextOptions !== "function" && contextOptions.error) {
          exitCode = 1;
        }
        this._exit(exitCode, "commander.help", "(outputHelp)");
      }
      /**
       * Add additional text to be displayed with the built-in help.
       *
       * Position is 'before' or 'after' to affect just this command,
       * and 'beforeAll' or 'afterAll' to affect this command and all its subcommands.
       *
       * @param {string} position - before or after built-in help
       * @param {(string | Function)} text - string to add, or a function returning a string
       * @return {Command} `this` command for chaining
       */
      addHelpText(position, text) {
        const allowedValues = ["beforeAll", "before", "after", "afterAll"];
        if (!allowedValues.includes(position)) {
          throw new Error(`Unexpected value for position to addHelpText.
Expecting one of '${allowedValues.join("', '")}'`);
        }
        const helpEvent = `${position}Help`;
        this.on(helpEvent, (context) => {
          let helpStr;
          if (typeof text === "function") {
            helpStr = text({ error: context.error, command: context.command });
          } else {
            helpStr = text;
          }
          if (helpStr) {
            context.write(`${helpStr}
`);
          }
        });
        return this;
      }
      /**
       * Output help information if help flags specified
       *
       * @param {Array} args - array of options to search for help flags
       * @private
       */
      _outputHelpIfRequested(args) {
        const helpOption = this._getHelpOption();
        const helpRequested = helpOption && args.find((arg) => helpOption.is(arg));
        if (helpRequested) {
          this.outputHelp();
          this._exit(0, "commander.helpDisplayed", "(outputHelp)");
        }
      }
    };
    function incrementNodeInspectorPort(args) {
      return args.map((arg) => {
        if (!arg.startsWith("--inspect")) {
          return arg;
        }
        let debugOption;
        let debugHost = "127.0.0.1";
        let debugPort = "9229";
        let match;
        if ((match = arg.match(/^(--inspect(-brk)?)$/)) !== null) {
          debugOption = match[1];
        } else if ((match = arg.match(/^(--inspect(-brk|-port)?)=([^:]+)$/)) !== null) {
          debugOption = match[1];
          if (/^\d+$/.test(match[3])) {
            debugPort = match[3];
          } else {
            debugHost = match[3];
          }
        } else if ((match = arg.match(/^(--inspect(-brk|-port)?)=([^:]+):(\d+)$/)) !== null) {
          debugOption = match[1];
          debugHost = match[3];
          debugPort = match[4];
        }
        if (debugOption && debugPort !== "0") {
          return `${debugOption}=${debugHost}:${parseInt(debugPort) + 1}`;
        }
        return arg;
      });
    }
    exports.Command = Command2;
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/commander/index.js
var require_commander = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/commander/index.js"(exports) {
    var { Argument: Argument2 } = require_argument();
    var { Command: Command2 } = require_command();
    var { CommanderError: CommanderError2, InvalidArgumentError: InvalidArgumentError2 } = require_error();
    var { Help: Help2 } = require_help();
    var { Option: Option2 } = require_option();
    exports.program = new Command2();
    exports.createCommand = (name) => new Command2(name);
    exports.createOption = (flags, description) => new Option2(flags, description);
    exports.createArgument = (name, description) => new Argument2(name, description);
    exports.Command = Command2;
    exports.Option = Option2;
    exports.Argument = Argument2;
    exports.Help = Help2;
    exports.CommanderError = CommanderError2;
    exports.InvalidArgumentError = InvalidArgumentError2;
    exports.InvalidOptionArgumentError = InvalidArgumentError2;
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/can-promise.js
var require_can_promise = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/can-promise.js"(exports, module) {
    module.exports = function() {
      return typeof Promise === "function" && Promise.prototype && Promise.prototype.then;
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/utils.js
var require_utils = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/utils.js"(exports) {
    var toSJISFunction;
    var CODEWORDS_COUNT = [
      0,
      // Not used
      26,
      44,
      70,
      100,
      134,
      172,
      196,
      242,
      292,
      346,
      404,
      466,
      532,
      581,
      655,
      733,
      815,
      901,
      991,
      1085,
      1156,
      1258,
      1364,
      1474,
      1588,
      1706,
      1828,
      1921,
      2051,
      2185,
      2323,
      2465,
      2611,
      2761,
      2876,
      3034,
      3196,
      3362,
      3532,
      3706
    ];
    exports.getSymbolSize = function getSymbolSize(version) {
      if (!version) throw new Error('"version" cannot be null or undefined');
      if (version < 1 || version > 40) throw new Error('"version" should be in range from 1 to 40');
      return version * 4 + 17;
    };
    exports.getSymbolTotalCodewords = function getSymbolTotalCodewords(version) {
      return CODEWORDS_COUNT[version];
    };
    exports.getBCHDigit = function(data) {
      let digit = 0;
      while (data !== 0) {
        digit++;
        data >>>= 1;
      }
      return digit;
    };
    exports.setToSJISFunction = function setToSJISFunction(f) {
      if (typeof f !== "function") {
        throw new Error('"toSJISFunc" is not a valid function.');
      }
      toSJISFunction = f;
    };
    exports.isKanjiModeEnabled = function() {
      return typeof toSJISFunction !== "undefined";
    };
    exports.toSJIS = function toSJIS(kanji) {
      return toSJISFunction(kanji);
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/error-correction-level.js
var require_error_correction_level = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/error-correction-level.js"(exports) {
    exports.L = { bit: 1 };
    exports.M = { bit: 0 };
    exports.Q = { bit: 3 };
    exports.H = { bit: 2 };
    function fromString(string) {
      if (typeof string !== "string") {
        throw new Error("Param is not a string");
      }
      const lcStr = string.toLowerCase();
      switch (lcStr) {
        case "l":
        case "low":
          return exports.L;
        case "m":
        case "medium":
          return exports.M;
        case "q":
        case "quartile":
          return exports.Q;
        case "h":
        case "high":
          return exports.H;
        default:
          throw new Error("Unknown EC Level: " + string);
      }
    }
    exports.isValid = function isValid(level) {
      return level && typeof level.bit !== "undefined" && level.bit >= 0 && level.bit < 4;
    };
    exports.from = function from(value, defaultValue) {
      if (exports.isValid(value)) {
        return value;
      }
      try {
        return fromString(value);
      } catch (e) {
        return defaultValue;
      }
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/bit-buffer.js
var require_bit_buffer = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/bit-buffer.js"(exports, module) {
    function BitBuffer() {
      this.buffer = [];
      this.length = 0;
    }
    BitBuffer.prototype = {
      get: function(index) {
        const bufIndex = Math.floor(index / 8);
        return (this.buffer[bufIndex] >>> 7 - index % 8 & 1) === 1;
      },
      put: function(num, length) {
        for (let i = 0; i < length; i++) {
          this.putBit((num >>> length - i - 1 & 1) === 1);
        }
      },
      getLengthInBits: function() {
        return this.length;
      },
      putBit: function(bit) {
        const bufIndex = Math.floor(this.length / 8);
        if (this.buffer.length <= bufIndex) {
          this.buffer.push(0);
        }
        if (bit) {
          this.buffer[bufIndex] |= 128 >>> this.length % 8;
        }
        this.length++;
      }
    };
    module.exports = BitBuffer;
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/bit-matrix.js
var require_bit_matrix = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/bit-matrix.js"(exports, module) {
    function BitMatrix(size) {
      if (!size || size < 1) {
        throw new Error("BitMatrix size must be defined and greater than 0");
      }
      this.size = size;
      this.data = new Uint8Array(size * size);
      this.reservedBit = new Uint8Array(size * size);
    }
    BitMatrix.prototype.set = function(row, col, value, reserved) {
      const index = row * this.size + col;
      this.data[index] = value;
      if (reserved) this.reservedBit[index] = true;
    };
    BitMatrix.prototype.get = function(row, col) {
      return this.data[row * this.size + col];
    };
    BitMatrix.prototype.xor = function(row, col, value) {
      this.data[row * this.size + col] ^= value;
    };
    BitMatrix.prototype.isReserved = function(row, col) {
      return this.reservedBit[row * this.size + col];
    };
    module.exports = BitMatrix;
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/alignment-pattern.js
var require_alignment_pattern = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/alignment-pattern.js"(exports) {
    var getSymbolSize = require_utils().getSymbolSize;
    exports.getRowColCoords = function getRowColCoords(version) {
      if (version === 1) return [];
      const posCount = Math.floor(version / 7) + 2;
      const size = getSymbolSize(version);
      const intervals = size === 145 ? 26 : Math.ceil((size - 13) / (2 * posCount - 2)) * 2;
      const positions = [size - 7];
      for (let i = 1; i < posCount - 1; i++) {
        positions[i] = positions[i - 1] - intervals;
      }
      positions.push(6);
      return positions.reverse();
    };
    exports.getPositions = function getPositions(version) {
      const coords = [];
      const pos = exports.getRowColCoords(version);
      const posLength = pos.length;
      for (let i = 0; i < posLength; i++) {
        for (let j = 0; j < posLength; j++) {
          if (i === 0 && j === 0 || // top-left
          i === 0 && j === posLength - 1 || // bottom-left
          i === posLength - 1 && j === 0) {
            continue;
          }
          coords.push([pos[i], pos[j]]);
        }
      }
      return coords;
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/finder-pattern.js
var require_finder_pattern = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/finder-pattern.js"(exports) {
    var getSymbolSize = require_utils().getSymbolSize;
    var FINDER_PATTERN_SIZE = 7;
    exports.getPositions = function getPositions(version) {
      const size = getSymbolSize(version);
      return [
        // top-left
        [0, 0],
        // top-right
        [size - FINDER_PATTERN_SIZE, 0],
        // bottom-left
        [0, size - FINDER_PATTERN_SIZE]
      ];
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/mask-pattern.js
var require_mask_pattern = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/mask-pattern.js"(exports) {
    exports.Patterns = {
      PATTERN000: 0,
      PATTERN001: 1,
      PATTERN010: 2,
      PATTERN011: 3,
      PATTERN100: 4,
      PATTERN101: 5,
      PATTERN110: 6,
      PATTERN111: 7
    };
    var PenaltyScores = {
      N1: 3,
      N2: 3,
      N3: 40,
      N4: 10
    };
    exports.isValid = function isValid(mask) {
      return mask != null && mask !== "" && !isNaN(mask) && mask >= 0 && mask <= 7;
    };
    exports.from = function from(value) {
      return exports.isValid(value) ? parseInt(value, 10) : void 0;
    };
    exports.getPenaltyN1 = function getPenaltyN1(data) {
      const size = data.size;
      let points = 0;
      let sameCountCol = 0;
      let sameCountRow = 0;
      let lastCol = null;
      let lastRow = null;
      for (let row = 0; row < size; row++) {
        sameCountCol = sameCountRow = 0;
        lastCol = lastRow = null;
        for (let col = 0; col < size; col++) {
          let module2 = data.get(row, col);
          if (module2 === lastCol) {
            sameCountCol++;
          } else {
            if (sameCountCol >= 5) points += PenaltyScores.N1 + (sameCountCol - 5);
            lastCol = module2;
            sameCountCol = 1;
          }
          module2 = data.get(col, row);
          if (module2 === lastRow) {
            sameCountRow++;
          } else {
            if (sameCountRow >= 5) points += PenaltyScores.N1 + (sameCountRow - 5);
            lastRow = module2;
            sameCountRow = 1;
          }
        }
        if (sameCountCol >= 5) points += PenaltyScores.N1 + (sameCountCol - 5);
        if (sameCountRow >= 5) points += PenaltyScores.N1 + (sameCountRow - 5);
      }
      return points;
    };
    exports.getPenaltyN2 = function getPenaltyN2(data) {
      const size = data.size;
      let points = 0;
      for (let row = 0; row < size - 1; row++) {
        for (let col = 0; col < size - 1; col++) {
          const last = data.get(row, col) + data.get(row, col + 1) + data.get(row + 1, col) + data.get(row + 1, col + 1);
          if (last === 4 || last === 0) points++;
        }
      }
      return points * PenaltyScores.N2;
    };
    exports.getPenaltyN3 = function getPenaltyN3(data) {
      const size = data.size;
      let points = 0;
      let bitsCol = 0;
      let bitsRow = 0;
      for (let row = 0; row < size; row++) {
        bitsCol = bitsRow = 0;
        for (let col = 0; col < size; col++) {
          bitsCol = bitsCol << 1 & 2047 | data.get(row, col);
          if (col >= 10 && (bitsCol === 1488 || bitsCol === 93)) points++;
          bitsRow = bitsRow << 1 & 2047 | data.get(col, row);
          if (col >= 10 && (bitsRow === 1488 || bitsRow === 93)) points++;
        }
      }
      return points * PenaltyScores.N3;
    };
    exports.getPenaltyN4 = function getPenaltyN4(data) {
      let darkCount = 0;
      const modulesCount = data.data.length;
      for (let i = 0; i < modulesCount; i++) darkCount += data.data[i];
      const k = Math.abs(Math.ceil(darkCount * 100 / modulesCount / 5) - 10);
      return k * PenaltyScores.N4;
    };
    function getMaskAt(maskPattern, i, j) {
      switch (maskPattern) {
        case exports.Patterns.PATTERN000:
          return (i + j) % 2 === 0;
        case exports.Patterns.PATTERN001:
          return i % 2 === 0;
        case exports.Patterns.PATTERN010:
          return j % 3 === 0;
        case exports.Patterns.PATTERN011:
          return (i + j) % 3 === 0;
        case exports.Patterns.PATTERN100:
          return (Math.floor(i / 2) + Math.floor(j / 3)) % 2 === 0;
        case exports.Patterns.PATTERN101:
          return i * j % 2 + i * j % 3 === 0;
        case exports.Patterns.PATTERN110:
          return (i * j % 2 + i * j % 3) % 2 === 0;
        case exports.Patterns.PATTERN111:
          return (i * j % 3 + (i + j) % 2) % 2 === 0;
        default:
          throw new Error("bad maskPattern:" + maskPattern);
      }
    }
    exports.applyMask = function applyMask(pattern, data) {
      const size = data.size;
      for (let col = 0; col < size; col++) {
        for (let row = 0; row < size; row++) {
          if (data.isReserved(row, col)) continue;
          data.xor(row, col, getMaskAt(pattern, row, col));
        }
      }
    };
    exports.getBestMask = function getBestMask(data, setupFormatFunc) {
      const numPatterns = Object.keys(exports.Patterns).length;
      let bestPattern = 0;
      let lowerPenalty = Infinity;
      for (let p = 0; p < numPatterns; p++) {
        setupFormatFunc(p);
        exports.applyMask(p, data);
        const penalty = exports.getPenaltyN1(data) + exports.getPenaltyN2(data) + exports.getPenaltyN3(data) + exports.getPenaltyN4(data);
        exports.applyMask(p, data);
        if (penalty < lowerPenalty) {
          lowerPenalty = penalty;
          bestPattern = p;
        }
      }
      return bestPattern;
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/error-correction-code.js
var require_error_correction_code = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/error-correction-code.js"(exports) {
    var ECLevel = require_error_correction_level();
    var EC_BLOCKS_TABLE = [
      // L  M  Q  H
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      2,
      2,
      1,
      2,
      2,
      4,
      1,
      2,
      4,
      4,
      2,
      4,
      4,
      4,
      2,
      4,
      6,
      5,
      2,
      4,
      6,
      6,
      2,
      5,
      8,
      8,
      4,
      5,
      8,
      8,
      4,
      5,
      8,
      11,
      4,
      8,
      10,
      11,
      4,
      9,
      12,
      16,
      4,
      9,
      16,
      16,
      6,
      10,
      12,
      18,
      6,
      10,
      17,
      16,
      6,
      11,
      16,
      19,
      6,
      13,
      18,
      21,
      7,
      14,
      21,
      25,
      8,
      16,
      20,
      25,
      8,
      17,
      23,
      25,
      9,
      17,
      23,
      34,
      9,
      18,
      25,
      30,
      10,
      20,
      27,
      32,
      12,
      21,
      29,
      35,
      12,
      23,
      34,
      37,
      12,
      25,
      34,
      40,
      13,
      26,
      35,
      42,
      14,
      28,
      38,
      45,
      15,
      29,
      40,
      48,
      16,
      31,
      43,
      51,
      17,
      33,
      45,
      54,
      18,
      35,
      48,
      57,
      19,
      37,
      51,
      60,
      19,
      38,
      53,
      63,
      20,
      40,
      56,
      66,
      21,
      43,
      59,
      70,
      22,
      45,
      62,
      74,
      24,
      47,
      65,
      77,
      25,
      49,
      68,
      81
    ];
    var EC_CODEWORDS_TABLE = [
      // L  M  Q  H
      7,
      10,
      13,
      17,
      10,
      16,
      22,
      28,
      15,
      26,
      36,
      44,
      20,
      36,
      52,
      64,
      26,
      48,
      72,
      88,
      36,
      64,
      96,
      112,
      40,
      72,
      108,
      130,
      48,
      88,
      132,
      156,
      60,
      110,
      160,
      192,
      72,
      130,
      192,
      224,
      80,
      150,
      224,
      264,
      96,
      176,
      260,
      308,
      104,
      198,
      288,
      352,
      120,
      216,
      320,
      384,
      132,
      240,
      360,
      432,
      144,
      280,
      408,
      480,
      168,
      308,
      448,
      532,
      180,
      338,
      504,
      588,
      196,
      364,
      546,
      650,
      224,
      416,
      600,
      700,
      224,
      442,
      644,
      750,
      252,
      476,
      690,
      816,
      270,
      504,
      750,
      900,
      300,
      560,
      810,
      960,
      312,
      588,
      870,
      1050,
      336,
      644,
      952,
      1110,
      360,
      700,
      1020,
      1200,
      390,
      728,
      1050,
      1260,
      420,
      784,
      1140,
      1350,
      450,
      812,
      1200,
      1440,
      480,
      868,
      1290,
      1530,
      510,
      924,
      1350,
      1620,
      540,
      980,
      1440,
      1710,
      570,
      1036,
      1530,
      1800,
      570,
      1064,
      1590,
      1890,
      600,
      1120,
      1680,
      1980,
      630,
      1204,
      1770,
      2100,
      660,
      1260,
      1860,
      2220,
      720,
      1316,
      1950,
      2310,
      750,
      1372,
      2040,
      2430
    ];
    exports.getBlocksCount = function getBlocksCount(version, errorCorrectionLevel) {
      switch (errorCorrectionLevel) {
        case ECLevel.L:
          return EC_BLOCKS_TABLE[(version - 1) * 4 + 0];
        case ECLevel.M:
          return EC_BLOCKS_TABLE[(version - 1) * 4 + 1];
        case ECLevel.Q:
          return EC_BLOCKS_TABLE[(version - 1) * 4 + 2];
        case ECLevel.H:
          return EC_BLOCKS_TABLE[(version - 1) * 4 + 3];
        default:
          return void 0;
      }
    };
    exports.getTotalCodewordsCount = function getTotalCodewordsCount(version, errorCorrectionLevel) {
      switch (errorCorrectionLevel) {
        case ECLevel.L:
          return EC_CODEWORDS_TABLE[(version - 1) * 4 + 0];
        case ECLevel.M:
          return EC_CODEWORDS_TABLE[(version - 1) * 4 + 1];
        case ECLevel.Q:
          return EC_CODEWORDS_TABLE[(version - 1) * 4 + 2];
        case ECLevel.H:
          return EC_CODEWORDS_TABLE[(version - 1) * 4 + 3];
        default:
          return void 0;
      }
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/galois-field.js
var require_galois_field = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/galois-field.js"(exports) {
    var EXP_TABLE = new Uint8Array(512);
    var LOG_TABLE = new Uint8Array(256);
    (function initTables() {
      let x = 1;
      for (let i = 0; i < 255; i++) {
        EXP_TABLE[i] = x;
        LOG_TABLE[x] = i;
        x <<= 1;
        if (x & 256) {
          x ^= 285;
        }
      }
      for (let i = 255; i < 512; i++) {
        EXP_TABLE[i] = EXP_TABLE[i - 255];
      }
    })();
    exports.log = function log(n) {
      if (n < 1) throw new Error("log(" + n + ")");
      return LOG_TABLE[n];
    };
    exports.exp = function exp(n) {
      return EXP_TABLE[n];
    };
    exports.mul = function mul(x, y) {
      if (x === 0 || y === 0) return 0;
      return EXP_TABLE[LOG_TABLE[x] + LOG_TABLE[y]];
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/polynomial.js
var require_polynomial = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/polynomial.js"(exports) {
    var GF = require_galois_field();
    exports.mul = function mul(p1, p2) {
      const coeff = new Uint8Array(p1.length + p2.length - 1);
      for (let i = 0; i < p1.length; i++) {
        for (let j = 0; j < p2.length; j++) {
          coeff[i + j] ^= GF.mul(p1[i], p2[j]);
        }
      }
      return coeff;
    };
    exports.mod = function mod(divident, divisor) {
      let result = new Uint8Array(divident);
      while (result.length - divisor.length >= 0) {
        const coeff = result[0];
        for (let i = 0; i < divisor.length; i++) {
          result[i] ^= GF.mul(divisor[i], coeff);
        }
        let offset = 0;
        while (offset < result.length && result[offset] === 0) offset++;
        result = result.slice(offset);
      }
      return result;
    };
    exports.generateECPolynomial = function generateECPolynomial(degree) {
      let poly = new Uint8Array([1]);
      for (let i = 0; i < degree; i++) {
        poly = exports.mul(poly, new Uint8Array([1, GF.exp(i)]));
      }
      return poly;
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/reed-solomon-encoder.js
var require_reed_solomon_encoder = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/reed-solomon-encoder.js"(exports, module) {
    var Polynomial = require_polynomial();
    function ReedSolomonEncoder(degree) {
      this.genPoly = void 0;
      this.degree = degree;
      if (this.degree) this.initialize(this.degree);
    }
    ReedSolomonEncoder.prototype.initialize = function initialize(degree) {
      this.degree = degree;
      this.genPoly = Polynomial.generateECPolynomial(this.degree);
    };
    ReedSolomonEncoder.prototype.encode = function encode(data) {
      if (!this.genPoly) {
        throw new Error("Encoder not initialized");
      }
      const paddedData = new Uint8Array(data.length + this.degree);
      paddedData.set(data);
      const remainder = Polynomial.mod(paddedData, this.genPoly);
      const start = this.degree - remainder.length;
      if (start > 0) {
        const buff = new Uint8Array(this.degree);
        buff.set(remainder, start);
        return buff;
      }
      return remainder;
    };
    module.exports = ReedSolomonEncoder;
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/version-check.js
var require_version_check = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/version-check.js"(exports) {
    exports.isValid = function isValid(version) {
      return !isNaN(version) && version >= 1 && version <= 40;
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/regex.js
var require_regex = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/regex.js"(exports) {
    var numeric = "[0-9]+";
    var alphanumeric = "[A-Z $%*+\\-./:]+";
    var kanji = "(?:[u3000-u303F]|[u3040-u309F]|[u30A0-u30FF]|[uFF00-uFFEF]|[u4E00-u9FAF]|[u2605-u2606]|[u2190-u2195]|u203B|[u2010u2015u2018u2019u2025u2026u201Cu201Du2225u2260]|[u0391-u0451]|[u00A7u00A8u00B1u00B4u00D7u00F7])+";
    kanji = kanji.replace(/u/g, "\\u");
    var byte = "(?:(?![A-Z0-9 $%*+\\-./:]|" + kanji + ")(?:.|[\r\n]))+";
    exports.KANJI = new RegExp(kanji, "g");
    exports.BYTE_KANJI = new RegExp("[^A-Z0-9 $%*+\\-./:]+", "g");
    exports.BYTE = new RegExp(byte, "g");
    exports.NUMERIC = new RegExp(numeric, "g");
    exports.ALPHANUMERIC = new RegExp(alphanumeric, "g");
    var TEST_KANJI = new RegExp("^" + kanji + "$");
    var TEST_NUMERIC = new RegExp("^" + numeric + "$");
    var TEST_ALPHANUMERIC = new RegExp("^[A-Z0-9 $%*+\\-./:]+$");
    exports.testKanji = function testKanji(str) {
      return TEST_KANJI.test(str);
    };
    exports.testNumeric = function testNumeric(str) {
      return TEST_NUMERIC.test(str);
    };
    exports.testAlphanumeric = function testAlphanumeric(str) {
      return TEST_ALPHANUMERIC.test(str);
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/mode.js
var require_mode = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/mode.js"(exports) {
    var VersionCheck = require_version_check();
    var Regex = require_regex();
    exports.NUMERIC = {
      id: "Numeric",
      bit: 1 << 0,
      ccBits: [10, 12, 14]
    };
    exports.ALPHANUMERIC = {
      id: "Alphanumeric",
      bit: 1 << 1,
      ccBits: [9, 11, 13]
    };
    exports.BYTE = {
      id: "Byte",
      bit: 1 << 2,
      ccBits: [8, 16, 16]
    };
    exports.KANJI = {
      id: "Kanji",
      bit: 1 << 3,
      ccBits: [8, 10, 12]
    };
    exports.MIXED = {
      bit: -1
    };
    exports.getCharCountIndicator = function getCharCountIndicator(mode, version) {
      if (!mode.ccBits) throw new Error("Invalid mode: " + mode);
      if (!VersionCheck.isValid(version)) {
        throw new Error("Invalid version: " + version);
      }
      if (version >= 1 && version < 10) return mode.ccBits[0];
      else if (version < 27) return mode.ccBits[1];
      return mode.ccBits[2];
    };
    exports.getBestModeForData = function getBestModeForData(dataStr) {
      if (Regex.testNumeric(dataStr)) return exports.NUMERIC;
      else if (Regex.testAlphanumeric(dataStr)) return exports.ALPHANUMERIC;
      else if (Regex.testKanji(dataStr)) return exports.KANJI;
      else return exports.BYTE;
    };
    exports.toString = function toString(mode) {
      if (mode && mode.id) return mode.id;
      throw new Error("Invalid mode");
    };
    exports.isValid = function isValid(mode) {
      return mode && mode.bit && mode.ccBits;
    };
    function fromString(string) {
      if (typeof string !== "string") {
        throw new Error("Param is not a string");
      }
      const lcStr = string.toLowerCase();
      switch (lcStr) {
        case "numeric":
          return exports.NUMERIC;
        case "alphanumeric":
          return exports.ALPHANUMERIC;
        case "kanji":
          return exports.KANJI;
        case "byte":
          return exports.BYTE;
        default:
          throw new Error("Unknown mode: " + string);
      }
    }
    exports.from = function from(value, defaultValue) {
      if (exports.isValid(value)) {
        return value;
      }
      try {
        return fromString(value);
      } catch (e) {
        return defaultValue;
      }
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/version.js
var require_version = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/version.js"(exports) {
    var Utils = require_utils();
    var ECCode = require_error_correction_code();
    var ECLevel = require_error_correction_level();
    var Mode = require_mode();
    var VersionCheck = require_version_check();
    var G18 = 1 << 12 | 1 << 11 | 1 << 10 | 1 << 9 | 1 << 8 | 1 << 5 | 1 << 2 | 1 << 0;
    var G18_BCH = Utils.getBCHDigit(G18);
    function getBestVersionForDataLength(mode, length, errorCorrectionLevel) {
      for (let currentVersion = 1; currentVersion <= 40; currentVersion++) {
        if (length <= exports.getCapacity(currentVersion, errorCorrectionLevel, mode)) {
          return currentVersion;
        }
      }
      return void 0;
    }
    function getReservedBitsCount(mode, version) {
      return Mode.getCharCountIndicator(mode, version) + 4;
    }
    function getTotalBitsFromDataArray(segments, version) {
      let totalBits = 0;
      segments.forEach(function(data) {
        const reservedBits = getReservedBitsCount(data.mode, version);
        totalBits += reservedBits + data.getBitsLength();
      });
      return totalBits;
    }
    function getBestVersionForMixedData(segments, errorCorrectionLevel) {
      for (let currentVersion = 1; currentVersion <= 40; currentVersion++) {
        const length = getTotalBitsFromDataArray(segments, currentVersion);
        if (length <= exports.getCapacity(currentVersion, errorCorrectionLevel, Mode.MIXED)) {
          return currentVersion;
        }
      }
      return void 0;
    }
    exports.from = function from(value, defaultValue) {
      if (VersionCheck.isValid(value)) {
        return parseInt(value, 10);
      }
      return defaultValue;
    };
    exports.getCapacity = function getCapacity(version, errorCorrectionLevel, mode) {
      if (!VersionCheck.isValid(version)) {
        throw new Error("Invalid QR Code version");
      }
      if (typeof mode === "undefined") mode = Mode.BYTE;
      const totalCodewords = Utils.getSymbolTotalCodewords(version);
      const ecTotalCodewords = ECCode.getTotalCodewordsCount(version, errorCorrectionLevel);
      const dataTotalCodewordsBits = (totalCodewords - ecTotalCodewords) * 8;
      if (mode === Mode.MIXED) return dataTotalCodewordsBits;
      const usableBits = dataTotalCodewordsBits - getReservedBitsCount(mode, version);
      switch (mode) {
        case Mode.NUMERIC:
          return Math.floor(usableBits / 10 * 3);
        case Mode.ALPHANUMERIC:
          return Math.floor(usableBits / 11 * 2);
        case Mode.KANJI:
          return Math.floor(usableBits / 13);
        case Mode.BYTE:
        default:
          return Math.floor(usableBits / 8);
      }
    };
    exports.getBestVersionForData = function getBestVersionForData(data, errorCorrectionLevel) {
      let seg;
      const ecl = ECLevel.from(errorCorrectionLevel, ECLevel.M);
      if (Array.isArray(data)) {
        if (data.length > 1) {
          return getBestVersionForMixedData(data, ecl);
        }
        if (data.length === 0) {
          return 1;
        }
        seg = data[0];
      } else {
        seg = data;
      }
      return getBestVersionForDataLength(seg.mode, seg.getLength(), ecl);
    };
    exports.getEncodedBits = function getEncodedBits(version) {
      if (!VersionCheck.isValid(version) || version < 7) {
        throw new Error("Invalid QR Code version");
      }
      let d = version << 12;
      while (Utils.getBCHDigit(d) - G18_BCH >= 0) {
        d ^= G18 << Utils.getBCHDigit(d) - G18_BCH;
      }
      return version << 12 | d;
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/format-info.js
var require_format_info = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/format-info.js"(exports) {
    var Utils = require_utils();
    var G15 = 1 << 10 | 1 << 8 | 1 << 5 | 1 << 4 | 1 << 2 | 1 << 1 | 1 << 0;
    var G15_MASK = 1 << 14 | 1 << 12 | 1 << 10 | 1 << 4 | 1 << 1;
    var G15_BCH = Utils.getBCHDigit(G15);
    exports.getEncodedBits = function getEncodedBits(errorCorrectionLevel, mask) {
      const data = errorCorrectionLevel.bit << 3 | mask;
      let d = data << 10;
      while (Utils.getBCHDigit(d) - G15_BCH >= 0) {
        d ^= G15 << Utils.getBCHDigit(d) - G15_BCH;
      }
      return (data << 10 | d) ^ G15_MASK;
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/numeric-data.js
var require_numeric_data = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/numeric-data.js"(exports, module) {
    var Mode = require_mode();
    function NumericData(data) {
      this.mode = Mode.NUMERIC;
      this.data = data.toString();
    }
    NumericData.getBitsLength = function getBitsLength(length) {
      return 10 * Math.floor(length / 3) + (length % 3 ? length % 3 * 3 + 1 : 0);
    };
    NumericData.prototype.getLength = function getLength() {
      return this.data.length;
    };
    NumericData.prototype.getBitsLength = function getBitsLength() {
      return NumericData.getBitsLength(this.data.length);
    };
    NumericData.prototype.write = function write(bitBuffer) {
      let i, group, value;
      for (i = 0; i + 3 <= this.data.length; i += 3) {
        group = this.data.substr(i, 3);
        value = parseInt(group, 10);
        bitBuffer.put(value, 10);
      }
      const remainingNum = this.data.length - i;
      if (remainingNum > 0) {
        group = this.data.substr(i);
        value = parseInt(group, 10);
        bitBuffer.put(value, remainingNum * 3 + 1);
      }
    };
    module.exports = NumericData;
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/alphanumeric-data.js
var require_alphanumeric_data = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/alphanumeric-data.js"(exports, module) {
    var Mode = require_mode();
    var ALPHA_NUM_CHARS = [
      "0",
      "1",
      "2",
      "3",
      "4",
      "5",
      "6",
      "7",
      "8",
      "9",
      "A",
      "B",
      "C",
      "D",
      "E",
      "F",
      "G",
      "H",
      "I",
      "J",
      "K",
      "L",
      "M",
      "N",
      "O",
      "P",
      "Q",
      "R",
      "S",
      "T",
      "U",
      "V",
      "W",
      "X",
      "Y",
      "Z",
      " ",
      "$",
      "%",
      "*",
      "+",
      "-",
      ".",
      "/",
      ":"
    ];
    function AlphanumericData(data) {
      this.mode = Mode.ALPHANUMERIC;
      this.data = data;
    }
    AlphanumericData.getBitsLength = function getBitsLength(length) {
      return 11 * Math.floor(length / 2) + 6 * (length % 2);
    };
    AlphanumericData.prototype.getLength = function getLength() {
      return this.data.length;
    };
    AlphanumericData.prototype.getBitsLength = function getBitsLength() {
      return AlphanumericData.getBitsLength(this.data.length);
    };
    AlphanumericData.prototype.write = function write(bitBuffer) {
      let i;
      for (i = 0; i + 2 <= this.data.length; i += 2) {
        let value = ALPHA_NUM_CHARS.indexOf(this.data[i]) * 45;
        value += ALPHA_NUM_CHARS.indexOf(this.data[i + 1]);
        bitBuffer.put(value, 11);
      }
      if (this.data.length % 2) {
        bitBuffer.put(ALPHA_NUM_CHARS.indexOf(this.data[i]), 6);
      }
    };
    module.exports = AlphanumericData;
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/byte-data.js
var require_byte_data = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/byte-data.js"(exports, module) {
    var Mode = require_mode();
    function ByteData(data) {
      this.mode = Mode.BYTE;
      if (typeof data === "string") {
        this.data = new TextEncoder().encode(data);
      } else {
        this.data = new Uint8Array(data);
      }
    }
    ByteData.getBitsLength = function getBitsLength(length) {
      return length * 8;
    };
    ByteData.prototype.getLength = function getLength() {
      return this.data.length;
    };
    ByteData.prototype.getBitsLength = function getBitsLength() {
      return ByteData.getBitsLength(this.data.length);
    };
    ByteData.prototype.write = function(bitBuffer) {
      for (let i = 0, l = this.data.length; i < l; i++) {
        bitBuffer.put(this.data[i], 8);
      }
    };
    module.exports = ByteData;
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/kanji-data.js
var require_kanji_data = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/kanji-data.js"(exports, module) {
    var Mode = require_mode();
    var Utils = require_utils();
    function KanjiData(data) {
      this.mode = Mode.KANJI;
      this.data = data;
    }
    KanjiData.getBitsLength = function getBitsLength(length) {
      return length * 13;
    };
    KanjiData.prototype.getLength = function getLength() {
      return this.data.length;
    };
    KanjiData.prototype.getBitsLength = function getBitsLength() {
      return KanjiData.getBitsLength(this.data.length);
    };
    KanjiData.prototype.write = function(bitBuffer) {
      let i;
      for (i = 0; i < this.data.length; i++) {
        let value = Utils.toSJIS(this.data[i]);
        if (value >= 33088 && value <= 40956) {
          value -= 33088;
        } else if (value >= 57408 && value <= 60351) {
          value -= 49472;
        } else {
          throw new Error(
            "Invalid SJIS character: " + this.data[i] + "\nMake sure your charset is UTF-8"
          );
        }
        value = (value >>> 8 & 255) * 192 + (value & 255);
        bitBuffer.put(value, 13);
      }
    };
    module.exports = KanjiData;
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/dijkstrajs/dijkstra.js
var require_dijkstra = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/dijkstrajs/dijkstra.js"(exports, module) {
    "use strict";
    var dijkstra = {
      single_source_shortest_paths: function(graph, s, d) {
        var predecessors = {};
        var costs = {};
        costs[s] = 0;
        var open = dijkstra.PriorityQueue.make();
        open.push(s, 0);
        var closest, u, v, cost_of_s_to_u, adjacent_nodes, cost_of_e, cost_of_s_to_u_plus_cost_of_e, cost_of_s_to_v, first_visit;
        while (!open.empty()) {
          closest = open.pop();
          u = closest.value;
          cost_of_s_to_u = closest.cost;
          adjacent_nodes = graph[u] || {};
          for (v in adjacent_nodes) {
            if (adjacent_nodes.hasOwnProperty(v)) {
              cost_of_e = adjacent_nodes[v];
              cost_of_s_to_u_plus_cost_of_e = cost_of_s_to_u + cost_of_e;
              cost_of_s_to_v = costs[v];
              first_visit = typeof costs[v] === "undefined";
              if (first_visit || cost_of_s_to_v > cost_of_s_to_u_plus_cost_of_e) {
                costs[v] = cost_of_s_to_u_plus_cost_of_e;
                open.push(v, cost_of_s_to_u_plus_cost_of_e);
                predecessors[v] = u;
              }
            }
          }
        }
        if (typeof d !== "undefined" && typeof costs[d] === "undefined") {
          var msg = ["Could not find a path from ", s, " to ", d, "."].join("");
          throw new Error(msg);
        }
        return predecessors;
      },
      extract_shortest_path_from_predecessor_list: function(predecessors, d) {
        var nodes = [];
        var u = d;
        var predecessor;
        while (u) {
          nodes.push(u);
          predecessor = predecessors[u];
          u = predecessors[u];
        }
        nodes.reverse();
        return nodes;
      },
      find_path: function(graph, s, d) {
        var predecessors = dijkstra.single_source_shortest_paths(graph, s, d);
        return dijkstra.extract_shortest_path_from_predecessor_list(
          predecessors,
          d
        );
      },
      /**
       * A very naive priority queue implementation.
       */
      PriorityQueue: {
        make: function(opts) {
          var T = dijkstra.PriorityQueue, t = {}, key;
          opts = opts || {};
          for (key in T) {
            if (T.hasOwnProperty(key)) {
              t[key] = T[key];
            }
          }
          t.queue = [];
          t.sorter = opts.sorter || T.default_sorter;
          return t;
        },
        default_sorter: function(a, b) {
          return a.cost - b.cost;
        },
        /**
         * Add a new item to the queue and ensure the highest priority element
         * is at the front of the queue.
         */
        push: function(value, cost) {
          var item = { value, cost };
          this.queue.push(item);
          this.queue.sort(this.sorter);
        },
        /**
         * Return the highest priority element in the queue.
         */
        pop: function() {
          return this.queue.shift();
        },
        empty: function() {
          return this.queue.length === 0;
        }
      }
    };
    if (typeof module !== "undefined") {
      module.exports = dijkstra;
    }
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/segments.js
var require_segments = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/segments.js"(exports) {
    var Mode = require_mode();
    var NumericData = require_numeric_data();
    var AlphanumericData = require_alphanumeric_data();
    var ByteData = require_byte_data();
    var KanjiData = require_kanji_data();
    var Regex = require_regex();
    var Utils = require_utils();
    var dijkstra = require_dijkstra();
    function getStringByteLength(str) {
      return unescape(encodeURIComponent(str)).length;
    }
    function getSegments(regex, mode, str) {
      const segments = [];
      let result;
      while ((result = regex.exec(str)) !== null) {
        segments.push({
          data: result[0],
          index: result.index,
          mode,
          length: result[0].length
        });
      }
      return segments;
    }
    function getSegmentsFromString(dataStr) {
      const numSegs = getSegments(Regex.NUMERIC, Mode.NUMERIC, dataStr);
      const alphaNumSegs = getSegments(Regex.ALPHANUMERIC, Mode.ALPHANUMERIC, dataStr);
      let byteSegs;
      let kanjiSegs;
      if (Utils.isKanjiModeEnabled()) {
        byteSegs = getSegments(Regex.BYTE, Mode.BYTE, dataStr);
        kanjiSegs = getSegments(Regex.KANJI, Mode.KANJI, dataStr);
      } else {
        byteSegs = getSegments(Regex.BYTE_KANJI, Mode.BYTE, dataStr);
        kanjiSegs = [];
      }
      const segs = numSegs.concat(alphaNumSegs, byteSegs, kanjiSegs);
      return segs.sort(function(s1, s2) {
        return s1.index - s2.index;
      }).map(function(obj) {
        return {
          data: obj.data,
          mode: obj.mode,
          length: obj.length
        };
      });
    }
    function getSegmentBitsLength(length, mode) {
      switch (mode) {
        case Mode.NUMERIC:
          return NumericData.getBitsLength(length);
        case Mode.ALPHANUMERIC:
          return AlphanumericData.getBitsLength(length);
        case Mode.KANJI:
          return KanjiData.getBitsLength(length);
        case Mode.BYTE:
          return ByteData.getBitsLength(length);
      }
    }
    function mergeSegments(segs) {
      return segs.reduce(function(acc, curr) {
        const prevSeg = acc.length - 1 >= 0 ? acc[acc.length - 1] : null;
        if (prevSeg && prevSeg.mode === curr.mode) {
          acc[acc.length - 1].data += curr.data;
          return acc;
        }
        acc.push(curr);
        return acc;
      }, []);
    }
    function buildNodes(segs) {
      const nodes = [];
      for (let i = 0; i < segs.length; i++) {
        const seg = segs[i];
        switch (seg.mode) {
          case Mode.NUMERIC:
            nodes.push([
              seg,
              { data: seg.data, mode: Mode.ALPHANUMERIC, length: seg.length },
              { data: seg.data, mode: Mode.BYTE, length: seg.length }
            ]);
            break;
          case Mode.ALPHANUMERIC:
            nodes.push([
              seg,
              { data: seg.data, mode: Mode.BYTE, length: seg.length }
            ]);
            break;
          case Mode.KANJI:
            nodes.push([
              seg,
              { data: seg.data, mode: Mode.BYTE, length: getStringByteLength(seg.data) }
            ]);
            break;
          case Mode.BYTE:
            nodes.push([
              { data: seg.data, mode: Mode.BYTE, length: getStringByteLength(seg.data) }
            ]);
        }
      }
      return nodes;
    }
    function buildGraph(nodes, version) {
      const table = {};
      const graph = { start: {} };
      let prevNodeIds = ["start"];
      for (let i = 0; i < nodes.length; i++) {
        const nodeGroup = nodes[i];
        const currentNodeIds = [];
        for (let j = 0; j < nodeGroup.length; j++) {
          const node = nodeGroup[j];
          const key = "" + i + j;
          currentNodeIds.push(key);
          table[key] = { node, lastCount: 0 };
          graph[key] = {};
          for (let n = 0; n < prevNodeIds.length; n++) {
            const prevNodeId = prevNodeIds[n];
            if (table[prevNodeId] && table[prevNodeId].node.mode === node.mode) {
              graph[prevNodeId][key] = getSegmentBitsLength(table[prevNodeId].lastCount + node.length, node.mode) - getSegmentBitsLength(table[prevNodeId].lastCount, node.mode);
              table[prevNodeId].lastCount += node.length;
            } else {
              if (table[prevNodeId]) table[prevNodeId].lastCount = node.length;
              graph[prevNodeId][key] = getSegmentBitsLength(node.length, node.mode) + 4 + Mode.getCharCountIndicator(node.mode, version);
            }
          }
        }
        prevNodeIds = currentNodeIds;
      }
      for (let n = 0; n < prevNodeIds.length; n++) {
        graph[prevNodeIds[n]].end = 0;
      }
      return { map: graph, table };
    }
    function buildSingleSegment(data, modesHint) {
      let mode;
      const bestMode = Mode.getBestModeForData(data);
      mode = Mode.from(modesHint, bestMode);
      if (mode !== Mode.BYTE && mode.bit < bestMode.bit) {
        throw new Error('"' + data + '" cannot be encoded with mode ' + Mode.toString(mode) + ".\n Suggested mode is: " + Mode.toString(bestMode));
      }
      if (mode === Mode.KANJI && !Utils.isKanjiModeEnabled()) {
        mode = Mode.BYTE;
      }
      switch (mode) {
        case Mode.NUMERIC:
          return new NumericData(data);
        case Mode.ALPHANUMERIC:
          return new AlphanumericData(data);
        case Mode.KANJI:
          return new KanjiData(data);
        case Mode.BYTE:
          return new ByteData(data);
      }
    }
    exports.fromArray = function fromArray(array) {
      return array.reduce(function(acc, seg) {
        if (typeof seg === "string") {
          acc.push(buildSingleSegment(seg, null));
        } else if (seg.data) {
          acc.push(buildSingleSegment(seg.data, seg.mode));
        }
        return acc;
      }, []);
    };
    exports.fromString = function fromString(data, version) {
      const segs = getSegmentsFromString(data, Utils.isKanjiModeEnabled());
      const nodes = buildNodes(segs);
      const graph = buildGraph(nodes, version);
      const path3 = dijkstra.find_path(graph.map, "start", "end");
      const optimizedSegs = [];
      for (let i = 1; i < path3.length - 1; i++) {
        optimizedSegs.push(graph.table[path3[i]].node);
      }
      return exports.fromArray(mergeSegments(optimizedSegs));
    };
    exports.rawSplit = function rawSplit(data) {
      return exports.fromArray(
        getSegmentsFromString(data, Utils.isKanjiModeEnabled())
      );
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/qrcode.js
var require_qrcode = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/core/qrcode.js"(exports) {
    var Utils = require_utils();
    var ECLevel = require_error_correction_level();
    var BitBuffer = require_bit_buffer();
    var BitMatrix = require_bit_matrix();
    var AlignmentPattern = require_alignment_pattern();
    var FinderPattern = require_finder_pattern();
    var MaskPattern = require_mask_pattern();
    var ECCode = require_error_correction_code();
    var ReedSolomonEncoder = require_reed_solomon_encoder();
    var Version = require_version();
    var FormatInfo = require_format_info();
    var Mode = require_mode();
    var Segments = require_segments();
    function setupFinderPattern(matrix, version) {
      const size = matrix.size;
      const pos = FinderPattern.getPositions(version);
      for (let i = 0; i < pos.length; i++) {
        const row = pos[i][0];
        const col = pos[i][1];
        for (let r = -1; r <= 7; r++) {
          if (row + r <= -1 || size <= row + r) continue;
          for (let c = -1; c <= 7; c++) {
            if (col + c <= -1 || size <= col + c) continue;
            if (r >= 0 && r <= 6 && (c === 0 || c === 6) || c >= 0 && c <= 6 && (r === 0 || r === 6) || r >= 2 && r <= 4 && c >= 2 && c <= 4) {
              matrix.set(row + r, col + c, true, true);
            } else {
              matrix.set(row + r, col + c, false, true);
            }
          }
        }
      }
    }
    function setupTimingPattern(matrix) {
      const size = matrix.size;
      for (let r = 8; r < size - 8; r++) {
        const value = r % 2 === 0;
        matrix.set(r, 6, value, true);
        matrix.set(6, r, value, true);
      }
    }
    function setupAlignmentPattern(matrix, version) {
      const pos = AlignmentPattern.getPositions(version);
      for (let i = 0; i < pos.length; i++) {
        const row = pos[i][0];
        const col = pos[i][1];
        for (let r = -2; r <= 2; r++) {
          for (let c = -2; c <= 2; c++) {
            if (r === -2 || r === 2 || c === -2 || c === 2 || r === 0 && c === 0) {
              matrix.set(row + r, col + c, true, true);
            } else {
              matrix.set(row + r, col + c, false, true);
            }
          }
        }
      }
    }
    function setupVersionInfo(matrix, version) {
      const size = matrix.size;
      const bits = Version.getEncodedBits(version);
      let row, col, mod;
      for (let i = 0; i < 18; i++) {
        row = Math.floor(i / 3);
        col = i % 3 + size - 8 - 3;
        mod = (bits >> i & 1) === 1;
        matrix.set(row, col, mod, true);
        matrix.set(col, row, mod, true);
      }
    }
    function setupFormatInfo(matrix, errorCorrectionLevel, maskPattern) {
      const size = matrix.size;
      const bits = FormatInfo.getEncodedBits(errorCorrectionLevel, maskPattern);
      let i, mod;
      for (i = 0; i < 15; i++) {
        mod = (bits >> i & 1) === 1;
        if (i < 6) {
          matrix.set(i, 8, mod, true);
        } else if (i < 8) {
          matrix.set(i + 1, 8, mod, true);
        } else {
          matrix.set(size - 15 + i, 8, mod, true);
        }
        if (i < 8) {
          matrix.set(8, size - i - 1, mod, true);
        } else if (i < 9) {
          matrix.set(8, 15 - i - 1 + 1, mod, true);
        } else {
          matrix.set(8, 15 - i - 1, mod, true);
        }
      }
      matrix.set(size - 8, 8, 1, true);
    }
    function setupData(matrix, data) {
      const size = matrix.size;
      let inc = -1;
      let row = size - 1;
      let bitIndex = 7;
      let byteIndex = 0;
      for (let col = size - 1; col > 0; col -= 2) {
        if (col === 6) col--;
        while (true) {
          for (let c = 0; c < 2; c++) {
            if (!matrix.isReserved(row, col - c)) {
              let dark = false;
              if (byteIndex < data.length) {
                dark = (data[byteIndex] >>> bitIndex & 1) === 1;
              }
              matrix.set(row, col - c, dark);
              bitIndex--;
              if (bitIndex === -1) {
                byteIndex++;
                bitIndex = 7;
              }
            }
          }
          row += inc;
          if (row < 0 || size <= row) {
            row -= inc;
            inc = -inc;
            break;
          }
        }
      }
    }
    function createData(version, errorCorrectionLevel, segments) {
      const buffer = new BitBuffer();
      segments.forEach(function(data) {
        buffer.put(data.mode.bit, 4);
        buffer.put(data.getLength(), Mode.getCharCountIndicator(data.mode, version));
        data.write(buffer);
      });
      const totalCodewords = Utils.getSymbolTotalCodewords(version);
      const ecTotalCodewords = ECCode.getTotalCodewordsCount(version, errorCorrectionLevel);
      const dataTotalCodewordsBits = (totalCodewords - ecTotalCodewords) * 8;
      if (buffer.getLengthInBits() + 4 <= dataTotalCodewordsBits) {
        buffer.put(0, 4);
      }
      while (buffer.getLengthInBits() % 8 !== 0) {
        buffer.putBit(0);
      }
      const remainingByte = (dataTotalCodewordsBits - buffer.getLengthInBits()) / 8;
      for (let i = 0; i < remainingByte; i++) {
        buffer.put(i % 2 ? 17 : 236, 8);
      }
      return createCodewords(buffer, version, errorCorrectionLevel);
    }
    function createCodewords(bitBuffer, version, errorCorrectionLevel) {
      const totalCodewords = Utils.getSymbolTotalCodewords(version);
      const ecTotalCodewords = ECCode.getTotalCodewordsCount(version, errorCorrectionLevel);
      const dataTotalCodewords = totalCodewords - ecTotalCodewords;
      const ecTotalBlocks = ECCode.getBlocksCount(version, errorCorrectionLevel);
      const blocksInGroup2 = totalCodewords % ecTotalBlocks;
      const blocksInGroup1 = ecTotalBlocks - blocksInGroup2;
      const totalCodewordsInGroup1 = Math.floor(totalCodewords / ecTotalBlocks);
      const dataCodewordsInGroup1 = Math.floor(dataTotalCodewords / ecTotalBlocks);
      const dataCodewordsInGroup2 = dataCodewordsInGroup1 + 1;
      const ecCount = totalCodewordsInGroup1 - dataCodewordsInGroup1;
      const rs = new ReedSolomonEncoder(ecCount);
      let offset = 0;
      const dcData = new Array(ecTotalBlocks);
      const ecData = new Array(ecTotalBlocks);
      let maxDataSize = 0;
      const buffer = new Uint8Array(bitBuffer.buffer);
      for (let b = 0; b < ecTotalBlocks; b++) {
        const dataSize = b < blocksInGroup1 ? dataCodewordsInGroup1 : dataCodewordsInGroup2;
        dcData[b] = buffer.slice(offset, offset + dataSize);
        ecData[b] = rs.encode(dcData[b]);
        offset += dataSize;
        maxDataSize = Math.max(maxDataSize, dataSize);
      }
      const data = new Uint8Array(totalCodewords);
      let index = 0;
      let i, r;
      for (i = 0; i < maxDataSize; i++) {
        for (r = 0; r < ecTotalBlocks; r++) {
          if (i < dcData[r].length) {
            data[index++] = dcData[r][i];
          }
        }
      }
      for (i = 0; i < ecCount; i++) {
        for (r = 0; r < ecTotalBlocks; r++) {
          data[index++] = ecData[r][i];
        }
      }
      return data;
    }
    function createSymbol(data, version, errorCorrectionLevel, maskPattern) {
      let segments;
      if (Array.isArray(data)) {
        segments = Segments.fromArray(data);
      } else if (typeof data === "string") {
        let estimatedVersion = version;
        if (!estimatedVersion) {
          const rawSegments = Segments.rawSplit(data);
          estimatedVersion = Version.getBestVersionForData(rawSegments, errorCorrectionLevel);
        }
        segments = Segments.fromString(data, estimatedVersion || 40);
      } else {
        throw new Error("Invalid data");
      }
      const bestVersion = Version.getBestVersionForData(segments, errorCorrectionLevel);
      if (!bestVersion) {
        throw new Error("The amount of data is too big to be stored in a QR Code");
      }
      if (!version) {
        version = bestVersion;
      } else if (version < bestVersion) {
        throw new Error(
          "\nThe chosen QR Code version cannot contain this amount of data.\nMinimum version required to store current data is: " + bestVersion + ".\n"
        );
      }
      const dataBits = createData(version, errorCorrectionLevel, segments);
      const moduleCount = Utils.getSymbolSize(version);
      const modules = new BitMatrix(moduleCount);
      setupFinderPattern(modules, version);
      setupTimingPattern(modules);
      setupAlignmentPattern(modules, version);
      setupFormatInfo(modules, errorCorrectionLevel, 0);
      if (version >= 7) {
        setupVersionInfo(modules, version);
      }
      setupData(modules, dataBits);
      if (isNaN(maskPattern)) {
        maskPattern = MaskPattern.getBestMask(
          modules,
          setupFormatInfo.bind(null, modules, errorCorrectionLevel)
        );
      }
      MaskPattern.applyMask(maskPattern, modules);
      setupFormatInfo(modules, errorCorrectionLevel, maskPattern);
      return {
        modules,
        version,
        errorCorrectionLevel,
        maskPattern,
        segments
      };
    }
    exports.create = function create(data, options) {
      if (typeof data === "undefined" || data === "") {
        throw new Error("No input text");
      }
      let errorCorrectionLevel = ECLevel.M;
      let version;
      let mask;
      if (typeof options !== "undefined") {
        errorCorrectionLevel = ECLevel.from(options.errorCorrectionLevel, ECLevel.M);
        version = Version.from(options.version);
        mask = MaskPattern.from(options.maskPattern);
        if (options.toSJISFunc) {
          Utils.setToSJISFunction(options.toSJISFunc);
        }
      }
      return createSymbol(data, version, errorCorrectionLevel, mask);
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/chunkstream.js
var require_chunkstream = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/chunkstream.js"(exports, module) {
    "use strict";
    var util = __require("util");
    var Stream = __require("stream");
    var ChunkStream = module.exports = function() {
      Stream.call(this);
      this._buffers = [];
      this._buffered = 0;
      this._reads = [];
      this._paused = false;
      this._encoding = "utf8";
      this.writable = true;
    };
    util.inherits(ChunkStream, Stream);
    ChunkStream.prototype.read = function(length, callback) {
      this._reads.push({
        length: Math.abs(length),
        // if length < 0 then at most this length
        allowLess: length < 0,
        func: callback
      });
      process.nextTick(
        function() {
          this._process();
          if (this._paused && this._reads && this._reads.length > 0) {
            this._paused = false;
            this.emit("drain");
          }
        }.bind(this)
      );
    };
    ChunkStream.prototype.write = function(data, encoding) {
      if (!this.writable) {
        this.emit("error", new Error("Stream not writable"));
        return false;
      }
      let dataBuffer;
      if (Buffer.isBuffer(data)) {
        dataBuffer = data;
      } else {
        dataBuffer = Buffer.from(data, encoding || this._encoding);
      }
      this._buffers.push(dataBuffer);
      this._buffered += dataBuffer.length;
      this._process();
      if (this._reads && this._reads.length === 0) {
        this._paused = true;
      }
      return this.writable && !this._paused;
    };
    ChunkStream.prototype.end = function(data, encoding) {
      if (data) {
        this.write(data, encoding);
      }
      this.writable = false;
      if (!this._buffers) {
        return;
      }
      if (this._buffers.length === 0) {
        this._end();
      } else {
        this._buffers.push(null);
        this._process();
      }
    };
    ChunkStream.prototype.destroySoon = ChunkStream.prototype.end;
    ChunkStream.prototype._end = function() {
      if (this._reads.length > 0) {
        this.emit("error", new Error("Unexpected end of input"));
      }
      this.destroy();
    };
    ChunkStream.prototype.destroy = function() {
      if (!this._buffers) {
        return;
      }
      this.writable = false;
      this._reads = null;
      this._buffers = null;
      this.emit("close");
    };
    ChunkStream.prototype._processReadAllowingLess = function(read) {
      this._reads.shift();
      let smallerBuf = this._buffers[0];
      if (smallerBuf.length > read.length) {
        this._buffered -= read.length;
        this._buffers[0] = smallerBuf.slice(read.length);
        read.func.call(this, smallerBuf.slice(0, read.length));
      } else {
        this._buffered -= smallerBuf.length;
        this._buffers.shift();
        read.func.call(this, smallerBuf);
      }
    };
    ChunkStream.prototype._processRead = function(read) {
      this._reads.shift();
      let pos = 0;
      let count = 0;
      let data = Buffer.alloc(read.length);
      while (pos < read.length) {
        let buf = this._buffers[count++];
        let len = Math.min(buf.length, read.length - pos);
        buf.copy(data, pos, 0, len);
        pos += len;
        if (len !== buf.length) {
          this._buffers[--count] = buf.slice(len);
        }
      }
      if (count > 0) {
        this._buffers.splice(0, count);
      }
      this._buffered -= read.length;
      read.func.call(this, data);
    };
    ChunkStream.prototype._process = function() {
      try {
        while (this._buffered > 0 && this._reads && this._reads.length > 0) {
          let read = this._reads[0];
          if (read.allowLess) {
            this._processReadAllowingLess(read);
          } else if (this._buffered >= read.length) {
            this._processRead(read);
          } else {
            break;
          }
        }
        if (this._buffers && !this.writable) {
          this._end();
        }
      } catch (ex) {
        this.emit("error", ex);
      }
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/interlace.js
var require_interlace = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/interlace.js"(exports) {
    "use strict";
    var imagePasses = [
      {
        // pass 1 - 1px
        x: [0],
        y: [0]
      },
      {
        // pass 2 - 1px
        x: [4],
        y: [0]
      },
      {
        // pass 3 - 2px
        x: [0, 4],
        y: [4]
      },
      {
        // pass 4 - 4px
        x: [2, 6],
        y: [0, 4]
      },
      {
        // pass 5 - 8px
        x: [0, 2, 4, 6],
        y: [2, 6]
      },
      {
        // pass 6 - 16px
        x: [1, 3, 5, 7],
        y: [0, 2, 4, 6]
      },
      {
        // pass 7 - 32px
        x: [0, 1, 2, 3, 4, 5, 6, 7],
        y: [1, 3, 5, 7]
      }
    ];
    exports.getImagePasses = function(width, height) {
      let images = [];
      let xLeftOver = width % 8;
      let yLeftOver = height % 8;
      let xRepeats = (width - xLeftOver) / 8;
      let yRepeats = (height - yLeftOver) / 8;
      for (let i = 0; i < imagePasses.length; i++) {
        let pass = imagePasses[i];
        let passWidth = xRepeats * pass.x.length;
        let passHeight = yRepeats * pass.y.length;
        for (let j = 0; j < pass.x.length; j++) {
          if (pass.x[j] < xLeftOver) {
            passWidth++;
          } else {
            break;
          }
        }
        for (let j = 0; j < pass.y.length; j++) {
          if (pass.y[j] < yLeftOver) {
            passHeight++;
          } else {
            break;
          }
        }
        if (passWidth > 0 && passHeight > 0) {
          images.push({ width: passWidth, height: passHeight, index: i });
        }
      }
      return images;
    };
    exports.getInterlaceIterator = function(width) {
      return function(x, y, pass) {
        let outerXLeftOver = x % imagePasses[pass].x.length;
        let outerX = (x - outerXLeftOver) / imagePasses[pass].x.length * 8 + imagePasses[pass].x[outerXLeftOver];
        let outerYLeftOver = y % imagePasses[pass].y.length;
        let outerY = (y - outerYLeftOver) / imagePasses[pass].y.length * 8 + imagePasses[pass].y[outerYLeftOver];
        return outerX * 4 + outerY * width * 4;
      };
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/paeth-predictor.js
var require_paeth_predictor = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/paeth-predictor.js"(exports, module) {
    "use strict";
    module.exports = function paethPredictor(left, above, upLeft) {
      let paeth = left + above - upLeft;
      let pLeft = Math.abs(paeth - left);
      let pAbove = Math.abs(paeth - above);
      let pUpLeft = Math.abs(paeth - upLeft);
      if (pLeft <= pAbove && pLeft <= pUpLeft) {
        return left;
      }
      if (pAbove <= pUpLeft) {
        return above;
      }
      return upLeft;
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/filter-parse.js
var require_filter_parse = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/filter-parse.js"(exports, module) {
    "use strict";
    var interlaceUtils = require_interlace();
    var paethPredictor = require_paeth_predictor();
    function getByteWidth(width, bpp, depth) {
      let byteWidth = width * bpp;
      if (depth !== 8) {
        byteWidth = Math.ceil(byteWidth / (8 / depth));
      }
      return byteWidth;
    }
    var Filter = module.exports = function(bitmapInfo, dependencies) {
      let width = bitmapInfo.width;
      let height = bitmapInfo.height;
      let interlace = bitmapInfo.interlace;
      let bpp = bitmapInfo.bpp;
      let depth = bitmapInfo.depth;
      this.read = dependencies.read;
      this.write = dependencies.write;
      this.complete = dependencies.complete;
      this._imageIndex = 0;
      this._images = [];
      if (interlace) {
        let passes = interlaceUtils.getImagePasses(width, height);
        for (let i = 0; i < passes.length; i++) {
          this._images.push({
            byteWidth: getByteWidth(passes[i].width, bpp, depth),
            height: passes[i].height,
            lineIndex: 0
          });
        }
      } else {
        this._images.push({
          byteWidth: getByteWidth(width, bpp, depth),
          height,
          lineIndex: 0
        });
      }
      if (depth === 8) {
        this._xComparison = bpp;
      } else if (depth === 16) {
        this._xComparison = bpp * 2;
      } else {
        this._xComparison = 1;
      }
    };
    Filter.prototype.start = function() {
      this.read(
        this._images[this._imageIndex].byteWidth + 1,
        this._reverseFilterLine.bind(this)
      );
    };
    Filter.prototype._unFilterType1 = function(rawData, unfilteredLine, byteWidth) {
      let xComparison = this._xComparison;
      let xBiggerThan = xComparison - 1;
      for (let x = 0; x < byteWidth; x++) {
        let rawByte = rawData[1 + x];
        let f1Left = x > xBiggerThan ? unfilteredLine[x - xComparison] : 0;
        unfilteredLine[x] = rawByte + f1Left;
      }
    };
    Filter.prototype._unFilterType2 = function(rawData, unfilteredLine, byteWidth) {
      let lastLine = this._lastLine;
      for (let x = 0; x < byteWidth; x++) {
        let rawByte = rawData[1 + x];
        let f2Up = lastLine ? lastLine[x] : 0;
        unfilteredLine[x] = rawByte + f2Up;
      }
    };
    Filter.prototype._unFilterType3 = function(rawData, unfilteredLine, byteWidth) {
      let xComparison = this._xComparison;
      let xBiggerThan = xComparison - 1;
      let lastLine = this._lastLine;
      for (let x = 0; x < byteWidth; x++) {
        let rawByte = rawData[1 + x];
        let f3Up = lastLine ? lastLine[x] : 0;
        let f3Left = x > xBiggerThan ? unfilteredLine[x - xComparison] : 0;
        let f3Add = Math.floor((f3Left + f3Up) / 2);
        unfilteredLine[x] = rawByte + f3Add;
      }
    };
    Filter.prototype._unFilterType4 = function(rawData, unfilteredLine, byteWidth) {
      let xComparison = this._xComparison;
      let xBiggerThan = xComparison - 1;
      let lastLine = this._lastLine;
      for (let x = 0; x < byteWidth; x++) {
        let rawByte = rawData[1 + x];
        let f4Up = lastLine ? lastLine[x] : 0;
        let f4Left = x > xBiggerThan ? unfilteredLine[x - xComparison] : 0;
        let f4UpLeft = x > xBiggerThan && lastLine ? lastLine[x - xComparison] : 0;
        let f4Add = paethPredictor(f4Left, f4Up, f4UpLeft);
        unfilteredLine[x] = rawByte + f4Add;
      }
    };
    Filter.prototype._reverseFilterLine = function(rawData) {
      let filter = rawData[0];
      let unfilteredLine;
      let currentImage = this._images[this._imageIndex];
      let byteWidth = currentImage.byteWidth;
      if (filter === 0) {
        unfilteredLine = rawData.slice(1, byteWidth + 1);
      } else {
        unfilteredLine = Buffer.alloc(byteWidth);
        switch (filter) {
          case 1:
            this._unFilterType1(rawData, unfilteredLine, byteWidth);
            break;
          case 2:
            this._unFilterType2(rawData, unfilteredLine, byteWidth);
            break;
          case 3:
            this._unFilterType3(rawData, unfilteredLine, byteWidth);
            break;
          case 4:
            this._unFilterType4(rawData, unfilteredLine, byteWidth);
            break;
          default:
            throw new Error("Unrecognised filter type - " + filter);
        }
      }
      this.write(unfilteredLine);
      currentImage.lineIndex++;
      if (currentImage.lineIndex >= currentImage.height) {
        this._lastLine = null;
        this._imageIndex++;
        currentImage = this._images[this._imageIndex];
      } else {
        this._lastLine = unfilteredLine;
      }
      if (currentImage) {
        this.read(currentImage.byteWidth + 1, this._reverseFilterLine.bind(this));
      } else {
        this._lastLine = null;
        this.complete();
      }
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/filter-parse-async.js
var require_filter_parse_async = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/filter-parse-async.js"(exports, module) {
    "use strict";
    var util = __require("util");
    var ChunkStream = require_chunkstream();
    var Filter = require_filter_parse();
    var FilterAsync = module.exports = function(bitmapInfo) {
      ChunkStream.call(this);
      let buffers = [];
      let that = this;
      this._filter = new Filter(bitmapInfo, {
        read: this.read.bind(this),
        write: function(buffer) {
          buffers.push(buffer);
        },
        complete: function() {
          that.emit("complete", Buffer.concat(buffers));
        }
      });
      this._filter.start();
    };
    util.inherits(FilterAsync, ChunkStream);
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/constants.js
var require_constants = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/constants.js"(exports, module) {
    "use strict";
    module.exports = {
      PNG_SIGNATURE: [137, 80, 78, 71, 13, 10, 26, 10],
      TYPE_IHDR: 1229472850,
      TYPE_IEND: 1229278788,
      TYPE_IDAT: 1229209940,
      TYPE_PLTE: 1347179589,
      TYPE_tRNS: 1951551059,
      // eslint-disable-line camelcase
      TYPE_gAMA: 1732332865,
      // eslint-disable-line camelcase
      // color-type bits
      COLORTYPE_GRAYSCALE: 0,
      COLORTYPE_PALETTE: 1,
      COLORTYPE_COLOR: 2,
      COLORTYPE_ALPHA: 4,
      // e.g. grayscale and alpha
      // color-type combinations
      COLORTYPE_PALETTE_COLOR: 3,
      COLORTYPE_COLOR_ALPHA: 6,
      COLORTYPE_TO_BPP_MAP: {
        0: 1,
        2: 3,
        3: 1,
        4: 2,
        6: 4
      },
      GAMMA_DIVISION: 1e5
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/crc.js
var require_crc = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/crc.js"(exports, module) {
    "use strict";
    var crcTable = [];
    (function() {
      for (let i = 0; i < 256; i++) {
        let currentCrc = i;
        for (let j = 0; j < 8; j++) {
          if (currentCrc & 1) {
            currentCrc = 3988292384 ^ currentCrc >>> 1;
          } else {
            currentCrc = currentCrc >>> 1;
          }
        }
        crcTable[i] = currentCrc;
      }
    })();
    var CrcCalculator = module.exports = function() {
      this._crc = -1;
    };
    CrcCalculator.prototype.write = function(data) {
      for (let i = 0; i < data.length; i++) {
        this._crc = crcTable[(this._crc ^ data[i]) & 255] ^ this._crc >>> 8;
      }
      return true;
    };
    CrcCalculator.prototype.crc32 = function() {
      return this._crc ^ -1;
    };
    CrcCalculator.crc32 = function(buf) {
      let crc = -1;
      for (let i = 0; i < buf.length; i++) {
        crc = crcTable[(crc ^ buf[i]) & 255] ^ crc >>> 8;
      }
      return crc ^ -1;
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/parser.js
var require_parser = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/parser.js"(exports, module) {
    "use strict";
    var constants = require_constants();
    var CrcCalculator = require_crc();
    var Parser = module.exports = function(options, dependencies) {
      this._options = options;
      options.checkCRC = options.checkCRC !== false;
      this._hasIHDR = false;
      this._hasIEND = false;
      this._emittedHeadersFinished = false;
      this._palette = [];
      this._colorType = 0;
      this._chunks = {};
      this._chunks[constants.TYPE_IHDR] = this._handleIHDR.bind(this);
      this._chunks[constants.TYPE_IEND] = this._handleIEND.bind(this);
      this._chunks[constants.TYPE_IDAT] = this._handleIDAT.bind(this);
      this._chunks[constants.TYPE_PLTE] = this._handlePLTE.bind(this);
      this._chunks[constants.TYPE_tRNS] = this._handleTRNS.bind(this);
      this._chunks[constants.TYPE_gAMA] = this._handleGAMA.bind(this);
      this.read = dependencies.read;
      this.error = dependencies.error;
      this.metadata = dependencies.metadata;
      this.gamma = dependencies.gamma;
      this.transColor = dependencies.transColor;
      this.palette = dependencies.palette;
      this.parsed = dependencies.parsed;
      this.inflateData = dependencies.inflateData;
      this.finished = dependencies.finished;
      this.simpleTransparency = dependencies.simpleTransparency;
      this.headersFinished = dependencies.headersFinished || function() {
      };
    };
    Parser.prototype.start = function() {
      this.read(constants.PNG_SIGNATURE.length, this._parseSignature.bind(this));
    };
    Parser.prototype._parseSignature = function(data) {
      let signature = constants.PNG_SIGNATURE;
      for (let i = 0; i < signature.length; i++) {
        if (data[i] !== signature[i]) {
          this.error(new Error("Invalid file signature"));
          return;
        }
      }
      this.read(8, this._parseChunkBegin.bind(this));
    };
    Parser.prototype._parseChunkBegin = function(data) {
      let length = data.readUInt32BE(0);
      let type = data.readUInt32BE(4);
      let name = "";
      for (let i = 4; i < 8; i++) {
        name += String.fromCharCode(data[i]);
      }
      let ancillary = Boolean(data[4] & 32);
      if (!this._hasIHDR && type !== constants.TYPE_IHDR) {
        this.error(new Error("Expected IHDR on beggining"));
        return;
      }
      this._crc = new CrcCalculator();
      this._crc.write(Buffer.from(name));
      if (this._chunks[type]) {
        return this._chunks[type](length);
      }
      if (!ancillary) {
        this.error(new Error("Unsupported critical chunk type " + name));
        return;
      }
      this.read(length + 4, this._skipChunk.bind(this));
    };
    Parser.prototype._skipChunk = function() {
      this.read(8, this._parseChunkBegin.bind(this));
    };
    Parser.prototype._handleChunkEnd = function() {
      this.read(4, this._parseChunkEnd.bind(this));
    };
    Parser.prototype._parseChunkEnd = function(data) {
      let fileCrc = data.readInt32BE(0);
      let calcCrc = this._crc.crc32();
      if (this._options.checkCRC && calcCrc !== fileCrc) {
        this.error(new Error("Crc error - " + fileCrc + " - " + calcCrc));
        return;
      }
      if (!this._hasIEND) {
        this.read(8, this._parseChunkBegin.bind(this));
      }
    };
    Parser.prototype._handleIHDR = function(length) {
      this.read(length, this._parseIHDR.bind(this));
    };
    Parser.prototype._parseIHDR = function(data) {
      this._crc.write(data);
      let width = data.readUInt32BE(0);
      let height = data.readUInt32BE(4);
      let depth = data[8];
      let colorType = data[9];
      let compr = data[10];
      let filter = data[11];
      let interlace = data[12];
      if (depth !== 8 && depth !== 4 && depth !== 2 && depth !== 1 && depth !== 16) {
        this.error(new Error("Unsupported bit depth " + depth));
        return;
      }
      if (!(colorType in constants.COLORTYPE_TO_BPP_MAP)) {
        this.error(new Error("Unsupported color type"));
        return;
      }
      if (compr !== 0) {
        this.error(new Error("Unsupported compression method"));
        return;
      }
      if (filter !== 0) {
        this.error(new Error("Unsupported filter method"));
        return;
      }
      if (interlace !== 0 && interlace !== 1) {
        this.error(new Error("Unsupported interlace method"));
        return;
      }
      this._colorType = colorType;
      let bpp = constants.COLORTYPE_TO_BPP_MAP[this._colorType];
      this._hasIHDR = true;
      this.metadata({
        width,
        height,
        depth,
        interlace: Boolean(interlace),
        palette: Boolean(colorType & constants.COLORTYPE_PALETTE),
        color: Boolean(colorType & constants.COLORTYPE_COLOR),
        alpha: Boolean(colorType & constants.COLORTYPE_ALPHA),
        bpp,
        colorType
      });
      this._handleChunkEnd();
    };
    Parser.prototype._handlePLTE = function(length) {
      this.read(length, this._parsePLTE.bind(this));
    };
    Parser.prototype._parsePLTE = function(data) {
      this._crc.write(data);
      let entries = Math.floor(data.length / 3);
      for (let i = 0; i < entries; i++) {
        this._palette.push([data[i * 3], data[i * 3 + 1], data[i * 3 + 2], 255]);
      }
      this.palette(this._palette);
      this._handleChunkEnd();
    };
    Parser.prototype._handleTRNS = function(length) {
      this.simpleTransparency();
      this.read(length, this._parseTRNS.bind(this));
    };
    Parser.prototype._parseTRNS = function(data) {
      this._crc.write(data);
      if (this._colorType === constants.COLORTYPE_PALETTE_COLOR) {
        if (this._palette.length === 0) {
          this.error(new Error("Transparency chunk must be after palette"));
          return;
        }
        if (data.length > this._palette.length) {
          this.error(new Error("More transparent colors than palette size"));
          return;
        }
        for (let i = 0; i < data.length; i++) {
          this._palette[i][3] = data[i];
        }
        this.palette(this._palette);
      }
      if (this._colorType === constants.COLORTYPE_GRAYSCALE) {
        this.transColor([data.readUInt16BE(0)]);
      }
      if (this._colorType === constants.COLORTYPE_COLOR) {
        this.transColor([
          data.readUInt16BE(0),
          data.readUInt16BE(2),
          data.readUInt16BE(4)
        ]);
      }
      this._handleChunkEnd();
    };
    Parser.prototype._handleGAMA = function(length) {
      this.read(length, this._parseGAMA.bind(this));
    };
    Parser.prototype._parseGAMA = function(data) {
      this._crc.write(data);
      this.gamma(data.readUInt32BE(0) / constants.GAMMA_DIVISION);
      this._handleChunkEnd();
    };
    Parser.prototype._handleIDAT = function(length) {
      if (!this._emittedHeadersFinished) {
        this._emittedHeadersFinished = true;
        this.headersFinished();
      }
      this.read(-length, this._parseIDAT.bind(this, length));
    };
    Parser.prototype._parseIDAT = function(length, data) {
      this._crc.write(data);
      if (this._colorType === constants.COLORTYPE_PALETTE_COLOR && this._palette.length === 0) {
        throw new Error("Expected palette not found");
      }
      this.inflateData(data);
      let leftOverLength = length - data.length;
      if (leftOverLength > 0) {
        this._handleIDAT(leftOverLength);
      } else {
        this._handleChunkEnd();
      }
    };
    Parser.prototype._handleIEND = function(length) {
      this.read(length, this._parseIEND.bind(this));
    };
    Parser.prototype._parseIEND = function(data) {
      this._crc.write(data);
      this._hasIEND = true;
      this._handleChunkEnd();
      if (this.finished) {
        this.finished();
      }
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/bitmapper.js
var require_bitmapper = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/bitmapper.js"(exports) {
    "use strict";
    var interlaceUtils = require_interlace();
    var pixelBppMapper = [
      // 0 - dummy entry
      function() {
      },
      // 1 - L
      // 0: 0, 1: 0, 2: 0, 3: 0xff
      function(pxData, data, pxPos, rawPos) {
        if (rawPos === data.length) {
          throw new Error("Ran out of data");
        }
        let pixel = data[rawPos];
        pxData[pxPos] = pixel;
        pxData[pxPos + 1] = pixel;
        pxData[pxPos + 2] = pixel;
        pxData[pxPos + 3] = 255;
      },
      // 2 - LA
      // 0: 0, 1: 0, 2: 0, 3: 1
      function(pxData, data, pxPos, rawPos) {
        if (rawPos + 1 >= data.length) {
          throw new Error("Ran out of data");
        }
        let pixel = data[rawPos];
        pxData[pxPos] = pixel;
        pxData[pxPos + 1] = pixel;
        pxData[pxPos + 2] = pixel;
        pxData[pxPos + 3] = data[rawPos + 1];
      },
      // 3 - RGB
      // 0: 0, 1: 1, 2: 2, 3: 0xff
      function(pxData, data, pxPos, rawPos) {
        if (rawPos + 2 >= data.length) {
          throw new Error("Ran out of data");
        }
        pxData[pxPos] = data[rawPos];
        pxData[pxPos + 1] = data[rawPos + 1];
        pxData[pxPos + 2] = data[rawPos + 2];
        pxData[pxPos + 3] = 255;
      },
      // 4 - RGBA
      // 0: 0, 1: 1, 2: 2, 3: 3
      function(pxData, data, pxPos, rawPos) {
        if (rawPos + 3 >= data.length) {
          throw new Error("Ran out of data");
        }
        pxData[pxPos] = data[rawPos];
        pxData[pxPos + 1] = data[rawPos + 1];
        pxData[pxPos + 2] = data[rawPos + 2];
        pxData[pxPos + 3] = data[rawPos + 3];
      }
    ];
    var pixelBppCustomMapper = [
      // 0 - dummy entry
      function() {
      },
      // 1 - L
      // 0: 0, 1: 0, 2: 0, 3: 0xff
      function(pxData, pixelData, pxPos, maxBit) {
        let pixel = pixelData[0];
        pxData[pxPos] = pixel;
        pxData[pxPos + 1] = pixel;
        pxData[pxPos + 2] = pixel;
        pxData[pxPos + 3] = maxBit;
      },
      // 2 - LA
      // 0: 0, 1: 0, 2: 0, 3: 1
      function(pxData, pixelData, pxPos) {
        let pixel = pixelData[0];
        pxData[pxPos] = pixel;
        pxData[pxPos + 1] = pixel;
        pxData[pxPos + 2] = pixel;
        pxData[pxPos + 3] = pixelData[1];
      },
      // 3 - RGB
      // 0: 0, 1: 1, 2: 2, 3: 0xff
      function(pxData, pixelData, pxPos, maxBit) {
        pxData[pxPos] = pixelData[0];
        pxData[pxPos + 1] = pixelData[1];
        pxData[pxPos + 2] = pixelData[2];
        pxData[pxPos + 3] = maxBit;
      },
      // 4 - RGBA
      // 0: 0, 1: 1, 2: 2, 3: 3
      function(pxData, pixelData, pxPos) {
        pxData[pxPos] = pixelData[0];
        pxData[pxPos + 1] = pixelData[1];
        pxData[pxPos + 2] = pixelData[2];
        pxData[pxPos + 3] = pixelData[3];
      }
    ];
    function bitRetriever(data, depth) {
      let leftOver = [];
      let i = 0;
      function split() {
        if (i === data.length) {
          throw new Error("Ran out of data");
        }
        let byte = data[i];
        i++;
        let byte8, byte7, byte6, byte5, byte4, byte3, byte2, byte1;
        switch (depth) {
          default:
            throw new Error("unrecognised depth");
          case 16:
            byte2 = data[i];
            i++;
            leftOver.push((byte << 8) + byte2);
            break;
          case 4:
            byte2 = byte & 15;
            byte1 = byte >> 4;
            leftOver.push(byte1, byte2);
            break;
          case 2:
            byte4 = byte & 3;
            byte3 = byte >> 2 & 3;
            byte2 = byte >> 4 & 3;
            byte1 = byte >> 6 & 3;
            leftOver.push(byte1, byte2, byte3, byte4);
            break;
          case 1:
            byte8 = byte & 1;
            byte7 = byte >> 1 & 1;
            byte6 = byte >> 2 & 1;
            byte5 = byte >> 3 & 1;
            byte4 = byte >> 4 & 1;
            byte3 = byte >> 5 & 1;
            byte2 = byte >> 6 & 1;
            byte1 = byte >> 7 & 1;
            leftOver.push(byte1, byte2, byte3, byte4, byte5, byte6, byte7, byte8);
            break;
        }
      }
      return {
        get: function(count) {
          while (leftOver.length < count) {
            split();
          }
          let returner = leftOver.slice(0, count);
          leftOver = leftOver.slice(count);
          return returner;
        },
        resetAfterLine: function() {
          leftOver.length = 0;
        },
        end: function() {
          if (i !== data.length) {
            throw new Error("extra data found");
          }
        }
      };
    }
    function mapImage8Bit(image, pxData, getPxPos, bpp, data, rawPos) {
      let imageWidth = image.width;
      let imageHeight = image.height;
      let imagePass = image.index;
      for (let y = 0; y < imageHeight; y++) {
        for (let x = 0; x < imageWidth; x++) {
          let pxPos = getPxPos(x, y, imagePass);
          pixelBppMapper[bpp](pxData, data, pxPos, rawPos);
          rawPos += bpp;
        }
      }
      return rawPos;
    }
    function mapImageCustomBit(image, pxData, getPxPos, bpp, bits, maxBit) {
      let imageWidth = image.width;
      let imageHeight = image.height;
      let imagePass = image.index;
      for (let y = 0; y < imageHeight; y++) {
        for (let x = 0; x < imageWidth; x++) {
          let pixelData = bits.get(bpp);
          let pxPos = getPxPos(x, y, imagePass);
          pixelBppCustomMapper[bpp](pxData, pixelData, pxPos, maxBit);
        }
        bits.resetAfterLine();
      }
    }
    exports.dataToBitMap = function(data, bitmapInfo) {
      let width = bitmapInfo.width;
      let height = bitmapInfo.height;
      let depth = bitmapInfo.depth;
      let bpp = bitmapInfo.bpp;
      let interlace = bitmapInfo.interlace;
      let bits;
      if (depth !== 8) {
        bits = bitRetriever(data, depth);
      }
      let pxData;
      if (depth <= 8) {
        pxData = Buffer.alloc(width * height * 4);
      } else {
        pxData = new Uint16Array(width * height * 4);
      }
      let maxBit = Math.pow(2, depth) - 1;
      let rawPos = 0;
      let images;
      let getPxPos;
      if (interlace) {
        images = interlaceUtils.getImagePasses(width, height);
        getPxPos = interlaceUtils.getInterlaceIterator(width, height);
      } else {
        let nonInterlacedPxPos = 0;
        getPxPos = function() {
          let returner = nonInterlacedPxPos;
          nonInterlacedPxPos += 4;
          return returner;
        };
        images = [{ width, height }];
      }
      for (let imageIndex = 0; imageIndex < images.length; imageIndex++) {
        if (depth === 8) {
          rawPos = mapImage8Bit(
            images[imageIndex],
            pxData,
            getPxPos,
            bpp,
            data,
            rawPos
          );
        } else {
          mapImageCustomBit(
            images[imageIndex],
            pxData,
            getPxPos,
            bpp,
            bits,
            maxBit
          );
        }
      }
      if (depth === 8) {
        if (rawPos !== data.length) {
          throw new Error("extra data found");
        }
      } else {
        bits.end();
      }
      return pxData;
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/format-normaliser.js
var require_format_normaliser = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/format-normaliser.js"(exports, module) {
    "use strict";
    function dePalette(indata, outdata, width, height, palette) {
      let pxPos = 0;
      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          let color = palette[indata[pxPos]];
          if (!color) {
            throw new Error("index " + indata[pxPos] + " not in palette");
          }
          for (let i = 0; i < 4; i++) {
            outdata[pxPos + i] = color[i];
          }
          pxPos += 4;
        }
      }
    }
    function replaceTransparentColor(indata, outdata, width, height, transColor) {
      let pxPos = 0;
      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          let makeTrans = false;
          if (transColor.length === 1) {
            if (transColor[0] === indata[pxPos]) {
              makeTrans = true;
            }
          } else if (transColor[0] === indata[pxPos] && transColor[1] === indata[pxPos + 1] && transColor[2] === indata[pxPos + 2]) {
            makeTrans = true;
          }
          if (makeTrans) {
            for (let i = 0; i < 4; i++) {
              outdata[pxPos + i] = 0;
            }
          }
          pxPos += 4;
        }
      }
    }
    function scaleDepth(indata, outdata, width, height, depth) {
      let maxOutSample = 255;
      let maxInSample = Math.pow(2, depth) - 1;
      let pxPos = 0;
      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          for (let i = 0; i < 4; i++) {
            outdata[pxPos + i] = Math.floor(
              indata[pxPos + i] * maxOutSample / maxInSample + 0.5
            );
          }
          pxPos += 4;
        }
      }
    }
    module.exports = function(indata, imageData) {
      let depth = imageData.depth;
      let width = imageData.width;
      let height = imageData.height;
      let colorType = imageData.colorType;
      let transColor = imageData.transColor;
      let palette = imageData.palette;
      let outdata = indata;
      if (colorType === 3) {
        dePalette(indata, outdata, width, height, palette);
      } else {
        if (transColor) {
          replaceTransparentColor(indata, outdata, width, height, transColor);
        }
        if (depth !== 8) {
          if (depth === 16) {
            outdata = Buffer.alloc(width * height * 4);
          }
          scaleDepth(indata, outdata, width, height, depth);
        }
      }
      return outdata;
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/parser-async.js
var require_parser_async = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/parser-async.js"(exports, module) {
    "use strict";
    var util = __require("util");
    var zlib = __require("zlib");
    var ChunkStream = require_chunkstream();
    var FilterAsync = require_filter_parse_async();
    var Parser = require_parser();
    var bitmapper = require_bitmapper();
    var formatNormaliser = require_format_normaliser();
    var ParserAsync = module.exports = function(options) {
      ChunkStream.call(this);
      this._parser = new Parser(options, {
        read: this.read.bind(this),
        error: this._handleError.bind(this),
        metadata: this._handleMetaData.bind(this),
        gamma: this.emit.bind(this, "gamma"),
        palette: this._handlePalette.bind(this),
        transColor: this._handleTransColor.bind(this),
        finished: this._finished.bind(this),
        inflateData: this._inflateData.bind(this),
        simpleTransparency: this._simpleTransparency.bind(this),
        headersFinished: this._headersFinished.bind(this)
      });
      this._options = options;
      this.writable = true;
      this._parser.start();
    };
    util.inherits(ParserAsync, ChunkStream);
    ParserAsync.prototype._handleError = function(err) {
      this.emit("error", err);
      this.writable = false;
      this.destroy();
      if (this._inflate && this._inflate.destroy) {
        this._inflate.destroy();
      }
      if (this._filter) {
        this._filter.destroy();
        this._filter.on("error", function() {
        });
      }
      this.errord = true;
    };
    ParserAsync.prototype._inflateData = function(data) {
      if (!this._inflate) {
        if (this._bitmapInfo.interlace) {
          this._inflate = zlib.createInflate();
          this._inflate.on("error", this.emit.bind(this, "error"));
          this._filter.on("complete", this._complete.bind(this));
          this._inflate.pipe(this._filter);
        } else {
          let rowSize = (this._bitmapInfo.width * this._bitmapInfo.bpp * this._bitmapInfo.depth + 7 >> 3) + 1;
          let imageSize = rowSize * this._bitmapInfo.height;
          let chunkSize = Math.max(imageSize, zlib.Z_MIN_CHUNK);
          this._inflate = zlib.createInflate({ chunkSize });
          let leftToInflate = imageSize;
          let emitError = this.emit.bind(this, "error");
          this._inflate.on("error", function(err) {
            if (!leftToInflate) {
              return;
            }
            emitError(err);
          });
          this._filter.on("complete", this._complete.bind(this));
          let filterWrite = this._filter.write.bind(this._filter);
          this._inflate.on("data", function(chunk) {
            if (!leftToInflate) {
              return;
            }
            if (chunk.length > leftToInflate) {
              chunk = chunk.slice(0, leftToInflate);
            }
            leftToInflate -= chunk.length;
            filterWrite(chunk);
          });
          this._inflate.on("end", this._filter.end.bind(this._filter));
        }
      }
      this._inflate.write(data);
    };
    ParserAsync.prototype._handleMetaData = function(metaData) {
      this._metaData = metaData;
      this._bitmapInfo = Object.create(metaData);
      this._filter = new FilterAsync(this._bitmapInfo);
    };
    ParserAsync.prototype._handleTransColor = function(transColor) {
      this._bitmapInfo.transColor = transColor;
    };
    ParserAsync.prototype._handlePalette = function(palette) {
      this._bitmapInfo.palette = palette;
    };
    ParserAsync.prototype._simpleTransparency = function() {
      this._metaData.alpha = true;
    };
    ParserAsync.prototype._headersFinished = function() {
      this.emit("metadata", this._metaData);
    };
    ParserAsync.prototype._finished = function() {
      if (this.errord) {
        return;
      }
      if (!this._inflate) {
        this.emit("error", "No Inflate block");
      } else {
        this._inflate.end();
      }
    };
    ParserAsync.prototype._complete = function(filteredData) {
      if (this.errord) {
        return;
      }
      let normalisedBitmapData;
      try {
        let bitmapData = bitmapper.dataToBitMap(filteredData, this._bitmapInfo);
        normalisedBitmapData = formatNormaliser(bitmapData, this._bitmapInfo);
        bitmapData = null;
      } catch (ex) {
        this._handleError(ex);
        return;
      }
      this.emit("parsed", normalisedBitmapData);
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/bitpacker.js
var require_bitpacker = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/bitpacker.js"(exports, module) {
    "use strict";
    var constants = require_constants();
    module.exports = function(dataIn, width, height, options) {
      let outHasAlpha = [constants.COLORTYPE_COLOR_ALPHA, constants.COLORTYPE_ALPHA].indexOf(
        options.colorType
      ) !== -1;
      if (options.colorType === options.inputColorType) {
        let bigEndian = (function() {
          let buffer = new ArrayBuffer(2);
          new DataView(buffer).setInt16(
            0,
            256,
            true
            /* littleEndian */
          );
          return new Int16Array(buffer)[0] !== 256;
        })();
        if (options.bitDepth === 8 || options.bitDepth === 16 && bigEndian) {
          return dataIn;
        }
      }
      let data = options.bitDepth !== 16 ? dataIn : new Uint16Array(dataIn.buffer);
      let maxValue = 255;
      let inBpp = constants.COLORTYPE_TO_BPP_MAP[options.inputColorType];
      if (inBpp === 4 && !options.inputHasAlpha) {
        inBpp = 3;
      }
      let outBpp = constants.COLORTYPE_TO_BPP_MAP[options.colorType];
      if (options.bitDepth === 16) {
        maxValue = 65535;
        outBpp *= 2;
      }
      let outData = Buffer.alloc(width * height * outBpp);
      let inIndex = 0;
      let outIndex = 0;
      let bgColor = options.bgColor || {};
      if (bgColor.red === void 0) {
        bgColor.red = maxValue;
      }
      if (bgColor.green === void 0) {
        bgColor.green = maxValue;
      }
      if (bgColor.blue === void 0) {
        bgColor.blue = maxValue;
      }
      function getRGBA() {
        let red;
        let green;
        let blue;
        let alpha = maxValue;
        switch (options.inputColorType) {
          case constants.COLORTYPE_COLOR_ALPHA:
            alpha = data[inIndex + 3];
            red = data[inIndex];
            green = data[inIndex + 1];
            blue = data[inIndex + 2];
            break;
          case constants.COLORTYPE_COLOR:
            red = data[inIndex];
            green = data[inIndex + 1];
            blue = data[inIndex + 2];
            break;
          case constants.COLORTYPE_ALPHA:
            alpha = data[inIndex + 1];
            red = data[inIndex];
            green = red;
            blue = red;
            break;
          case constants.COLORTYPE_GRAYSCALE:
            red = data[inIndex];
            green = red;
            blue = red;
            break;
          default:
            throw new Error(
              "input color type:" + options.inputColorType + " is not supported at present"
            );
        }
        if (options.inputHasAlpha) {
          if (!outHasAlpha) {
            alpha /= maxValue;
            red = Math.min(
              Math.max(Math.round((1 - alpha) * bgColor.red + alpha * red), 0),
              maxValue
            );
            green = Math.min(
              Math.max(Math.round((1 - alpha) * bgColor.green + alpha * green), 0),
              maxValue
            );
            blue = Math.min(
              Math.max(Math.round((1 - alpha) * bgColor.blue + alpha * blue), 0),
              maxValue
            );
          }
        }
        return { red, green, blue, alpha };
      }
      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          let rgba = getRGBA(data, inIndex);
          switch (options.colorType) {
            case constants.COLORTYPE_COLOR_ALPHA:
            case constants.COLORTYPE_COLOR:
              if (options.bitDepth === 8) {
                outData[outIndex] = rgba.red;
                outData[outIndex + 1] = rgba.green;
                outData[outIndex + 2] = rgba.blue;
                if (outHasAlpha) {
                  outData[outIndex + 3] = rgba.alpha;
                }
              } else {
                outData.writeUInt16BE(rgba.red, outIndex);
                outData.writeUInt16BE(rgba.green, outIndex + 2);
                outData.writeUInt16BE(rgba.blue, outIndex + 4);
                if (outHasAlpha) {
                  outData.writeUInt16BE(rgba.alpha, outIndex + 6);
                }
              }
              break;
            case constants.COLORTYPE_ALPHA:
            case constants.COLORTYPE_GRAYSCALE: {
              let grayscale = (rgba.red + rgba.green + rgba.blue) / 3;
              if (options.bitDepth === 8) {
                outData[outIndex] = grayscale;
                if (outHasAlpha) {
                  outData[outIndex + 1] = rgba.alpha;
                }
              } else {
                outData.writeUInt16BE(grayscale, outIndex);
                if (outHasAlpha) {
                  outData.writeUInt16BE(rgba.alpha, outIndex + 2);
                }
              }
              break;
            }
            default:
              throw new Error("unrecognised color Type " + options.colorType);
          }
          inIndex += inBpp;
          outIndex += outBpp;
        }
      }
      return outData;
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/filter-pack.js
var require_filter_pack = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/filter-pack.js"(exports, module) {
    "use strict";
    var paethPredictor = require_paeth_predictor();
    function filterNone(pxData, pxPos, byteWidth, rawData, rawPos) {
      for (let x = 0; x < byteWidth; x++) {
        rawData[rawPos + x] = pxData[pxPos + x];
      }
    }
    function filterSumNone(pxData, pxPos, byteWidth) {
      let sum = 0;
      let length = pxPos + byteWidth;
      for (let i = pxPos; i < length; i++) {
        sum += Math.abs(pxData[i]);
      }
      return sum;
    }
    function filterSub(pxData, pxPos, byteWidth, rawData, rawPos, bpp) {
      for (let x = 0; x < byteWidth; x++) {
        let left = x >= bpp ? pxData[pxPos + x - bpp] : 0;
        let val = pxData[pxPos + x] - left;
        rawData[rawPos + x] = val;
      }
    }
    function filterSumSub(pxData, pxPos, byteWidth, bpp) {
      let sum = 0;
      for (let x = 0; x < byteWidth; x++) {
        let left = x >= bpp ? pxData[pxPos + x - bpp] : 0;
        let val = pxData[pxPos + x] - left;
        sum += Math.abs(val);
      }
      return sum;
    }
    function filterUp(pxData, pxPos, byteWidth, rawData, rawPos) {
      for (let x = 0; x < byteWidth; x++) {
        let up = pxPos > 0 ? pxData[pxPos + x - byteWidth] : 0;
        let val = pxData[pxPos + x] - up;
        rawData[rawPos + x] = val;
      }
    }
    function filterSumUp(pxData, pxPos, byteWidth) {
      let sum = 0;
      let length = pxPos + byteWidth;
      for (let x = pxPos; x < length; x++) {
        let up = pxPos > 0 ? pxData[x - byteWidth] : 0;
        let val = pxData[x] - up;
        sum += Math.abs(val);
      }
      return sum;
    }
    function filterAvg(pxData, pxPos, byteWidth, rawData, rawPos, bpp) {
      for (let x = 0; x < byteWidth; x++) {
        let left = x >= bpp ? pxData[pxPos + x - bpp] : 0;
        let up = pxPos > 0 ? pxData[pxPos + x - byteWidth] : 0;
        let val = pxData[pxPos + x] - (left + up >> 1);
        rawData[rawPos + x] = val;
      }
    }
    function filterSumAvg(pxData, pxPos, byteWidth, bpp) {
      let sum = 0;
      for (let x = 0; x < byteWidth; x++) {
        let left = x >= bpp ? pxData[pxPos + x - bpp] : 0;
        let up = pxPos > 0 ? pxData[pxPos + x - byteWidth] : 0;
        let val = pxData[pxPos + x] - (left + up >> 1);
        sum += Math.abs(val);
      }
      return sum;
    }
    function filterPaeth(pxData, pxPos, byteWidth, rawData, rawPos, bpp) {
      for (let x = 0; x < byteWidth; x++) {
        let left = x >= bpp ? pxData[pxPos + x - bpp] : 0;
        let up = pxPos > 0 ? pxData[pxPos + x - byteWidth] : 0;
        let upleft = pxPos > 0 && x >= bpp ? pxData[pxPos + x - (byteWidth + bpp)] : 0;
        let val = pxData[pxPos + x] - paethPredictor(left, up, upleft);
        rawData[rawPos + x] = val;
      }
    }
    function filterSumPaeth(pxData, pxPos, byteWidth, bpp) {
      let sum = 0;
      for (let x = 0; x < byteWidth; x++) {
        let left = x >= bpp ? pxData[pxPos + x - bpp] : 0;
        let up = pxPos > 0 ? pxData[pxPos + x - byteWidth] : 0;
        let upleft = pxPos > 0 && x >= bpp ? pxData[pxPos + x - (byteWidth + bpp)] : 0;
        let val = pxData[pxPos + x] - paethPredictor(left, up, upleft);
        sum += Math.abs(val);
      }
      return sum;
    }
    var filters = {
      0: filterNone,
      1: filterSub,
      2: filterUp,
      3: filterAvg,
      4: filterPaeth
    };
    var filterSums = {
      0: filterSumNone,
      1: filterSumSub,
      2: filterSumUp,
      3: filterSumAvg,
      4: filterSumPaeth
    };
    module.exports = function(pxData, width, height, options, bpp) {
      let filterTypes;
      if (!("filterType" in options) || options.filterType === -1) {
        filterTypes = [0, 1, 2, 3, 4];
      } else if (typeof options.filterType === "number") {
        filterTypes = [options.filterType];
      } else {
        throw new Error("unrecognised filter types");
      }
      if (options.bitDepth === 16) {
        bpp *= 2;
      }
      let byteWidth = width * bpp;
      let rawPos = 0;
      let pxPos = 0;
      let rawData = Buffer.alloc((byteWidth + 1) * height);
      let sel = filterTypes[0];
      for (let y = 0; y < height; y++) {
        if (filterTypes.length > 1) {
          let min = Infinity;
          for (let i = 0; i < filterTypes.length; i++) {
            let sum = filterSums[filterTypes[i]](pxData, pxPos, byteWidth, bpp);
            if (sum < min) {
              sel = filterTypes[i];
              min = sum;
            }
          }
        }
        rawData[rawPos] = sel;
        rawPos++;
        filters[sel](pxData, pxPos, byteWidth, rawData, rawPos, bpp);
        rawPos += byteWidth;
        pxPos += byteWidth;
      }
      return rawData;
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/packer.js
var require_packer = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/packer.js"(exports, module) {
    "use strict";
    var constants = require_constants();
    var CrcStream = require_crc();
    var bitPacker = require_bitpacker();
    var filter = require_filter_pack();
    var zlib = __require("zlib");
    var Packer = module.exports = function(options) {
      this._options = options;
      options.deflateChunkSize = options.deflateChunkSize || 32 * 1024;
      options.deflateLevel = options.deflateLevel != null ? options.deflateLevel : 9;
      options.deflateStrategy = options.deflateStrategy != null ? options.deflateStrategy : 3;
      options.inputHasAlpha = options.inputHasAlpha != null ? options.inputHasAlpha : true;
      options.deflateFactory = options.deflateFactory || zlib.createDeflate;
      options.bitDepth = options.bitDepth || 8;
      options.colorType = typeof options.colorType === "number" ? options.colorType : constants.COLORTYPE_COLOR_ALPHA;
      options.inputColorType = typeof options.inputColorType === "number" ? options.inputColorType : constants.COLORTYPE_COLOR_ALPHA;
      if ([
        constants.COLORTYPE_GRAYSCALE,
        constants.COLORTYPE_COLOR,
        constants.COLORTYPE_COLOR_ALPHA,
        constants.COLORTYPE_ALPHA
      ].indexOf(options.colorType) === -1) {
        throw new Error(
          "option color type:" + options.colorType + " is not supported at present"
        );
      }
      if ([
        constants.COLORTYPE_GRAYSCALE,
        constants.COLORTYPE_COLOR,
        constants.COLORTYPE_COLOR_ALPHA,
        constants.COLORTYPE_ALPHA
      ].indexOf(options.inputColorType) === -1) {
        throw new Error(
          "option input color type:" + options.inputColorType + " is not supported at present"
        );
      }
      if (options.bitDepth !== 8 && options.bitDepth !== 16) {
        throw new Error(
          "option bit depth:" + options.bitDepth + " is not supported at present"
        );
      }
    };
    Packer.prototype.getDeflateOptions = function() {
      return {
        chunkSize: this._options.deflateChunkSize,
        level: this._options.deflateLevel,
        strategy: this._options.deflateStrategy
      };
    };
    Packer.prototype.createDeflate = function() {
      return this._options.deflateFactory(this.getDeflateOptions());
    };
    Packer.prototype.filterData = function(data, width, height) {
      let packedData = bitPacker(data, width, height, this._options);
      let bpp = constants.COLORTYPE_TO_BPP_MAP[this._options.colorType];
      let filteredData = filter(packedData, width, height, this._options, bpp);
      return filteredData;
    };
    Packer.prototype._packChunk = function(type, data) {
      let len = data ? data.length : 0;
      let buf = Buffer.alloc(len + 12);
      buf.writeUInt32BE(len, 0);
      buf.writeUInt32BE(type, 4);
      if (data) {
        data.copy(buf, 8);
      }
      buf.writeInt32BE(
        CrcStream.crc32(buf.slice(4, buf.length - 4)),
        buf.length - 4
      );
      return buf;
    };
    Packer.prototype.packGAMA = function(gamma) {
      let buf = Buffer.alloc(4);
      buf.writeUInt32BE(Math.floor(gamma * constants.GAMMA_DIVISION), 0);
      return this._packChunk(constants.TYPE_gAMA, buf);
    };
    Packer.prototype.packIHDR = function(width, height) {
      let buf = Buffer.alloc(13);
      buf.writeUInt32BE(width, 0);
      buf.writeUInt32BE(height, 4);
      buf[8] = this._options.bitDepth;
      buf[9] = this._options.colorType;
      buf[10] = 0;
      buf[11] = 0;
      buf[12] = 0;
      return this._packChunk(constants.TYPE_IHDR, buf);
    };
    Packer.prototype.packIDAT = function(data) {
      return this._packChunk(constants.TYPE_IDAT, data);
    };
    Packer.prototype.packIEND = function() {
      return this._packChunk(constants.TYPE_IEND, null);
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/packer-async.js
var require_packer_async = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/packer-async.js"(exports, module) {
    "use strict";
    var util = __require("util");
    var Stream = __require("stream");
    var constants = require_constants();
    var Packer = require_packer();
    var PackerAsync = module.exports = function(opt) {
      Stream.call(this);
      let options = opt || {};
      this._packer = new Packer(options);
      this._deflate = this._packer.createDeflate();
      this.readable = true;
    };
    util.inherits(PackerAsync, Stream);
    PackerAsync.prototype.pack = function(data, width, height, gamma) {
      this.emit("data", Buffer.from(constants.PNG_SIGNATURE));
      this.emit("data", this._packer.packIHDR(width, height));
      if (gamma) {
        this.emit("data", this._packer.packGAMA(gamma));
      }
      let filteredData = this._packer.filterData(data, width, height);
      this._deflate.on("error", this.emit.bind(this, "error"));
      this._deflate.on(
        "data",
        function(compressedData) {
          this.emit("data", this._packer.packIDAT(compressedData));
        }.bind(this)
      );
      this._deflate.on(
        "end",
        function() {
          this.emit("data", this._packer.packIEND());
          this.emit("end");
        }.bind(this)
      );
      this._deflate.end(filteredData);
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/sync-inflate.js
var require_sync_inflate = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/sync-inflate.js"(exports, module) {
    "use strict";
    var assert = __require("assert").ok;
    var zlib = __require("zlib");
    var util = __require("util");
    var kMaxLength = __require("buffer").kMaxLength;
    function Inflate(opts) {
      if (!(this instanceof Inflate)) {
        return new Inflate(opts);
      }
      if (opts && opts.chunkSize < zlib.Z_MIN_CHUNK) {
        opts.chunkSize = zlib.Z_MIN_CHUNK;
      }
      zlib.Inflate.call(this, opts);
      this._offset = this._offset === void 0 ? this._outOffset : this._offset;
      this._buffer = this._buffer || this._outBuffer;
      if (opts && opts.maxLength != null) {
        this._maxLength = opts.maxLength;
      }
    }
    function createInflate(opts) {
      return new Inflate(opts);
    }
    function _close(engine, callback) {
      if (callback) {
        process.nextTick(callback);
      }
      if (!engine._handle) {
        return;
      }
      engine._handle.close();
      engine._handle = null;
    }
    Inflate.prototype._processChunk = function(chunk, flushFlag, asyncCb) {
      if (typeof asyncCb === "function") {
        return zlib.Inflate._processChunk.call(this, chunk, flushFlag, asyncCb);
      }
      let self = this;
      let availInBefore = chunk && chunk.length;
      let availOutBefore = this._chunkSize - this._offset;
      let leftToInflate = this._maxLength;
      let inOff = 0;
      let buffers = [];
      let nread = 0;
      let error;
      this.on("error", function(err) {
        error = err;
      });
      function handleChunk(availInAfter, availOutAfter) {
        if (self._hadError) {
          return;
        }
        let have = availOutBefore - availOutAfter;
        assert(have >= 0, "have should not go down");
        if (have > 0) {
          let out = self._buffer.slice(self._offset, self._offset + have);
          self._offset += have;
          if (out.length > leftToInflate) {
            out = out.slice(0, leftToInflate);
          }
          buffers.push(out);
          nread += out.length;
          leftToInflate -= out.length;
          if (leftToInflate === 0) {
            return false;
          }
        }
        if (availOutAfter === 0 || self._offset >= self._chunkSize) {
          availOutBefore = self._chunkSize;
          self._offset = 0;
          self._buffer = Buffer.allocUnsafe(self._chunkSize);
        }
        if (availOutAfter === 0) {
          inOff += availInBefore - availInAfter;
          availInBefore = availInAfter;
          return true;
        }
        return false;
      }
      assert(this._handle, "zlib binding closed");
      let res;
      do {
        res = this._handle.writeSync(
          flushFlag,
          chunk,
          // in
          inOff,
          // in_off
          availInBefore,
          // in_len
          this._buffer,
          // out
          this._offset,
          //out_off
          availOutBefore
        );
        res = res || this._writeState;
      } while (!this._hadError && handleChunk(res[0], res[1]));
      if (this._hadError) {
        throw error;
      }
      if (nread >= kMaxLength) {
        _close(this);
        throw new RangeError(
          "Cannot create final Buffer. It would be larger than 0x" + kMaxLength.toString(16) + " bytes"
        );
      }
      let buf = Buffer.concat(buffers, nread);
      _close(this);
      return buf;
    };
    util.inherits(Inflate, zlib.Inflate);
    function zlibBufferSync(engine, buffer) {
      if (typeof buffer === "string") {
        buffer = Buffer.from(buffer);
      }
      if (!(buffer instanceof Buffer)) {
        throw new TypeError("Not a string or buffer");
      }
      let flushFlag = engine._finishFlushFlag;
      if (flushFlag == null) {
        flushFlag = zlib.Z_FINISH;
      }
      return engine._processChunk(buffer, flushFlag);
    }
    function inflateSync(buffer, opts) {
      return zlibBufferSync(new Inflate(opts), buffer);
    }
    module.exports = exports = inflateSync;
    exports.Inflate = Inflate;
    exports.createInflate = createInflate;
    exports.inflateSync = inflateSync;
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/sync-reader.js
var require_sync_reader = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/sync-reader.js"(exports, module) {
    "use strict";
    var SyncReader = module.exports = function(buffer) {
      this._buffer = buffer;
      this._reads = [];
    };
    SyncReader.prototype.read = function(length, callback) {
      this._reads.push({
        length: Math.abs(length),
        // if length < 0 then at most this length
        allowLess: length < 0,
        func: callback
      });
    };
    SyncReader.prototype.process = function() {
      while (this._reads.length > 0 && this._buffer.length) {
        let read = this._reads[0];
        if (this._buffer.length && (this._buffer.length >= read.length || read.allowLess)) {
          this._reads.shift();
          let buf = this._buffer;
          this._buffer = buf.slice(read.length);
          read.func.call(this, buf.slice(0, read.length));
        } else {
          break;
        }
      }
      if (this._reads.length > 0) {
        return new Error("There are some read requests waitng on finished stream");
      }
      if (this._buffer.length > 0) {
        return new Error("unrecognised content at end of stream");
      }
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/filter-parse-sync.js
var require_filter_parse_sync = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/filter-parse-sync.js"(exports) {
    "use strict";
    var SyncReader = require_sync_reader();
    var Filter = require_filter_parse();
    exports.process = function(inBuffer, bitmapInfo) {
      let outBuffers = [];
      let reader = new SyncReader(inBuffer);
      let filter = new Filter(bitmapInfo, {
        read: reader.read.bind(reader),
        write: function(bufferPart) {
          outBuffers.push(bufferPart);
        },
        complete: function() {
        }
      });
      filter.start();
      reader.process();
      return Buffer.concat(outBuffers);
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/parser-sync.js
var require_parser_sync = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/parser-sync.js"(exports, module) {
    "use strict";
    var hasSyncZlib = true;
    var zlib = __require("zlib");
    var inflateSync = require_sync_inflate();
    if (!zlib.deflateSync) {
      hasSyncZlib = false;
    }
    var SyncReader = require_sync_reader();
    var FilterSync = require_filter_parse_sync();
    var Parser = require_parser();
    var bitmapper = require_bitmapper();
    var formatNormaliser = require_format_normaliser();
    module.exports = function(buffer, options) {
      if (!hasSyncZlib) {
        throw new Error(
          "To use the sync capability of this library in old node versions, please pin pngjs to v2.3.0"
        );
      }
      let err;
      function handleError(_err_) {
        err = _err_;
      }
      let metaData;
      function handleMetaData(_metaData_) {
        metaData = _metaData_;
      }
      function handleTransColor(transColor) {
        metaData.transColor = transColor;
      }
      function handlePalette(palette) {
        metaData.palette = palette;
      }
      function handleSimpleTransparency() {
        metaData.alpha = true;
      }
      let gamma;
      function handleGamma(_gamma_) {
        gamma = _gamma_;
      }
      let inflateDataList = [];
      function handleInflateData(inflatedData2) {
        inflateDataList.push(inflatedData2);
      }
      let reader = new SyncReader(buffer);
      let parser = new Parser(options, {
        read: reader.read.bind(reader),
        error: handleError,
        metadata: handleMetaData,
        gamma: handleGamma,
        palette: handlePalette,
        transColor: handleTransColor,
        inflateData: handleInflateData,
        simpleTransparency: handleSimpleTransparency
      });
      parser.start();
      reader.process();
      if (err) {
        throw err;
      }
      let inflateData = Buffer.concat(inflateDataList);
      inflateDataList.length = 0;
      let inflatedData;
      if (metaData.interlace) {
        inflatedData = zlib.inflateSync(inflateData);
      } else {
        let rowSize = (metaData.width * metaData.bpp * metaData.depth + 7 >> 3) + 1;
        let imageSize = rowSize * metaData.height;
        inflatedData = inflateSync(inflateData, {
          chunkSize: imageSize,
          maxLength: imageSize
        });
      }
      inflateData = null;
      if (!inflatedData || !inflatedData.length) {
        throw new Error("bad png - invalid inflate data response");
      }
      let unfilteredData = FilterSync.process(inflatedData, metaData);
      inflateData = null;
      let bitmapData = bitmapper.dataToBitMap(unfilteredData, metaData);
      unfilteredData = null;
      let normalisedBitmapData = formatNormaliser(bitmapData, metaData);
      metaData.data = normalisedBitmapData;
      metaData.gamma = gamma || 0;
      return metaData;
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/packer-sync.js
var require_packer_sync = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/packer-sync.js"(exports, module) {
    "use strict";
    var hasSyncZlib = true;
    var zlib = __require("zlib");
    if (!zlib.deflateSync) {
      hasSyncZlib = false;
    }
    var constants = require_constants();
    var Packer = require_packer();
    module.exports = function(metaData, opt) {
      if (!hasSyncZlib) {
        throw new Error(
          "To use the sync capability of this library in old node versions, please pin pngjs to v2.3.0"
        );
      }
      let options = opt || {};
      let packer = new Packer(options);
      let chunks = [];
      chunks.push(Buffer.from(constants.PNG_SIGNATURE));
      chunks.push(packer.packIHDR(metaData.width, metaData.height));
      if (metaData.gamma) {
        chunks.push(packer.packGAMA(metaData.gamma));
      }
      let filteredData = packer.filterData(
        metaData.data,
        metaData.width,
        metaData.height
      );
      let compressedData = zlib.deflateSync(
        filteredData,
        packer.getDeflateOptions()
      );
      filteredData = null;
      if (!compressedData || !compressedData.length) {
        throw new Error("bad png - invalid compressed data response");
      }
      chunks.push(packer.packIDAT(compressedData));
      chunks.push(packer.packIEND());
      return Buffer.concat(chunks);
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/png-sync.js
var require_png_sync = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/png-sync.js"(exports) {
    "use strict";
    var parse = require_parser_sync();
    var pack = require_packer_sync();
    exports.read = function(buffer, options) {
      return parse(buffer, options || {});
    };
    exports.write = function(png, options) {
      return pack(png, options);
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/png.js
var require_png = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/pngjs/lib/png.js"(exports) {
    "use strict";
    var util = __require("util");
    var Stream = __require("stream");
    var Parser = require_parser_async();
    var Packer = require_packer_async();
    var PNGSync = require_png_sync();
    var PNG = exports.PNG = function(options) {
      Stream.call(this);
      options = options || {};
      this.width = options.width | 0;
      this.height = options.height | 0;
      this.data = this.width > 0 && this.height > 0 ? Buffer.alloc(4 * this.width * this.height) : null;
      if (options.fill && this.data) {
        this.data.fill(0);
      }
      this.gamma = 0;
      this.readable = this.writable = true;
      this._parser = new Parser(options);
      this._parser.on("error", this.emit.bind(this, "error"));
      this._parser.on("close", this._handleClose.bind(this));
      this._parser.on("metadata", this._metadata.bind(this));
      this._parser.on("gamma", this._gamma.bind(this));
      this._parser.on(
        "parsed",
        function(data) {
          this.data = data;
          this.emit("parsed", data);
        }.bind(this)
      );
      this._packer = new Packer(options);
      this._packer.on("data", this.emit.bind(this, "data"));
      this._packer.on("end", this.emit.bind(this, "end"));
      this._parser.on("close", this._handleClose.bind(this));
      this._packer.on("error", this.emit.bind(this, "error"));
    };
    util.inherits(PNG, Stream);
    PNG.sync = PNGSync;
    PNG.prototype.pack = function() {
      if (!this.data || !this.data.length) {
        this.emit("error", "No data provided");
        return this;
      }
      process.nextTick(
        function() {
          this._packer.pack(this.data, this.width, this.height, this.gamma);
        }.bind(this)
      );
      return this;
    };
    PNG.prototype.parse = function(data, callback) {
      if (callback) {
        let onParsed, onError;
        onParsed = function(parsedData) {
          this.removeListener("error", onError);
          this.data = parsedData;
          callback(null, this);
        }.bind(this);
        onError = function(err) {
          this.removeListener("parsed", onParsed);
          callback(err, null);
        }.bind(this);
        this.once("parsed", onParsed);
        this.once("error", onError);
      }
      this.end(data);
      return this;
    };
    PNG.prototype.write = function(data) {
      this._parser.write(data);
      return true;
    };
    PNG.prototype.end = function(data) {
      this._parser.end(data);
    };
    PNG.prototype._metadata = function(metadata) {
      this.width = metadata.width;
      this.height = metadata.height;
      this.emit("metadata", metadata);
    };
    PNG.prototype._gamma = function(gamma) {
      this.gamma = gamma;
    };
    PNG.prototype._handleClose = function() {
      if (!this._parser.writable && !this._packer.readable) {
        this.emit("close");
      }
    };
    PNG.bitblt = function(src, dst, srcX, srcY, width, height, deltaX, deltaY) {
      srcX |= 0;
      srcY |= 0;
      width |= 0;
      height |= 0;
      deltaX |= 0;
      deltaY |= 0;
      if (srcX > src.width || srcY > src.height || srcX + width > src.width || srcY + height > src.height) {
        throw new Error("bitblt reading outside image");
      }
      if (deltaX > dst.width || deltaY > dst.height || deltaX + width > dst.width || deltaY + height > dst.height) {
        throw new Error("bitblt writing outside image");
      }
      for (let y = 0; y < height; y++) {
        src.data.copy(
          dst.data,
          (deltaY + y) * dst.width + deltaX << 2,
          (srcY + y) * src.width + srcX << 2,
          (srcY + y) * src.width + srcX + width << 2
        );
      }
    };
    PNG.prototype.bitblt = function(dst, srcX, srcY, width, height, deltaX, deltaY) {
      PNG.bitblt(this, dst, srcX, srcY, width, height, deltaX, deltaY);
      return this;
    };
    PNG.adjustGamma = function(src) {
      if (src.gamma) {
        for (let y = 0; y < src.height; y++) {
          for (let x = 0; x < src.width; x++) {
            let idx = src.width * y + x << 2;
            for (let i = 0; i < 3; i++) {
              let sample = src.data[idx + i] / 255;
              sample = Math.pow(sample, 1 / 2.2 / src.gamma);
              src.data[idx + i] = Math.round(sample * 255);
            }
          }
        }
        src.gamma = 0;
      }
    };
    PNG.prototype.adjustGamma = function() {
      PNG.adjustGamma(this);
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/utils.js
var require_utils2 = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/utils.js"(exports) {
    function hex2rgba(hex) {
      if (typeof hex === "number") {
        hex = hex.toString();
      }
      if (typeof hex !== "string") {
        throw new Error("Color should be defined as hex string");
      }
      let hexCode = hex.slice().replace("#", "").split("");
      if (hexCode.length < 3 || hexCode.length === 5 || hexCode.length > 8) {
        throw new Error("Invalid hex color: " + hex);
      }
      if (hexCode.length === 3 || hexCode.length === 4) {
        hexCode = Array.prototype.concat.apply([], hexCode.map(function(c) {
          return [c, c];
        }));
      }
      if (hexCode.length === 6) hexCode.push("F", "F");
      const hexValue = parseInt(hexCode.join(""), 16);
      return {
        r: hexValue >> 24 & 255,
        g: hexValue >> 16 & 255,
        b: hexValue >> 8 & 255,
        a: hexValue & 255,
        hex: "#" + hexCode.slice(0, 6).join("")
      };
    }
    exports.getOptions = function getOptions(options) {
      if (!options) options = {};
      if (!options.color) options.color = {};
      const margin = typeof options.margin === "undefined" || options.margin === null || options.margin < 0 ? 4 : options.margin;
      const width = options.width && options.width >= 21 ? options.width : void 0;
      const scale = options.scale || 4;
      return {
        width,
        scale: width ? 4 : scale,
        margin,
        color: {
          dark: hex2rgba(options.color.dark || "#000000ff"),
          light: hex2rgba(options.color.light || "#ffffffff")
        },
        type: options.type,
        rendererOpts: options.rendererOpts || {}
      };
    };
    exports.getScale = function getScale(qrSize, opts) {
      return opts.width && opts.width >= qrSize + opts.margin * 2 ? opts.width / (qrSize + opts.margin * 2) : opts.scale;
    };
    exports.getImageWidth = function getImageWidth(qrSize, opts) {
      const scale = exports.getScale(qrSize, opts);
      return Math.floor((qrSize + opts.margin * 2) * scale);
    };
    exports.qrToImageData = function qrToImageData(imgData, qr, opts) {
      const size = qr.modules.size;
      const data = qr.modules.data;
      const scale = exports.getScale(size, opts);
      const symbolSize = Math.floor((size + opts.margin * 2) * scale);
      const scaledMargin = opts.margin * scale;
      const palette = [opts.color.light, opts.color.dark];
      for (let i = 0; i < symbolSize; i++) {
        for (let j = 0; j < symbolSize; j++) {
          let posDst = (i * symbolSize + j) * 4;
          let pxColor = opts.color.light;
          if (i >= scaledMargin && j >= scaledMargin && i < symbolSize - scaledMargin && j < symbolSize - scaledMargin) {
            const iSrc = Math.floor((i - scaledMargin) / scale);
            const jSrc = Math.floor((j - scaledMargin) / scale);
            pxColor = palette[data[iSrc * size + jSrc] ? 1 : 0];
          }
          imgData[posDst++] = pxColor.r;
          imgData[posDst++] = pxColor.g;
          imgData[posDst++] = pxColor.b;
          imgData[posDst] = pxColor.a;
        }
      }
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/png.js
var require_png2 = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/png.js"(exports) {
    var fs2 = __require("fs");
    var PNG = require_png().PNG;
    var Utils = require_utils2();
    exports.render = function render(qrData, options) {
      const opts = Utils.getOptions(options);
      const pngOpts = opts.rendererOpts;
      const size = Utils.getImageWidth(qrData.modules.size, opts);
      pngOpts.width = size;
      pngOpts.height = size;
      const pngImage = new PNG(pngOpts);
      Utils.qrToImageData(pngImage.data, qrData, opts);
      return pngImage;
    };
    exports.renderToDataURL = function renderToDataURL(qrData, options, cb) {
      if (typeof cb === "undefined") {
        cb = options;
        options = void 0;
      }
      exports.renderToBuffer(qrData, options, function(err, output) {
        if (err) cb(err);
        let url = "data:image/png;base64,";
        url += output.toString("base64");
        cb(null, url);
      });
    };
    exports.renderToBuffer = function renderToBuffer(qrData, options, cb) {
      if (typeof cb === "undefined") {
        cb = options;
        options = void 0;
      }
      const png = exports.render(qrData, options);
      const buffer = [];
      png.on("error", cb);
      png.on("data", function(data) {
        buffer.push(data);
      });
      png.on("end", function() {
        cb(null, Buffer.concat(buffer));
      });
      png.pack();
    };
    exports.renderToFile = function renderToFile(path3, qrData, options, cb) {
      if (typeof cb === "undefined") {
        cb = options;
        options = void 0;
      }
      let called = false;
      const done = (...args) => {
        if (called) return;
        called = true;
        cb.apply(null, args);
      };
      const stream = fs2.createWriteStream(path3);
      stream.on("error", done);
      stream.on("close", done);
      exports.renderToFileStream(stream, qrData, options);
    };
    exports.renderToFileStream = function renderToFileStream(stream, qrData, options) {
      const png = exports.render(qrData, options);
      png.pack().pipe(stream);
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/utf8.js
var require_utf8 = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/utf8.js"(exports) {
    var Utils = require_utils2();
    var BLOCK_CHAR = {
      WW: " ",
      WB: "\u2584",
      BB: "\u2588",
      BW: "\u2580"
    };
    var INVERTED_BLOCK_CHAR = {
      BB: " ",
      BW: "\u2584",
      WW: "\u2588",
      WB: "\u2580"
    };
    function getBlockChar(top, bottom, blocks) {
      if (top && bottom) return blocks.BB;
      if (top && !bottom) return blocks.BW;
      if (!top && bottom) return blocks.WB;
      return blocks.WW;
    }
    exports.render = function(qrData, options, cb) {
      const opts = Utils.getOptions(options);
      let blocks = BLOCK_CHAR;
      if (opts.color.dark.hex === "#ffffff" || opts.color.light.hex === "#000000") {
        blocks = INVERTED_BLOCK_CHAR;
      }
      const size = qrData.modules.size;
      const data = qrData.modules.data;
      let output = "";
      let hMargin = Array(size + opts.margin * 2 + 1).join(blocks.WW);
      hMargin = Array(opts.margin / 2 + 1).join(hMargin + "\n");
      const vMargin = Array(opts.margin + 1).join(blocks.WW);
      output += hMargin;
      for (let i = 0; i < size; i += 2) {
        output += vMargin;
        for (let j = 0; j < size; j++) {
          const topModule = data[i * size + j];
          const bottomModule = data[(i + 1) * size + j];
          output += getBlockChar(topModule, bottomModule, blocks);
        }
        output += vMargin + "\n";
      }
      output += hMargin.slice(0, -1);
      if (typeof cb === "function") {
        cb(null, output);
      }
      return output;
    };
    exports.renderToFile = function renderToFile(path3, qrData, options, cb) {
      if (typeof cb === "undefined") {
        cb = options;
        options = void 0;
      }
      const fs2 = __require("fs");
      const utf8 = exports.render(qrData, options);
      fs2.writeFile(path3, utf8, cb);
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/terminal/terminal.js
var require_terminal = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/terminal/terminal.js"(exports) {
    exports.render = function(qrData, options, cb) {
      const size = qrData.modules.size;
      const data = qrData.modules.data;
      const black = "\x1B[40m  \x1B[0m";
      const white = "\x1B[47m  \x1B[0m";
      let output = "";
      const hMargin = Array(size + 3).join(white);
      const vMargin = Array(2).join(white);
      output += hMargin + "\n";
      for (let i = 0; i < size; ++i) {
        output += white;
        for (let j = 0; j < size; j++) {
          output += data[i * size + j] ? black : white;
        }
        output += vMargin + "\n";
      }
      output += hMargin + "\n";
      if (typeof cb === "function") {
        cb(null, output);
      }
      return output;
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/terminal/terminal-small.js
var require_terminal_small = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/terminal/terminal-small.js"(exports) {
    var backgroundWhite = "\x1B[47m";
    var backgroundBlack = "\x1B[40m";
    var foregroundWhite = "\x1B[37m";
    var foregroundBlack = "\x1B[30m";
    var reset = "\x1B[0m";
    var lineSetupNormal = backgroundWhite + foregroundBlack;
    var lineSetupInverse = backgroundBlack + foregroundWhite;
    var createPalette = function(lineSetup, foregroundWhite2, foregroundBlack2) {
      return {
        // 1 ... white, 2 ... black, 0 ... transparent (default)
        "00": reset + " " + lineSetup,
        "01": reset + foregroundWhite2 + "\u2584" + lineSetup,
        "02": reset + foregroundBlack2 + "\u2584" + lineSetup,
        10: reset + foregroundWhite2 + "\u2580" + lineSetup,
        11: " ",
        12: "\u2584",
        20: reset + foregroundBlack2 + "\u2580" + lineSetup,
        21: "\u2580",
        22: "\u2588"
      };
    };
    var mkCodePixel = function(modules, size, x, y) {
      const sizePlus = size + 1;
      if (x >= sizePlus || y >= sizePlus || y < -1 || x < -1) return "0";
      if (x >= size || y >= size || y < 0 || x < 0) return "1";
      const idx = y * size + x;
      return modules[idx] ? "2" : "1";
    };
    var mkCode = function(modules, size, x, y) {
      return mkCodePixel(modules, size, x, y) + mkCodePixel(modules, size, x, y + 1);
    };
    exports.render = function(qrData, options, cb) {
      const size = qrData.modules.size;
      const data = qrData.modules.data;
      const inverse = !!(options && options.inverse);
      const lineSetup = options && options.inverse ? lineSetupInverse : lineSetupNormal;
      const white = inverse ? foregroundBlack : foregroundWhite;
      const black = inverse ? foregroundWhite : foregroundBlack;
      const palette = createPalette(lineSetup, white, black);
      const newLine = reset + "\n" + lineSetup;
      let output = lineSetup;
      for (let y = -1; y < size + 1; y += 2) {
        for (let x = -1; x < size; x++) {
          output += palette[mkCode(data, size, x, y)];
        }
        output += palette[mkCode(data, size, size, y)] + newLine;
      }
      output += reset;
      if (typeof cb === "function") {
        cb(null, output);
      }
      return output;
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/terminal.js
var require_terminal2 = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/terminal.js"(exports) {
    var big = require_terminal();
    var small = require_terminal_small();
    exports.render = function(qrData, options, cb) {
      if (options && options.small) {
        return small.render(qrData, options, cb);
      }
      return big.render(qrData, options, cb);
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/svg-tag.js
var require_svg_tag = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/svg-tag.js"(exports) {
    var Utils = require_utils2();
    function getColorAttrib(color, attrib) {
      const alpha = color.a / 255;
      const str = attrib + '="' + color.hex + '"';
      return alpha < 1 ? str + " " + attrib + '-opacity="' + alpha.toFixed(2).slice(1) + '"' : str;
    }
    function svgCmd(cmd, x, y) {
      let str = cmd + x;
      if (typeof y !== "undefined") str += " " + y;
      return str;
    }
    function qrToPath(data, size, margin) {
      let path3 = "";
      let moveBy = 0;
      let newRow = false;
      let lineLength = 0;
      for (let i = 0; i < data.length; i++) {
        const col = Math.floor(i % size);
        const row = Math.floor(i / size);
        if (!col && !newRow) newRow = true;
        if (data[i]) {
          lineLength++;
          if (!(i > 0 && col > 0 && data[i - 1])) {
            path3 += newRow ? svgCmd("M", col + margin, 0.5 + row + margin) : svgCmd("m", moveBy, 0);
            moveBy = 0;
            newRow = false;
          }
          if (!(col + 1 < size && data[i + 1])) {
            path3 += svgCmd("h", lineLength);
            lineLength = 0;
          }
        } else {
          moveBy++;
        }
      }
      return path3;
    }
    exports.render = function render(qrData, options, cb) {
      const opts = Utils.getOptions(options);
      const size = qrData.modules.size;
      const data = qrData.modules.data;
      const qrcodesize = size + opts.margin * 2;
      const bg = !opts.color.light.a ? "" : "<path " + getColorAttrib(opts.color.light, "fill") + ' d="M0 0h' + qrcodesize + "v" + qrcodesize + 'H0z"/>';
      const path3 = "<path " + getColorAttrib(opts.color.dark, "stroke") + ' d="' + qrToPath(data, size, opts.margin) + '"/>';
      const viewBox = 'viewBox="0 0 ' + qrcodesize + " " + qrcodesize + '"';
      const width = !opts.width ? "" : 'width="' + opts.width + '" height="' + opts.width + '" ';
      const svgTag = '<svg xmlns="http://www.w3.org/2000/svg" ' + width + viewBox + ' shape-rendering="crispEdges">' + bg + path3 + "</svg>\n";
      if (typeof cb === "function") {
        cb(null, svgTag);
      }
      return svgTag;
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/svg.js
var require_svg = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/svg.js"(exports) {
    var svgTagRenderer = require_svg_tag();
    exports.render = svgTagRenderer.render;
    exports.renderToFile = function renderToFile(path3, qrData, options, cb) {
      if (typeof cb === "undefined") {
        cb = options;
        options = void 0;
      }
      const fs2 = __require("fs");
      const svgTag = exports.render(qrData, options);
      const xmlStr = '<?xml version="1.0" encoding="utf-8"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">' + svgTag;
      fs2.writeFile(path3, xmlStr, cb);
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/canvas.js
var require_canvas = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/renderer/canvas.js"(exports) {
    var Utils = require_utils2();
    function clearCanvas(ctx, canvas, size) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      if (!canvas.style) canvas.style = {};
      canvas.height = size;
      canvas.width = size;
      canvas.style.height = size + "px";
      canvas.style.width = size + "px";
    }
    function getCanvasElement() {
      try {
        return document.createElement("canvas");
      } catch (e) {
        throw new Error("You need to specify a canvas element");
      }
    }
    exports.render = function render(qrData, canvas, options) {
      let opts = options;
      let canvasEl = canvas;
      if (typeof opts === "undefined" && (!canvas || !canvas.getContext)) {
        opts = canvas;
        canvas = void 0;
      }
      if (!canvas) {
        canvasEl = getCanvasElement();
      }
      opts = Utils.getOptions(opts);
      const size = Utils.getImageWidth(qrData.modules.size, opts);
      const ctx = canvasEl.getContext("2d");
      const image = ctx.createImageData(size, size);
      Utils.qrToImageData(image.data, qrData, opts);
      clearCanvas(ctx, canvasEl, size);
      ctx.putImageData(image, 0, 0);
      return canvasEl;
    };
    exports.renderToDataURL = function renderToDataURL(qrData, canvas, options) {
      let opts = options;
      if (typeof opts === "undefined" && (!canvas || !canvas.getContext)) {
        opts = canvas;
        canvas = void 0;
      }
      if (!opts) opts = {};
      const canvasEl = exports.render(qrData, canvas, opts);
      const type = opts.type || "image/png";
      const rendererOpts = opts.rendererOpts || {};
      return canvasEl.toDataURL(type, rendererOpts.quality);
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/browser.js
var require_browser = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/browser.js"(exports) {
    var canPromise = require_can_promise();
    var QRCode2 = require_qrcode();
    var CanvasRenderer = require_canvas();
    var SvgRenderer = require_svg_tag();
    function renderCanvas(renderFunc, canvas, text, opts, cb) {
      const args = [].slice.call(arguments, 1);
      const argsNum = args.length;
      const isLastArgCb = typeof args[argsNum - 1] === "function";
      if (!isLastArgCb && !canPromise()) {
        throw new Error("Callback required as last argument");
      }
      if (isLastArgCb) {
        if (argsNum < 2) {
          throw new Error("Too few arguments provided");
        }
        if (argsNum === 2) {
          cb = text;
          text = canvas;
          canvas = opts = void 0;
        } else if (argsNum === 3) {
          if (canvas.getContext && typeof cb === "undefined") {
            cb = opts;
            opts = void 0;
          } else {
            cb = opts;
            opts = text;
            text = canvas;
            canvas = void 0;
          }
        }
      } else {
        if (argsNum < 1) {
          throw new Error("Too few arguments provided");
        }
        if (argsNum === 1) {
          text = canvas;
          canvas = opts = void 0;
        } else if (argsNum === 2 && !canvas.getContext) {
          opts = text;
          text = canvas;
          canvas = void 0;
        }
        return new Promise(function(resolve5, reject) {
          try {
            const data = QRCode2.create(text, opts);
            resolve5(renderFunc(data, canvas, opts));
          } catch (e) {
            reject(e);
          }
        });
      }
      try {
        const data = QRCode2.create(text, opts);
        cb(null, renderFunc(data, canvas, opts));
      } catch (e) {
        cb(e);
      }
    }
    exports.create = QRCode2.create;
    exports.toCanvas = renderCanvas.bind(null, CanvasRenderer.render);
    exports.toDataURL = renderCanvas.bind(null, CanvasRenderer.renderToDataURL);
    exports.toString = renderCanvas.bind(null, function(data, _, opts) {
      return SvgRenderer.render(data, opts);
    });
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/server.js
var require_server = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/server.js"(exports) {
    var canPromise = require_can_promise();
    var QRCode2 = require_qrcode();
    var PngRenderer = require_png2();
    var Utf8Renderer = require_utf8();
    var TerminalRenderer = require_terminal2();
    var SvgRenderer = require_svg();
    function checkParams(text, opts, cb) {
      if (typeof text === "undefined") {
        throw new Error("String required as first argument");
      }
      if (typeof cb === "undefined") {
        cb = opts;
        opts = {};
      }
      if (typeof cb !== "function") {
        if (!canPromise()) {
          throw new Error("Callback required as last argument");
        } else {
          opts = cb || {};
          cb = null;
        }
      }
      return {
        opts,
        cb
      };
    }
    function getTypeFromFilename(path3) {
      return path3.slice((path3.lastIndexOf(".") - 1 >>> 0) + 2).toLowerCase();
    }
    function getRendererFromType(type) {
      switch (type) {
        case "svg":
          return SvgRenderer;
        case "txt":
        case "utf8":
          return Utf8Renderer;
        case "png":
        case "image/png":
        default:
          return PngRenderer;
      }
    }
    function getStringRendererFromType(type) {
      switch (type) {
        case "svg":
          return SvgRenderer;
        case "terminal":
          return TerminalRenderer;
        case "utf8":
        default:
          return Utf8Renderer;
      }
    }
    function render(renderFunc, text, params) {
      if (!params.cb) {
        return new Promise(function(resolve5, reject) {
          try {
            const data = QRCode2.create(text, params.opts);
            return renderFunc(data, params.opts, function(err, data2) {
              return err ? reject(err) : resolve5(data2);
            });
          } catch (e) {
            reject(e);
          }
        });
      }
      try {
        const data = QRCode2.create(text, params.opts);
        return renderFunc(data, params.opts, params.cb);
      } catch (e) {
        params.cb(e);
      }
    }
    exports.create = QRCode2.create;
    exports.toCanvas = require_browser().toCanvas;
    exports.toString = function toString(text, opts, cb) {
      const params = checkParams(text, opts, cb);
      const type = params.opts ? params.opts.type : void 0;
      const renderer = getStringRendererFromType(type);
      return render(renderer.render, text, params);
    };
    exports.toDataURL = function toDataURL(text, opts, cb) {
      const params = checkParams(text, opts, cb);
      const renderer = getRendererFromType(params.opts.type);
      return render(renderer.renderToDataURL, text, params);
    };
    exports.toBuffer = function toBuffer(text, opts, cb) {
      const params = checkParams(text, opts, cb);
      const renderer = getRendererFromType(params.opts.type);
      return render(renderer.renderToBuffer, text, params);
    };
    exports.toFile = function toFile(path3, text, opts, cb) {
      if (typeof path3 !== "string" || !(typeof text === "string" || typeof text === "object")) {
        throw new Error("Invalid argument");
      }
      if (arguments.length < 3 && !canPromise()) {
        throw new Error("Too few arguments provided");
      }
      const params = checkParams(text, opts, cb);
      const type = params.opts.type || getTypeFromFilename(path3);
      const renderer = getRendererFromType(type);
      const renderToFile = renderer.renderToFile.bind(null, path3);
      return render(renderToFile, text, params);
    };
    exports.toFileStream = function toFileStream(stream, text, opts) {
      if (arguments.length < 2) {
        throw new Error("Too few arguments provided");
      }
      const params = checkParams(text, opts, stream.emit.bind(stream, "error"));
      const renderer = getRendererFromType("png");
      const renderToFileStream = renderer.renderToFileStream.bind(null, stream);
      render(renderToFileStream, text, params);
    };
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/index.js
var require_lib = __commonJS({
  "../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/qrcode/lib/index.js"(exports, module) {
    module.exports = require_server();
  }
});

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/commander/esm.mjs
var import_index = __toESM(require_commander(), 1);
var {
  program,
  createCommand,
  createArgument,
  createOption,
  CommanderError,
  InvalidArgumentError,
  InvalidOptionArgumentError,
  // deprecated old name
  Command,
  Argument,
  Option,
  Help
} = import_index.default;

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/state/config.js
import { homedir as homedir2 } from "node:os";
import { mkdirSync as mkdirSync3 } from "node:fs";
import { resolve as resolve2 } from "node:path";

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/client/transport.js
var HttpTransportError = class extends Error {
  code;
  attempts;
  causeCode;
  retryable = true;
  constructor(code, attempts, causeCode, cause) {
    const suffix = attempts > 1 ? ` after ${attempts} attempts` : "";
    super(`${transportMessage(code)} before a complete HTTP response was received${suffix}`, { cause });
    this.code = code;
    this.attempts = attempts;
    this.causeCode = causeCode;
    this.name = "HttpTransportError";
  }
};
function asTransientTransportError(error, attempts) {
  if (isAbort(error))
    return void 0;
  const causeCode = findCauseCode(error);
  const code = causeCode ? classifyCauseCode(causeCode) : classifyFetchFailure(error);
  return code ? new HttpTransportError(code, attempts, causeCode, error) : void 0;
}
function classifyCauseCode(code) {
  switch (code) {
    case "ECONNRESET":
      return "network_connection_reset";
    case "ETIMEDOUT":
    case "UND_ERR_CONNECT_TIMEOUT":
    case "UND_ERR_HEADERS_TIMEOUT":
    case "UND_ERR_BODY_TIMEOUT":
      return "network_timeout";
    case "EAI_AGAIN":
      return "network_dns_temporary";
    case "ENETUNREACH":
    case "EHOSTUNREACH":
      return "network_unreachable";
    case "ECONNREFUSED":
      return "network_connection_refused";
    case "UND_ERR_SOCKET":
      return "network_socket_error";
    default:
      return void 0;
  }
}
function classifyFetchFailure(error) {
  return error instanceof TypeError && error.message === "fetch failed" ? "network_transport_failed" : void 0;
}
function findCauseCode(error) {
  const seen = /* @__PURE__ */ new Set();
  let current = error;
  while (current && typeof current === "object" && !seen.has(current)) {
    seen.add(current);
    const code = current.code;
    if (typeof code === "string" && code !== "")
      return code;
    current = current.cause;
  }
  return void 0;
}
function isAbort(error) {
  return error instanceof Error && (error.name === "AbortError" || error.name === "TimeoutError");
}
function transportMessage(code) {
  switch (code) {
    case "network_connection_reset":
      return "network connection was reset";
    case "network_timeout":
      return "network connection timed out";
    case "network_dns_temporary":
      return "DNS lookup was temporarily unavailable";
    case "network_unreachable":
      return "network was unreachable";
    case "network_connection_refused":
      return "network connection was refused";
    case "network_socket_error":
      return "network socket failed";
    case "network_transport_failed":
      return "network transport failed";
  }
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/client/http.js
var HttpError = class extends Error {
  status;
  code;
  payload;
  constructor(status, payload, fallbackMessage) {
    super(payload?.message || fallbackMessage);
    this.status = status;
    this.code = payload?.code || "unknown_error";
    this.payload = payload;
  }
};
var HttpClient = class _HttpClient {
  static MAX_TRANSPORT_RETRIES = 2;
  baseURL;
  fetchImpl;
  defaultHeaders;
  requestAuthorizer;
  recoverAuthorization;
  transportRetryDelayMs;
  constructor(config) {
    this.baseURL = config.baseURL.replace(/\/$/, "");
    this.fetchImpl = config.fetchImpl ?? globalThis.fetch;
    this.defaultHeaders = {
      "Content-Type": "application/json",
      Accept: "application/json",
      ...config.defaultHeaders ?? {}
    };
    this.requestAuthorizer = config.requestAuthorizer;
    this.recoverAuthorization = config.recoverAuthorization;
    this.transportRetryDelayMs = Math.max(0, config.transportRetryDelayMs ?? 200);
  }
  async request(path3, options = {}) {
    const url = path3.startsWith("http") ? path3 : this.baseURL + path3;
    const method = options.method ?? "GET";
    const body = options.body !== void 0 ? JSON.stringify(options.body) : "";
    const requestPath = new URL(url).pathname + new URL(url).search;
    const replaySafe = method === "GET" || Boolean(options.idempotencyKey) || options.replaySafe === true;
    let authorizationRecovered = false;
    let transportRetries = 0;
    for (; ; ) {
      const headers = { ...this.defaultHeaders };
      try {
        if (this.requestAuthorizer) {
          Object.assign(headers, await this.requestAuthorizer({ method, path: requestPath, body }));
        }
      } catch (error2) {
        if (error2 instanceof HttpTransportError)
          throw error2;
        throw asTransientTransportError(error2, 1) ?? error2;
      }
      if (options.bearer)
        headers.Authorization = `Bearer ${options.bearer}`;
      if (options.idempotencyKey)
        headers["Idempotency-Key"] = options.idempotencyKey;
      let response;
      let text;
      try {
        response = await this.fetchImpl(url, {
          method,
          headers,
          ...options.body !== void 0 ? { body } : {},
          ...options.signal ? { signal: options.signal } : {}
        });
        text = await response.text();
      } catch (error2) {
        if (options.signal?.aborted)
          throw error2;
        const transportError = asTransientTransportError(error2, transportRetries + 1);
        if (!transportError)
          throw error2;
        if (replaySafe && transportRetries < _HttpClient.MAX_TRANSPORT_RETRIES) {
          transportRetries += 1;
          await delay(this.transportRetryDelayMs * 2 ** (transportRetries - 1));
          continue;
        }
        throw asTransientTransportError(error2, transportRetries + 1) ?? error2;
      }
      const parsed = text.length > 0 ? safeParseJson(text) : void 0;
      if (response.ok)
        return parsed;
      const error = new HttpError(response.status, parsed, `HTTP ${response.status}`);
      if (!authorizationRecovered && error.status === 401 && error.code === "agent_device_session_required" && this.recoverAuthorization) {
        authorizationRecovered = true;
        await this.recoverAuthorization();
        continue;
      }
      throw error;
    }
  }
  get(path3, options = {}) {
    return this.request(path3, { ...options, method: "GET" });
  }
  post(path3, body, options = {}) {
    return this.request(path3, { ...options, method: "POST", body });
  }
  delete(path3, options = {}) {
    return this.request(path3, { ...options, method: "DELETE" });
  }
};
function delay(milliseconds) {
  return milliseconds === 0 ? Promise.resolve() : new Promise((resolve5) => setTimeout(resolve5, milliseconds));
}
function safeParseJson(text) {
  try {
    return JSON.parse(text);
  } catch {
    return void 0;
  }
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/client/backend.js
var BackendClient = class {
  http;
  constructor(http) {
    this.http = http;
  }
  readyz() {
    return this.http.get("/v1/readyz");
  }
  compatibility() {
    return this.http.get("/v1/platform/compatibility");
  }
  // --- Catalog ---
  getCatalogManifest() {
    return this.http.get("/v1/catalog/manifest");
  }
  // --- Cart ---
  createCart(input) {
    return this.http.post("/v1/carts", input);
  }
  getCart(cartID) {
    return this.http.get(`/v1/carts/${encodeURIComponent(cartID)}`);
  }
  addCartItem(cartID, input) {
    return this.http.post(`/v1/carts/${encodeURIComponent(cartID)}/items`, input);
  }
  removeCartItem(cartID, cartItemID) {
    return this.http.delete(`/v1/carts/${encodeURIComponent(cartID)}/items/${encodeURIComponent(cartItemID)}`);
  }
  abandonCart(cartID) {
    return this.http.delete(`/v1/carts/${encodeURIComponent(cartID)}`);
  }
  // --- Checkout ---
  createCheckout(input, idempotencyKey) {
    return this.http.post("/v1/checkouts", input, idempotencyKey ? { idempotencyKey } : void 0);
  }
  getCheckoutPresentation(checkoutID, displayToken, locale) {
    const qs = new URLSearchParams({ display_token: displayToken });
    if (locale)
      qs.set("locale", locale);
    return this.http.get(`/v1/checkouts/${encodeURIComponent(checkoutID)}/presentation?${qs}`);
  }
  // --- Payment intents ---
  createPaymentIntent(checkoutID, input) {
    return this.http.post(`/v1/checkouts/${encodeURIComponent(checkoutID)}/payment-intents`, input);
  }
  // --- SSE streaming ---
  streamCheckoutEvents(checkoutID, displayToken, onEvent, signal) {
    const qs = new URLSearchParams({ display_token: displayToken });
    const url = `${this.http.baseURL}/v1/checkouts/${encodeURIComponent(checkoutID)}/events?${qs}`;
    return streamSSE(url, onEvent, signal);
  }
  // --- Orders ---
  getOrder(orderID) {
    return this.http.get(`/v1/orders/${encodeURIComponent(orderID)}`);
  }
  getOrderDeliveryAccess(orderID) {
    return this.http.get(`/v1/orders/${encodeURIComponent(orderID)}/delivery-access`);
  }
  listAccountOrders(limit, status, bearer) {
    const qs = new URLSearchParams({ limit: String(limit) });
    if (status) {
      qs.set("status", status);
    }
    return this.http.get(`/v1/me/orders?${qs}`, bearer ? { bearer } : {});
  }
  // --- Refund ---
  createRefund(orderID, input, bearer, idempotencyKey) {
    const options = { ...bearer ? { bearer } : {}, ...idempotencyKey ? { idempotencyKey } : {} };
    return this.http.post(`/v1/orders/${encodeURIComponent(orderID)}/refunds`, input, options);
  }
  listOrderRefunds(orderID) {
    return this.http.get(`/v1/orders/${encodeURIComponent(orderID)}/refunds`);
  }
  getRefund(refundRequestID) {
    return this.http.get(`/v1/refunds/${encodeURIComponent(refundRequestID)}`);
  }
  cancelRefund(refundRequestID, reason = "buyer_cancelled") {
    return this.http.post(`/v1/refunds/${encodeURIComponent(refundRequestID)}/cancel`, { reason });
  }
  // --- Service Execution ---
  startServiceExecution(input) {
    return this.http.post("/v1/service-executions", input);
  }
  invokeServiceCapability(serviceExecutionID, capabilityID, input) {
    return this.http.post(`/v1/service-executions/${encodeURIComponent(serviceExecutionID)}/capabilities/${encodeURIComponent(capabilityID)}/invoke`, input, { replaySafe: Boolean(input.idempotency_key) });
  }
  recordServiceExecutionAction(serviceExecutionID, input) {
    return this.http.post(`/v1/service-executions/${encodeURIComponent(serviceExecutionID)}/actions`, input);
  }
  createServiceExecutionCheckout(serviceExecutionID, input) {
    return this.http.post(`/v1/service-executions/${encodeURIComponent(serviceExecutionID)}/checkout`, input, { replaySafe: true });
  }
  prepareServiceQuote(serviceExecutionID, input) {
    return this.http.post(`/v1/service-executions/${encodeURIComponent(serviceExecutionID)}/quotes`, input, { replaySafe: true });
  }
  getServiceExecution(serviceExecutionID) {
    return this.http.get(`/v1/service-executions/${encodeURIComponent(serviceExecutionID)}`);
  }
  listServiceExecutions(limit = 50) {
    return this.http.get(`/v1/service-executions?limit=${limit}`);
  }
  listServiceExecutionEvents(serviceExecutionID, afterSequence = 0, limit = 50) {
    const query = new URLSearchParams({
      after_sequence: String(afterSequence),
      limit: String(limit)
    });
    return this.http.get(`/v1/service-executions/${encodeURIComponent(serviceExecutionID)}/events?${query}`);
  }
  getGrantedServiceResult(serviceExecutionID) {
    return this.http.get(`/v1/service-executions/${encodeURIComponent(serviceExecutionID)}/granted-result`);
  }
};
async function streamSSE(url, onEvent, signal) {
  const response = await fetch(url, {
    headers: { Accept: "text/event-stream" },
    signal
  });
  if (!response.ok) {
    const text = await response.text();
    let msg = `SSE stream failed: HTTP ${response.status}`;
    try {
      const parsed = JSON.parse(text);
      msg = parsed.message || parsed.code || msg;
    } catch {
    }
    throw new Error(msg);
  }
  if (!response.body) {
    throw new Error("SSE stream: no response body");
  }
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done)
        break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";
      let currentEvent = {};
      for (const line of lines) {
        if (line === "") {
          if (currentEvent.type && currentEvent.payload) {
            onEvent(currentEvent);
          }
          currentEvent = {};
          continue;
        }
        if (line.startsWith("event: ")) {
          currentEvent.type = line.slice(7);
        } else if (line.startsWith("data: ")) {
          try {
            const data = JSON.parse(line.slice(6));
            currentEvent.type = currentEvent.type || data.event_type;
            currentEvent.aggregateType = data.aggregate_type;
            currentEvent.aggregateId = data.aggregate_id;
            currentEvent.sequence = data.sequence;
            currentEvent.payload = data;
          } catch {
          }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/state/agent_type.js
function declaredAgentType(env = process.env, argv = process.argv) {
  if (env.ITPAY_AGENT_TYPE)
    return canonicalAgentType(env.ITPAY_AGENT_TYPE);
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === "--agent-type")
      return canonicalAgentType(argv[index + 1]);
    if (value?.startsWith("--agent-type="))
      return canonicalAgentType(value.slice("--agent-type=".length));
  }
  return void 0;
}
function canonicalAgentType(value) {
  const normalized = value?.trim().toLowerCase();
  if (!normalized)
    return void 0;
  return normalized === "codex" ? "codex-desktop" : normalized;
}
function qualifyItPayCommand(command, agentType) {
  if (!agentType || !/^[a-z0-9-]+$/.test(agentType))
    return command;
  if (!command.startsWith("itpay ") || /^itpay\s+--agent-type(?:=|\s)/.test(command))
    return command;
  return `itpay --agent-type ${agentType} ${command.slice("itpay ".length)}`;
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/state/device_authority.js
import { createHash, createPrivateKey, createPublicKey, generateKeyPairSync, randomUUID, sign } from "node:crypto";
import { chmodSync, existsSync, mkdirSync, readFileSync, renameSync, rmdirSync, statSync, unlinkSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, resolve } from "node:path";
var PROTECTED_PATHS = ["/v1/carts", "/v1/service-executions", "/v1/agent-instances", "/v1/orders", "/v1/refunds"];
var DeviceAuthority = class {
  baseURL;
  backendKey;
  requestedAgentType;
  compatibilityHeaders;
  statePath;
  privateKeyPath;
  fetchImpl;
  pending;
  constructor(options) {
    this.baseURL = options.baseURL.replace(/\/$/, "");
    this.backendKey = normalizeBackendKey(options.baseURL);
    this.requestedAgentType = options.requestedAgentType;
    this.compatibilityHeaders = options.compatibilityHeaders;
    const root = resolve(homedir(), ".itpay-v3", "device");
    this.statePath = options.statePath ?? resolve(root, "identity.json");
    this.privateKeyPath = options.privateKeyPath ?? resolve(root, "device-private.pem");
    this.fetchImpl = (options.fetchImpl ?? globalThis.fetch).bind(globalThis);
  }
  async authorizationHeaders(input) {
    if (!PROTECTED_PATHS.some((prefix) => input.path.startsWith(prefix)))
      return {};
    const auth = await this.ensureAuthorization();
    const timestamp = (/* @__PURE__ */ new Date()).toISOString();
    const jti = randomUUID();
    const bodyHash = sha256(input.body);
    const message = requestProofMessage(input.method, input.path, bodyHash, timestamp, jti);
    const signature = sign(null, Buffer.from(message), auth.privateKey).toString("base64");
    return {
      Authorization: `ItPayDevice ${auth.session.token}`,
      "X-ItPay-Agent-Instance-ID": auth.state.agentInstances[auth.agentType] ?? "",
      "X-ItPay-Agent-Type": auth.agentType,
      "X-ItPay-Agent-Timestamp": timestamp,
      "X-ItPay-Agent-Proof-JTI": jti,
      "X-ItPay-Agent-Body-SHA256": bodyHash,
      "X-ItPay-Agent-Signature": signature
    };
  }
  async ensureAuthorization() {
    if (!this.pending) {
      this.pending = withFileLock(`${this.statePath}.lock`, () => this.prepareAuthorization()).finally(() => {
        this.pending = void 0;
      });
    }
    return this.pending;
  }
  async recoverAuthorization() {
    await withFileLock(`${this.statePath}.lock`, async () => {
      const state = this.readState();
      if (!state || !this.requestedAgentType)
        return;
      const registration = state.registrations[this.backendKey];
      if (!registration)
        return;
      delete registration.sessions[this.requestedAgentType];
      this.writeState(state);
    });
  }
  async recoverBackendReset() {
    return withFileLock(`${this.statePath}.lock`, async () => {
      const state = this.readState();
      const registration = state?.registrations[this.backendKey];
      if (!state || !registration)
        return { removed: false, agentTypes: [] };
      const agentTypes = Object.keys(registration.agentInstances).sort();
      delete state.registrations[this.backendKey];
      this.writeState(state);
      return { removed: true, agentTypes };
    });
  }
  async prepareAuthorization() {
    let state = this.readState() ?? emptyDeviceState();
    const agentType = this.requestedAgentType;
    if (!agentType) {
      throw new Error("agent type is required for ItPay commerce; pass --agent-type <type> or set ITPAY_AGENT_TYPE");
    }
    let privateKey = this.readPrivateKey();
    if (!privateKey) {
      const pair = generateKeyPairSync("ed25519");
      privateKey = pair.privateKey;
      this.writePrivateKey(pair.privateKey.export({ format: "pem", type: "pkcs8" }).toString());
      state = emptyDeviceState();
    }
    let registration = state.registrations[this.backendKey];
    if (!registration && state.legacyRegistration) {
      try {
        await this.ensureRegistrationAgentType(state.legacyRegistration, agentType, privateKey, true);
        registration = state.legacyRegistration;
        delete state.legacyRegistration;
      } catch (error) {
        if (!canMovePastLegacyRegistration(error))
          throw error;
      }
    }
    if (!registration) {
      registration = await this.enroll(agentType, privateKey);
    }
    state.registrations[this.backendKey] = registration;
    const session = await this.ensureRegistrationAgentType(registration, agentType, privateKey, false);
    this.writeState(state);
    return { state: registration, agentType, session, privateKey };
  }
  async ensureRegistrationAgentType(registration, agentType, privateKey, forceSession) {
    if (!registration.agentInstances[agentType]) {
      const existingType = firstAgentType(registration);
      if (!existingType)
        throw new Error("device has no registered agent instance");
      const existingSession = await this.ensureSession(registration, existingType, privateKey, forceSession);
      const registered = await this.signedJSON("/v1/agent-instances", { agent_type: agentType }, registration, existingType, existingSession, privateKey);
      registration.agentInstances[agentType] = registered.agent_instance_id;
    }
    return this.ensureSession(registration, agentType, privateKey, forceSession);
  }
  async enroll(agentType, privateKey) {
    const publicJWK = createPublicKey(privateKey).export({ format: "jwk" });
    if (!publicJWK.x)
      throw new Error("unable to export Ed25519 public key");
    const publicKey = Buffer.from(publicJWK.x, "base64url").toString("base64");
    const started = await this.publicJSON("/v1/agent-device-enrollments", { public_key: publicKey, agent_type: agentType });
    const proof = enrollmentProofMessage(started.agent_device_enrollment_id, started.challenge);
    const verified = await this.publicJSON(`/v1/agent-device-enrollments/${encodeURIComponent(started.agent_device_enrollment_id)}/verify`, { challenge: started.challenge, signature: sign(null, Buffer.from(proof), privateKey).toString("base64") });
    return {
      deviceID: verified.agent_device_id,
      deviceKeyID: verified.agent_device_key_id,
      quotaLineageID: verified.quota_lineage_id,
      agentInstances: { [verified.agent_type]: verified.agent_instance_id },
      sessions: {}
    };
  }
  async ensureSession(state, agentType, privateKey, force = false) {
    const existing = state.sessions[agentType];
    if (!force && existing && Date.parse(existing.expiresAt) > Date.now() + 6e4)
      return existing;
    const instanceID = state.agentInstances[agentType];
    if (!instanceID)
      throw new Error(`agent instance is not registered for ${agentType}`);
    const challenge = await this.publicJSON("/v1/agent-device-session-challenges", {
      agent_device_id: state.deviceID,
      agent_instance_id: instanceID
    });
    const proof = deviceSessionProofMessage(challenge.agent_device_session_challenge_id, challenge.challenge);
    const verified = await this.publicJSON(`/v1/agent-device-session-challenges/${encodeURIComponent(challenge.agent_device_session_challenge_id)}/verify`, { challenge: challenge.challenge, signature: sign(null, Buffer.from(proof), privateKey).toString("base64") });
    const session = { token: verified.session_token, expiresAt: verified.expires_at };
    state.sessions[agentType] = session;
    return session;
  }
  async signedJSON(path3, bodyValue, state, agentType, session, privateKey) {
    const body = JSON.stringify(bodyValue);
    const timestamp = (/* @__PURE__ */ new Date()).toISOString();
    const jti = randomUUID();
    const bodyHash = sha256(body);
    const signature = sign(null, Buffer.from(requestProofMessage("POST", path3, bodyHash, timestamp, jti)), privateKey).toString("base64");
    return this.fetchJSON(path3, body, {
      Authorization: `ItPayDevice ${session.token}`,
      "X-ItPay-Agent-Instance-ID": state.agentInstances[agentType] ?? "",
      "X-ItPay-Agent-Type": agentType,
      "X-ItPay-Agent-Timestamp": timestamp,
      "X-ItPay-Agent-Proof-JTI": jti,
      "X-ItPay-Agent-Body-SHA256": bodyHash,
      "X-ItPay-Agent-Signature": signature
    });
  }
  publicJSON(path3, bodyValue) {
    return this.fetchJSON(path3, JSON.stringify(bodyValue), {});
  }
  async fetchJSON(path3, body, extraHeaders) {
    const response = await this.fetchImpl(this.baseURL + path3, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json", ...this.compatibilityHeaders, ...extraHeaders },
      body
    });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok)
      throw new DeviceAuthorizationError(response.status, payload.code, payload.message || payload.code || `ItPay device request failed: ${response.status}`);
    return payload;
  }
  readState() {
    if (!existsSync(this.statePath))
      return void 0;
    try {
      const parsed = JSON.parse(readFileSync(this.statePath, "utf8"));
      if (parsed.schemaVersion === "itpay.device.v2")
        return parsed;
      if (parsed.schemaVersion === "itpay.device.v1") {
        const { schemaVersion: _, ...legacyRegistration } = parsed;
        return { ...emptyDeviceState(), legacyRegistration };
      }
      return void 0;
    } catch (error) {
      const stateError = asDeviceStateError(error, "read_state");
      if (stateError)
        throw stateError;
      return void 0;
    }
  }
  readPrivateKey() {
    if (!existsSync(this.privateKeyPath))
      return void 0;
    try {
      return createPrivateKey(readFileSync(this.privateKeyPath, "utf8"));
    } catch (error) {
      const stateError = asDeviceStateError(error, "read_private_key");
      if (stateError)
        throw stateError;
      return void 0;
    }
  }
  writeState(state) {
    atomicOwnerOnlyWrite(this.statePath, JSON.stringify(state, null, 2), "write_state");
  }
  writePrivateKey(value) {
    atomicOwnerOnlyWrite(this.privateKeyPath, value, "write_private_key");
  }
};
var DeviceAuthorizationError = class extends Error {
  status;
  code;
  constructor(status, code, message) {
    super(message);
    this.status = status;
    this.code = code;
    this.name = "DeviceAuthorizationError";
  }
};
var DeviceStateError = class extends Error {
  operation;
  causeCode;
  code = "device_state_unwritable";
  constructor(operation, causeCode) {
    super(`ItPay device state operation failed: ${operation} (${causeCode})`);
    this.operation = operation;
    this.causeCode = causeCode;
    this.name = "DeviceStateError";
  }
};
function emptyDeviceState() {
  return { schemaVersion: "itpay.device.v2", registrations: {} };
}
function firstAgentType(state) {
  return Object.keys(state.agentInstances)[0];
}
function canMovePastLegacyRegistration(error) {
  return error instanceof DeviceAuthorizationError && (error.code === "agent_device_revoked" || error.status === 404);
}
function normalizeBackendKey(value) {
  const url = new URL(value);
  url.search = "";
  url.hash = "";
  url.pathname = url.pathname.replace(/\/+$/, "");
  return url.toString().replace(/\/$/, "");
}
function sha256(value) {
  return `sha256:${createHash("sha256").update(value).digest("hex")}`;
}
function enrollmentProofMessage(id, challenge) {
  return `itpay-device-enrollment/v1
${id}
${challenge}`;
}
function deviceSessionProofMessage(id, challenge) {
  return `itpay-device-session/v1
${id}
${challenge}`;
}
function requestProofMessage(method, path3, bodyHash, timestamp, jti) {
  return ["itpay-agent-request/v1", method, path3, bodyHash, timestamp, jti].join("\n");
}
function atomicOwnerOnlyWrite(path3, value, operation) {
  const temporary = `${path3}.${process.pid}.${randomUUID()}.tmp`;
  try {
    mkdirSync(dirname(path3), { recursive: true, mode: 448 });
    writeFileSync(temporary, value, { encoding: "utf8", mode: 384 });
    chmodSync(temporary, 384);
    renameSync(temporary, path3);
    chmodSync(path3, 384);
  } catch (error) {
    try {
      unlinkSync(temporary);
    } catch {
    }
    throw asDeviceStatePathError(error, operation) ?? error;
  }
}
async function withFileLock(path3, run) {
  try {
    mkdirSync(dirname(path3), { recursive: true, mode: 448 });
  } catch (error) {
    throw asDeviceStatePathError(error, "prepare_lock") ?? error;
  }
  let acquired = false;
  for (let attempt = 0; attempt < 200; attempt += 1) {
    try {
      mkdirSync(path3, { mode: 448 });
      acquired = true;
      break;
    } catch (error) {
      const code = error.code;
      if (code !== "EEXIST")
        throw asDeviceStateError(error, "acquire_lock") ?? error;
      try {
        if (Date.now() - statSync(path3).mtimeMs > 3e4)
          removeLock(path3, "remove_stale_lock");
      } catch (statError) {
        if (statError.code !== "ENOENT") {
          throw asDeviceStateError(statError, "inspect_lock") ?? statError;
        }
      }
      await new Promise((resolve5) => setTimeout(resolve5, 25));
    }
  }
  if (!acquired)
    throw new Error("timed out waiting for ItPay device identity lock");
  try {
    return await run();
  } finally {
    removeLock(path3, "release_lock");
  }
}
function removeLock(path3, operation) {
  try {
    if (statSync(path3).isDirectory())
      rmdirSync(path3);
    else
      unlinkSync(path3);
  } catch (error) {
    if (error.code !== "ENOENT")
      throw asDeviceStateError(error, operation) ?? error;
  }
}
function asDeviceStateError(error, operation) {
  const code = error.code;
  return code === "EACCES" || code === "EPERM" || code === "EROFS" || code === "ENOTDIR" || code === "EISDIR" ? new DeviceStateError(operation, code) : void 0;
}
function asDeviceStatePathError(error, operation) {
  const code = error.code;
  return code === "EEXIST" ? new DeviceStateError(operation, code) : asDeviceStateError(error, operation);
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/state/operation_journal.js
import { chmodSync as chmodSync2, closeSync, existsSync as existsSync2, mkdirSync as mkdirSync2, openSync, readFileSync as readFileSync2, renameSync as renameSync2, statSync as statSync2, unlinkSync as unlinkSync2, writeFileSync as writeFileSync2 } from "node:fs";
import { dirname as dirname2 } from "node:path";
import { randomUUID as randomUUID2 } from "node:crypto";
var OperationJournal = class {
  path;
  constructor(path3) {
    this.path = path3;
  }
  async getOrCreate(operationKey) {
    return withFileLock2(`${this.path}.lock`, async () => {
      const state = this.read();
      const existing = state.operations[operationKey];
      if (existing)
        return existing.id;
      const id = `op_${randomUUID2().replaceAll("-", "")}`;
      state.operations[operationKey] = { id, createdAt: (/* @__PURE__ */ new Date()).toISOString() };
      atomicOwnerOnlyWrite2(this.path, JSON.stringify(state, null, 2));
      return id;
    });
  }
  read() {
    if (existsSync2(this.path)) {
      try {
        const parsed = JSON.parse(readFileSync2(this.path, "utf8"));
        if (parsed.schemaVersion === "itpay.operations.v1" && parsed.operations)
          return parsed;
      } catch {
      }
    }
    return { schemaVersion: "itpay.operations.v1", operations: {} };
  }
};
function atomicOwnerOnlyWrite2(path3, value) {
  mkdirSync2(dirname2(path3), { recursive: true, mode: 448 });
  const temporary = `${path3}.${process.pid}.${randomUUID2()}.tmp`;
  writeFileSync2(temporary, value, { encoding: "utf8", mode: 384 });
  chmodSync2(temporary, 384);
  renameSync2(temporary, path3);
  chmodSync2(path3, 384);
}
async function withFileLock2(path3, run) {
  mkdirSync2(dirname2(path3), { recursive: true, mode: 448 });
  let descriptor;
  for (let attempt = 0; attempt < 200; attempt += 1) {
    try {
      descriptor = openSync(path3, "wx", 384);
      break;
    } catch (error) {
      if (error.code !== "EEXIST")
        throw error;
      try {
        if (Date.now() - statSync2(path3).mtimeMs > 3e4)
          unlinkSync2(path3);
      } catch (statError) {
        if (statError.code !== "ENOENT")
          throw statError;
      }
      await new Promise((resolve5) => setTimeout(resolve5, 25));
    }
  }
  if (descriptor === void 0)
    throw new Error("timed out waiting for ItPay operation journal lock");
  try {
    return await run();
  } finally {
    closeSync(descriptor);
    try {
      unlinkSync2(path3);
    } catch (error) {
      if (error.code !== "ENOENT")
        throw error;
    }
  }
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/state/config.js
var DEFAULT_BASE_URL = "https://app.itpay.ai";
var DEV_BASE_URL = "https://dev.itpay.ai";
var CLI_VERSION = "2.0.25";
var API_CONTRACT_REVISION = "sha256:d4e94049c01b38bc77dce76bf4e49e8243adfc588541e33af6477cd5722a5bc4";
var CART_SESSION_DEFAULT_DIR = ".itpay-v3";
var CART_SESSION_FILENAME = "cart.json";
var OPERATION_JOURNAL_FILENAME = "operations.json";
function cliDistribution(env = process.env) {
  if (env.ITPAY_DISTRIBUTION === "openclaw-skill-bundle")
    return "openclaw-skill-bundle";
  if (env.ITPAY_DISTRIBUTION === "kimi-plugin-bundle")
    return "kimi-plugin-bundle";
  return "npm";
}
var BackendOverrideError = class extends Error {
  code = "backend_override_forbidden";
  constructor() {
    super(`ITPAY_BACKEND_URL only supports ${DEFAULT_BASE_URL} or ${DEV_BASE_URL}`);
    this.name = "BackendOverrideError";
  }
};
function resolveBackendURL(env = process.env) {
  const requested = env.ITPAY_BACKEND_URL?.trim();
  if (!requested || requested === DEFAULT_BASE_URL || requested === `${DEFAULT_BASE_URL}/`)
    return DEFAULT_BASE_URL;
  if (requested === DEV_BASE_URL || requested === `${DEV_BASE_URL}/`)
    return DEV_BASE_URL;
  throw new BackendOverrideError();
}
function qualifyBackendCommand(command, env = process.env) {
  const requested = env.ITPAY_BACKEND_URL?.trim();
  if (requested !== DEV_BASE_URL && requested !== `${DEV_BASE_URL}/`)
    return command;
  if (!command.startsWith("itpay ") || command.startsWith(`ITPAY_BACKEND_URL=${DEV_BASE_URL} `))
    return command;
  return `ITPAY_BACKEND_URL=${DEV_BASE_URL} ${command}`;
}
function stateFilename(filename, baseURL) {
  if (baseURL !== DEV_BASE_URL)
    return filename;
  const dot = filename.lastIndexOf(".");
  return dot < 0 ? `${filename}.dev` : `${filename.slice(0, dot)}.dev${filename.slice(dot)}`;
}
function stateDir(env) {
  return resolve2(env.HOME || homedir2(), CART_SESSION_DEFAULT_DIR);
}
function cartSessionPath(env = process.env) {
  if (env.ITPAY_CART_SESSION_PATH) {
    return resolve2(env.ITPAY_CART_SESSION_PATH);
  }
  const dir = stateDir(env);
  mkdirSync3(dir, { recursive: true });
  return resolve2(dir, stateFilename(CART_SESSION_FILENAME, resolveBackendURL(env)));
}
function loadConfig(env = process.env) {
  const baseURL = resolveBackendURL(env);
  const bearerToken = env.ITPAY_BEARER_TOKEN || void 0;
  const agentType = declaredAgentType(env);
  const checkoutCurrency = env.ITPAY_CURRENCY || "CNY";
  const idempotencyKey = env.ITPAY_IDEMPOTENCY_KEY || `cli_${shortRandom()}`;
  const ideImageAttach = env.ITPAY_IDE_IMAGE_ATTACH !== "0";
  const ideImageDirOverride = env.ITPAY_IDE_IMAGE_DIR_OVERRIDE;
  return {
    baseURL,
    environment: baseURL === DEV_BASE_URL ? "development" : "production",
    ...agentType ? { agentType } : {},
    checkoutCurrency,
    idempotencyKey,
    ...!env.ITPAY_IDEMPOTENCY_KEY ? { operationJournal: new OperationJournal(resolve2(stateDir(env), stateFilename(OPERATION_JOURNAL_FILENAME, baseURL))) } : {},
    ideImageAttach,
    ...ideImageDirOverride ? { ideImageDirOverride } : {},
    ...bearerToken ? { bearerToken } : {}
  };
}
function operationID(config, operationKey) {
  if (config.operationJournal)
    return config.operationJournal.getOrCreate(operationKey);
  return Promise.resolve(config.idempotencyKey);
}
function newBackendClient(config) {
  const authority = new DeviceAuthority({
    baseURL: config.baseURL,
    ...config.agentType ? { requestedAgentType: config.agentType } : {},
    compatibilityHeaders: {
      "X-ItPay-CLI-Version": CLI_VERSION,
      "X-ItPay-Contract-Revision": API_CONTRACT_REVISION
    }
  });
  const http = new HttpClient({
    baseURL: config.baseURL,
    defaultHeaders: {
      "X-ItPay-CLI-Version": CLI_VERSION,
      "X-ItPay-Contract-Revision": API_CONTRACT_REVISION
    },
    requestAuthorizer: (input) => authority.authorizationHeaders(input),
    recoverAuthorization: () => authority.recoverAuthorization()
  });
  return new BackendClient(http);
}
function shortRandom() {
  return Math.random().toString(36).slice(2, 10) + Math.random().toString(36).slice(2, 6);
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/state/cart_session.js
import { chmodSync as chmodSync3, existsSync as existsSync3, mkdirSync as mkdirSync4, readFileSync as readFileSync3, renameSync as renameSync3, writeFileSync as writeFileSync3 } from "node:fs";
import { randomUUID as randomUUID3 } from "node:crypto";
import { dirname as dirname3 } from "node:path";
var CartSession = class _CartSession {
  state;
  loadFailed = false;
  constructor(currency) {
    this.state = { currency, items: [] };
  }
  static loadFromFile(path3, currency) {
    const session = new _CartSession(currency);
    if (existsSync3(path3)) {
      try {
        const raw = readFileSync3(path3, "utf-8");
        const persisted = JSON.parse(raw);
        if (Array.isArray(persisted.items)) {
          persisted.items.forEach((item) => {
            if (item.catalogVariantID && item.offerID && item.quantity > 0) {
              session.state.items.push({ ...item });
            }
          });
        }
        if (persisted.lastCartID)
          session.state.lastCartID = persisted.lastCartID;
        if (persisted.lastCartItemID)
          session.state.lastCartItemID = persisted.lastCartItemID;
        if (persisted.lastServiceExecutionID)
          session.state.lastServiceExecutionID = persisted.lastServiceExecutionID;
        if (persisted.lastCheckoutID)
          session.state.lastCheckoutID = persisted.lastCheckoutID;
        if (persisted.lastDisplayToken)
          session.state.lastDisplayToken = persisted.lastDisplayToken;
        if (persisted.lastCheckoutURL)
          session.state.lastCheckoutURL = persisted.lastCheckoutURL;
      } catch {
        session.state.items = [];
        session.loadFailed = true;
      }
    }
    return session;
  }
  saveToFile(path3) {
    const toSave = {
      currency: this.state.currency,
      items: this.state.items.map((item) => ({ ...item })),
      ...this.state.lastCartID ? { lastCartID: this.state.lastCartID } : {},
      ...this.state.lastCartItemID ? { lastCartItemID: this.state.lastCartItemID } : {},
      ...this.state.lastServiceExecutionID ? { lastServiceExecutionID: this.state.lastServiceExecutionID } : {},
      ...this.state.lastCheckoutID ? { lastCheckoutID: this.state.lastCheckoutID } : {},
      ...this.state.lastDisplayToken ? { lastDisplayToken: this.state.lastDisplayToken } : {},
      ...this.state.lastCheckoutURL ? { lastCheckoutURL: this.state.lastCheckoutURL } : {}
    };
    mkdirSync4(dirname3(path3), { recursive: true, mode: 448 });
    const temporary = `${path3}.${process.pid}.${randomUUID3()}.tmp`;
    writeFileSync3(temporary, JSON.stringify(toSave, null, 2), { encoding: "utf-8", mode: 384 });
    chmodSync3(temporary, 384);
    renameSync3(temporary, path3);
    chmodSync3(path3, 384);
  }
  add(item) {
    if (item.quantity <= 0) {
      throw new Error("quantity must be > 0");
    }
    const existing = this.state.items.find((i) => i.catalogVariantID === item.catalogVariantID && i.offerID === item.offerID);
    if (existing) {
      existing.quantity += item.quantity;
      if (item.input)
        existing.input = item.input;
      return;
    }
    this.state.items.push({ ...item });
  }
  remove(variantID, offerID) {
    const before = this.state.items.length;
    this.state.items = this.state.items.filter((i) => !(i.catalogVariantID === variantID && i.offerID === offerID));
    if (this.state.items.length === before) {
      throw new Error(`no line matches variant=${variantID} offer=${offerID}`);
    }
  }
  clear() {
    this.state = { currency: this.state.currency, items: [] };
  }
  show() {
    return JSON.parse(JSON.stringify(this.state));
  }
  toCreateCartRequest() {
    return {
      currency: this.state.currency,
      items: this.state.items.map((item) => ({
        catalog_item_id: item.catalogItemID,
        catalog_variant_id: item.catalogVariantID,
        offer_id: item.offerID,
        quantity: item.quantity,
        ...item.input ? { input: item.input } : {}
      }))
    };
  }
  rememberCheckout(input) {
    this.state.items = [];
    delete this.state.lastCartID;
    delete this.state.lastCartItemID;
    this.state.lastCheckoutID = input.checkoutID;
    this.state.lastDisplayToken = input.displayToken;
    this.state.lastCheckoutURL = input.checkoutURL;
    if (input.serviceExecutionID)
      this.state.lastServiceExecutionID = input.serviceExecutionID;
  }
  rememberServerCart(input) {
    this.state.items = [];
    this.state.lastCartID = input.cartID;
    delete this.state.lastCartItemID;
    delete this.state.lastServiceExecutionID;
    delete this.state.lastCheckoutID;
    delete this.state.lastDisplayToken;
    delete this.state.lastCheckoutURL;
    if (input.cartItemID)
      this.state.lastCartItemID = input.cartItemID;
    if (input.serviceExecutionID)
      this.state.lastServiceExecutionID = input.serviceExecutionID;
  }
  get lastCartID() {
    return this.state.lastCartID;
  }
  get lastCartItemID() {
    return this.state.lastCartItemID;
  }
  get lastServiceExecutionID() {
    return this.state.lastServiceExecutionID;
  }
  get lastCheckoutID() {
    return this.state.lastCheckoutID;
  }
  get lastDisplayToken() {
    return this.state.lastDisplayToken;
  }
  get currency() {
    return this.state.currency;
  }
  get stateLoadFailed() {
    return this.loadFailed;
  }
};

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/state/client_context.js
var SUPPORTED_HOSTS = /* @__PURE__ */ new Set([
  "terminal",
  "codex",
  "claude-code",
  "telegram",
  "discord",
  "whatsapp",
  "feishu",
  "lark",
  "plain-chat"
]);
var HOSTS_REQUIRING_TARGET = /* @__PURE__ */ new Set([
  "telegram",
  "discord",
  "whatsapp",
  "feishu",
  "lark"
]);
var HOST_ALIASES = {
  tg: "telegram",
  "openclaw-telegram": "telegram",
  trae: "codex",
  "trae-agent": "codex",
  feishu_im: "feishu",
  fs: "feishu"
};
function normalizeHost(raw) {
  if (!raw)
    return void 0;
  const lower = raw.trim().toLowerCase();
  if (SUPPORTED_HOSTS.has(lower))
    return lower;
  return HOST_ALIASES[lower];
}
function requiresTarget(host) {
  return HOSTS_REQUIRING_TARGET.has(host);
}
function defaultHostForAgentType(agentType) {
  const normalized = agentType?.trim().toLowerCase() ?? "";
  if (normalized === "codex-desktop")
    return "codex";
  if (normalized === "claude-code-desktop")
    return "claude-code";
  if (normalized === "workbuddy")
    return "plain-chat";
  if (normalized === "openclaw")
    return void 0;
  return "terminal";
}
function validateContext(host, target) {
  if (!host) {
    return { code: "client_context_required", message: "--host is required" };
  }
  if (requiresTarget(host) && !target) {
    return { code: "target_required", message: `--target is required for host ${host}` };
  }
  return void 0;
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/render/sink.js
var defaultOutput = (line) => process.stdout.write(line);
function resolveOutput(sink) {
  return sink ?? defaultOutput;
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/commands/guidance.js
function isTerminalServiceExecutionStatus(status) {
  return status === "failed" || status === "refunded" || status === "cancelled";
}
var CommandContractError = class extends Error {
  code;
  instruction;
  recovery;
  constructor(code, message, instruction, recovery) {
    super(message);
    this.code = code;
    this.instruction = instruction;
    this.recovery = recovery;
    this.name = "CommandContractError";
  }
};
function writeCommandEnvelope(value, options = {}) {
  const out = resolveOutput(options.output);
  const agentType = options.agentType ?? declaredAgentType();
  const qualified = qualifyEnvelope(value, agentType);
  if (options.jsonOutput) {
    out(JSON.stringify(qualified, null, 2) + "\n");
    return;
  }
  out(`${qualified.status}
`);
  const facts = "error" in qualified ? qualified.error : qualified.result;
  if (options.plainResult) {
    for (const line of options.plainResult)
      out(`${line}
`);
  } else {
    for (const [key, fact] of Object.entries(facts)) {
      out(`${key}: ${typeof fact === "string" ? fact : JSON.stringify(fact)}
`);
    }
    if ("error" in qualified && qualified.result) {
      for (const [key, fact] of Object.entries(qualified.result)) {
        out(`${key}: ${typeof fact === "string" ? fact : JSON.stringify(fact)}
`);
      }
    }
  }
  if ("handoff" in qualified && qualified.handoff) {
    for (const [key, fact] of Object.entries(qualified.handoff)) {
      out(`handoff.${key}: ${typeof fact === "string" ? fact : JSON.stringify(fact)}
`);
    }
  }
  out(`instruction: ${qualified.instruction}
`);
  if (qualified.next)
    out(`next: ${qualified.next.command}
`);
  if (qualified.recovery.length > 0) {
    out("recovery:\n");
    for (const action of qualified.recovery) {
      out(`  - ${action.command}
`);
      out(`    reason: ${action.reason}
`);
    }
  }
}
function qualifyEnvelope(value, agentType) {
  return {
    ...value,
    next: value.next ? { ...value.next, command: qualifyBackendCommand(qualifyItPayCommand(value.next.command, agentType)) } : null,
    recovery: value.recovery.map((action) => ({
      ...action,
      command: qualifyBackendCommand(qualifyItPayCommand(action.command, agentType))
    }))
  };
}
function errorRecoveryActions(error) {
  if (!(error instanceof HttpError))
    return [];
  if (error.code === "agent_identity_required") {
    return [
      {
        id: "inspect_agent_setup",
        label: "Inspect supported Agent Type setup",
        command: "itpay install --json"
      }
    ];
  }
  if (error.code === "agent_device_session_required") {
    return [
      {
        id: "read_agent_session_rules",
        label: "Read ItPay identity and session recovery rules",
        command: "itpay skill show itpay --json",
        reason: "The CLI already attempted one automatic session renewal; do not rotate identity or loop retries."
      }
    ];
  }
  if (error.code === "quota_exhausted" || error.code === "checkout_required") {
    return [
      {
        id: "inspect_service_execution",
        label: "Inspect Service Execution before checkout",
        command: "itpay services next <service_execution_id> --json"
      }
    ];
  }
  if (error.code === "cart_item_locked" || error.status === 409) {
    return [
      {
        id: "show_cart",
        label: "Inspect the canonical server cart",
        command: "itpay cart show"
      },
      {
        id: "continue_checkout",
        label: "Continue the last locally remembered checkout",
        command: "itpay checkout"
      },
      {
        id: "recover_service_execution",
        label: "List recoverable Service Executions if the local handoff is missing",
        command: "itpay services list"
      }
    ];
  }
  if (error.status === 404) {
    return [
      {
        id: "recover_service_executions",
        label: "List visible Service Executions and follow their next instruction",
        command: "itpay services list"
      }
    ];
  }
  if (error.status === 502 || error.status === 503 || error.status === 504) {
    return [
      {
        id: "retry_after_backend_recovers",
        label: "Retry after the selected official Backend is reachable",
        command: "itpay readyz"
      }
    ];
  }
  return [];
}
function printErrorRecovery(error, output) {
  const recovery = errorRecoveryActions(error);
  if (recovery.length === 0)
    return;
  const out = resolveOutput(output);
  out("recovery:\n");
  for (const action of recovery) {
    out(`  - ${action.label}
`);
    out(`    ${action.command}
`);
  }
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/commands/readyz.js
async function runReadyz(backend, options = {}) {
  const response = await backend.readyz();
  const backendURL = options.backendURL ?? "https://app.itpay.ai";
  const environment = options.environment ?? "production";
  writeCommandEnvelope({
    status: response.status,
    result: { backend: "available", backend_url: backendURL, environment, ...options.agentType ? { agent_type: options.agentType } : {} },
    instruction: environment === "development" ? "ItPay dev \u53EF\u7528\uFF1B\u540E\u7EED\u5FC5\u987B\u6267\u884C\u8FD4\u56DE\u7684\u5B8C\u6574\u547D\u4EE4\uFF0C\u5E76\u7EE7\u7EED\u4F7F\u7528\u540C\u4E00\u4E2A dev Backend\u3002\u5148\u5B8C\u6574\u8BFB\u53D6\u5185\u7F6E ItPay Skill\uFF0C\u518D\u8FDB\u5165\u5F53\u524D\u5DF2\u652F\u6301\u7684 buy \u6D41\u7A0B\u3002" : "ItPay \u53EF\u7528\uFF1B\u5148\u5B8C\u6574\u8BFB\u53D6\u5185\u7F6E ItPay Skill\uFF0C\u518D\u8FDB\u5165\u5F53\u524D\u5DF2\u652F\u6301\u7684 buy \u6D41\u7A0B\u3002sell \u5C06\u6765\u4E5F\u4F7F\u7528\u540C\u4E00\u5165\u53E3\uFF0C\u4F46\u5F53\u524D\u5C1A\u672A\u5B9E\u73B0\u3002",
    next: { command: "itpay skill show itpay --json", reason: "\u52A0\u8F7D\u5B8C\u6574\u64CD\u4F5C\u4E0E\u5B89\u5168\u89C4\u5219" },
    recovery: []
  }, options);
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/render/qr.js
var import_qrcode = __toESM(require_lib(), 1);
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { randomUUID as randomUUID4 } from "node:crypto";
function terminalQRType(format) {
  return format === "utf8" ? "utf8" : "terminal";
}
async function renderTerminalQR(url, format) {
  return import_qrcode.default.toString(url, {
    type: format === "unicode" ? "utf8" : terminalQRType(format),
    small: true,
    errorCorrectionLevel: "L"
  });
}
async function writeLocalPNG(url) {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "itpay-v3-"));
  const filePath = path.join(dir, `itpay-${randomUUID4()}.png`);
  await import_qrcode.default.toFile(filePath, url, {
    type: "png",
    errorCorrectionLevel: "M",
    margin: 2,
    width: 512
  });
  return { filePath, mimeType: "image/png" };
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/render/terminal_image.js
import { readFileSync as readFileSync4 } from "node:fs";
import path2 from "node:path";
function supportsInlineTerminalImages() {
  return Boolean(process.env.ITERM_SESSION_ID) || process.env.TERM_PROGRAM === "iTerm.app";
}
function renderInlineTerminalImage(filePath, out) {
  if (!supportsInlineTerminalImages())
    return;
  try {
    const buf = readFileSync4(filePath);
    const name = path2.basename(filePath);
    const nameB64 = Buffer.from(name).toString("base64");
    const dataB64 = buf.toString("base64");
    out(`\x1B]1337;File=name=${nameB64};size=${buf.length};inline=1;preserveAspectRatio=1:${dataB64}\x07
`);
  } catch {
    return;
  }
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/render/ide.js
import { mkdirSync as mkdirSync5, readFileSync as readFileSync5, renameSync as renameSync4, writeFileSync as writeFileSync4 } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { createHash as createHash2, randomUUID as randomUUID5 } from "node:crypto";
var IDE_ATTACH_REASON = "Human cannot scan a remote URL: the IDE chat window is the only surface they can pay from. The agent MUST render this PNG into the IDE chat (Trae `Read` tool with the localPath or one of the mirrors) and wait for the human to confirm they see + scan it. If the image is not visible in chat, the checkout is considered failed \u2014 re-render and ask again, do not mark the order complete.";
function canonicalDir(env = process.env) {
  const override = env.ITPAY_IDE_IMAGE_DIR_OVERRIDE;
  if (override && override.length > 0)
    return override;
  return join(tmpdir(), "itpay-v3-qr");
}
function resolveIdeImageDirs(env = process.env) {
  const canonical = canonicalDir(env);
  const dirs = [canonical];
  if (process.platform === "win32")
    return dirs;
  const tmps = "/tmp/itpay-v3-qr";
  if (tmps === canonical)
    return dirs;
  try {
    mkdirSync5(tmps, { recursive: true });
    dirs.push(tmps);
  } catch {
  }
  return dirs;
}
function stableNameFor(kind, id) {
  const safeID = id.replace(/[^a-zA-Z0-9_-]/g, "_") || randomUUID5();
  const hash = createHash2("sha1").update(`${kind}:${id}`).digest("hex").slice(0, 6);
  return `itpay-v3-${kind}-${safeID}-${hash}`;
}
async function detectImageFormat(url, fetchFn) {
  const r = await fetchFn(url);
  if (!r.ok)
    throw new Error(`http=${r.status}`);
  const ab = await r.arrayBuffer();
  const buf = Buffer.from(ab);
  if (buf.length >= 2 && buf[0] === 137 && buf[1] === 80) {
    return { ext: ".png", body: buf };
  }
  if (buf.length >= 2 && buf[0] === 255 && buf[1] === 216) {
    return { ext: ".jpg", body: buf };
  }
  if (buf.length >= 4 && buf.toString("ascii", 0, 4) === "RIFF") {
    return { ext: ".webp", body: buf };
  }
  if (buf.length >= 4 && buf.toString("ascii", 0, 4) === "<svg") {
    return { ext: ".svg", body: buf };
  }
  if (buf.length >= 5 && buf.toString("ascii", 0, 5) === "<?xml") {
    return { ext: ".svg", body: buf };
  }
  const ct = (r.headers.get("content-type") ?? "").toLowerCase();
  if (ct.includes("svg+xml") || ct.includes("svg"))
    return { ext: ".svg", body: buf };
  if (ct.includes("webp"))
    return { ext: ".webp", body: buf };
  if (ct.includes("jpeg") || ct.includes("jpg"))
    return { ext: ".jpg", body: buf };
  if (ct.includes("png"))
    return { ext: ".png", body: buf };
  return { ext: ".png", body: buf };
}
function atomicWrite(filePath, body) {
  const tmp = `${filePath}.tmp-${randomUUID5()}`;
  writeFileSync4(tmp, body);
  renameSync4(tmp, filePath);
}
function mirrorToDirs(fileName, body, dirs) {
  const written = [];
  for (const dir of dirs.slice(1)) {
    try {
      mkdirSync5(dir, { recursive: true });
      const target = join(dir, fileName);
      atomicWrite(target, body);
      written.push(target);
    } catch {
    }
  }
  return written;
}
function mimeFor(ext) {
  switch (ext) {
    case ".png":
      return "image/png";
    case ".jpg":
      return "image/jpeg";
    case ".webp":
      return "image/webp";
    case ".svg":
      return "image/svg+xml";
  }
}
function resolveFetchURL(url, baseURL) {
  if (!baseURL)
    return url;
  if (/^https?:\/\//.test(url)) {
    return url.replace(/^https?:\/\/[^/]+/, baseURL);
  }
  if (url.startsWith("//")) {
    return new URL(url, baseURL).toString();
  }
  if (url.startsWith("/")) {
    try {
      return new URL(url, baseURL).toString();
    } catch {
      return url;
    }
  }
  return url;
}
async function downloadBrandQRToTmp(url, kind, id, options = {}) {
  if (!url) {
    return { ok: false, reason: "no qr_png_url on plan" };
  }
  const stem = stableNameFor(kind, id ?? randomUUID5());
  const dirs = resolveIdeImageDirs();
  const canonical = dirs[0];
  if (!canonical) {
    return { ok: false, reason: "no IDE image directory resolved" };
  }
  try {
    mkdirSync5(canonical, { recursive: true });
  } catch (error) {
    return { ok: false, reason: `mkdir ${canonical} failed: ${error.message}` };
  }
  const fetchURL = resolveFetchURL(url, options.baseURL);
  try {
    const fetchFn = options.fetchImpl ?? globalThis.fetch;
    const detected = await detectImageFormat(fetchURL, fetchFn);
    const fileName = `${stem}${detected.ext}`;
    const filePath = join(canonical, fileName);
    atomicWrite(filePath, detected.body);
    const mirrors = mirrorToDirs(fileName, detected.body, dirs);
    return {
      ok: true,
      attach: {
        localPath: filePath,
        mirrors,
        mimeType: mimeFor(detected.ext),
        source: url,
        status: "downloaded",
        ...options.caption ? { caption: options.caption } : {},
        mustRenderReason: IDE_ATTACH_REASON
      }
    };
  } catch (error) {
    return { ok: false, reason: `brand image fetch failed: ${error.message}` };
  }
}
async function ensureIdeImageAttach(plan, options = {}) {
  if (plan.ideImageAttach) {
    if (plan.ideImageAttach.status === "downloaded" || plan.ideImageAttach.status === "disabled") {
      return;
    }
  }
  if (options.enabled === false) {
    plan.ideImageAttach = {
      localPath: "",
      mirrors: [],
      mimeType: "image/png",
      source: "",
      status: "disabled",
      mustRenderReason: IDE_ATTACH_REASON
    };
    return;
  }
  const pngURL = plan.preferredQRSources.find((src) => src.length > 0);
  if (!pngURL) {
    plan.ideImageAttach = {
      localPath: "",
      mirrors: [],
      mimeType: "image/png",
      source: "",
      status: "failed",
      mustRenderReason: IDE_ATTACH_REASON
    };
    return;
  }
  const kind = plan.kind === "payment_qr" ? "payment" : "checkout";
  const id = plan.paymentIntentID ?? plan.checkoutID;
  const caption = plan.kind === "payment_qr" ? "ItPay brand payment QR" : "ItPay checkout QR";
  const result = await downloadBrandQRToTmp(pngURL, kind, id, {
    ...options.fetchImpl ? { fetchImpl: options.fetchImpl } : {},
    ...options.baseURL ? { baseURL: options.baseURL } : {},
    caption
  });
  if (result.ok && result.attach) {
    plan.ideImageAttach = result.attach;
    return;
  }
  plan.ideImageAttach = {
    localPath: "",
    mirrors: [],
    mimeType: "image/png",
    source: pngURL,
    status: "failed",
    mustRenderReason: IDE_ATTACH_REASON,
    ...result.reason ? { error: result.reason } : {}
  };
}
function ideImageAttachBlock(attach) {
  const lines = [];
  if (attach.status === "downloaded" && attach.localPath) {
    lines.push("");
    lines.push("> [ATTACH] IDE image (must render)");
    lines.push(`> canonical: \`${attach.localPath}\``);
    if (attach.mirrors.length > 0) {
      lines.push(`> mirrors:`);
      for (const mirror of attach.mirrors) {
        lines.push(`>   - \`${mirror}\``);
      }
    }
  } else if (attach.status === "failed") {
    lines.push("");
    lines.push("> [ATTACH] IDE image MISSING \u2014 render is required but the brand image could not be downloaded");
    if (attach.error)
      lines.push(`> error: ${attach.error}`);
  } else if (attach.status === "disabled") {
    lines.push("");
    lines.push("> [ATTACH] IDE image attach disabled (ITPAY_IDE_IMAGE_ATTACH=0)");
  } else {
    lines.push("");
    lines.push("> [ATTACH] IDE image (must render)");
  }
  lines.push(`> source: ${attach.source}`);
  lines.push(`> mime:   ${attach.mimeType}`);
  if (attach.caption)
    lines.push(`> caption: ${attach.caption}`);
  lines.push(`> status: ${attach.status}`);
  lines.push(`> rule:   ${attach.mustRenderReason}`);
  lines.push("> action: agent must read the canonical local path (or any mirror) into the IDE chat window and wait for the human to confirm the image is visible. If the image does not appear in chat, the checkout is considered failed.");
  return lines;
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/render/terminal.js
import { copyFile } from "node:fs/promises";
async function renderTerminal(plan, options) {
  const out = options.output ?? ((line) => process.stdout.write(line));
  const isPayment = plan.kind === "payment_qr";
  out(`
${"\u2501".repeat(56)}
`);
  out(isPayment ? "  ITP \u5F85\u4ED8\u6B3E\n" : "  ITP \u6536\u94F6\u53F0\n");
  out(`${"\u2501".repeat(56)}

`);
  if (plan.orderItems && plan.orderItems.length > 0) {
    out("  \u8BA2\u5355\u8BE6\u60C5:\n");
    let total = 0;
    for (const item of plan.orderItems) {
      const price = fmtPrice(item.amountMinor, item.currency);
      const lineTotal = item.amountMinor * item.quantity;
      total += lineTotal;
      out(`    ${item.title}  \xD7${item.quantity}  ${price}
`);
    }
    out(`    ${"\u2500".repeat(40)}
`);
    out(`    \u5408\u8BA1: ${fmtPrice(total, plan.orderCurrency ?? "CNY")}

`);
  }
  if (isPayment) {
    out(`  \u652F\u4ED8\u65B9\u5F0F: ${plan.paymentMethod ?? "\u2014"}  \u72B6\u6001: ${plan.paymentStatus ?? "\u2014"}
`);
    if (plan.paymentIntentID)
      out(`  \u652F\u4ED8 ID:   ${plan.paymentIntentID}
`);
    out("\n");
  }
  out(`  Checkout:   ${plan.checkoutID ?? "\u2014"}
`);
  out(`  URL:        ${plan.url}
`);
  for (const link of plan.platform.links) {
    out(`  ${link.label}: ${link.url}
`);
  }
  out("\n");
  await downloadServerQR(plan, options, out);
  try {
    const ascii = await renderTerminalQR(plan.url, options.format);
    out(ascii + "\n");
  } catch {
    out("  [QR render failed]\n\n");
  }
  for (const interaction of plan.platform.interactions ?? []) {
    await renderTerminalInteraction(interaction, options);
  }
  if (plan.afterActionCommand) {
    out(`
  ${plan.afterActionLabel ?? "Next step:"}
`);
    out(`  ${plan.afterActionCommand}
`);
  }
  if (plan.ideImageAttach) {
    out("\n  \u2500\u2500 IDE \u56FE\u7247\u56DE\u663E\uFF08\u5FC5\u987B\u6267\u884C\uFF09 \u2500\u2500\n");
    for (const line of ideImageAttachBlock(plan.ideImageAttach)) {
      if (line === "") {
        out("\n");
      } else {
        out(`  ${line.replace(/^> ?/, "")}
`);
      }
    }
  }
  out(`
${"\u2501".repeat(56)}
`);
}
async function downloadServerQR(plan, options, out) {
  const attach = plan.ideImageAttach;
  if (attach && attach.status === "downloaded" && attach.localPath) {
    out(`  Branded QR:  ${attach.localPath}
`);
    if (attach.mirrors.length > 0) {
      out(`  QR mirrors:  ${attach.mirrors.join(", ")}
`);
    }
    out(`  QR PNG URL:  ${attach.source}
`);
    out(`  Attach status: ${attach.status}
`);
    const target = options.qrFilePath ?? attach.localPath;
    if (options.isTTY) {
      renderInlineTerminalImage(target, out);
    }
    return;
  }
  if (attach && attach.status === "failed") {
    out(`  Branded QR:  MISSING (${attach.error ?? "unknown error"})
`);
  }
  if (attach && attach.status === "disabled") {
    out(`  Branded QR:  disabled (ITPAY_IDE_IMAGE_ATTACH=0)
`);
  }
  try {
    const localPNG = await writeLocalPNG(plan.url);
    const filePath = options.qrFilePath ?? localPNG.filePath;
    if (options.qrFilePath) {
      await copyFile(localPNG.filePath, filePath);
    }
    out(`  QR file:     ${filePath}
`);
    if (options.isTTY) {
      renderInlineTerminalImage(filePath, out);
    }
  } catch {
  }
}
async function renderTerminalInteraction(request, options) {
  const out = options.output ?? ((line) => process.stdout.write(line));
  out(`
ITP INPUT REQUIRED [${request.kind}]
`);
  out(`  title:       ${request.title}
`);
  out(`  prompt:      ${request.prompt}
`);
  if (request.kind === "input") {
    for (const field of request.fields) {
      out(`  field:       ${field.id} (${field.inputType}${field.required ? " required" : ""}) - ${field.label}
`);
      if (field.placeholder)
        out(`  placeholder: ${field.placeholder}
`);
      if (field.description)
        out(`  note:        ${field.description}
`);
    }
    out(`  reply_json:  ${JSON.stringify(buildInputTemplate(request.fields))}
`);
    return;
  }
  out(`  select:      ${request.selectionMode ?? "single"}
`);
  request.options.forEach((option, index) => {
    out(`  [${index + 1}] ${option.label} -> ${option.value}
`);
    if (option.description)
      out(`      ${option.description}
`);
  });
  out(`  reply_hint:  reply with option id(s) for request ${request.id}
`);
}
function buildInputTemplate(fields) {
  return Object.fromEntries(fields.map((field) => [field.id, `<${field.inputType}>`]));
}
function fmtPrice(amountMinor, currency) {
  return `${(amountMinor / 100).toFixed(2)} ${currency}`;
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/render/markdown.js
function renderMarkdown(plan, options = {}) {
  const out = options.output ?? ((line) => process.stdout.write(line + "\n"));
  const handoff = buildAgentChatHandoff(plan);
  out(`> AGENT ACTION REQUIRED: ${handoff.instruction}

${handoff.markdown}`);
}
function buildAgentChatHandoff(plan) {
  const lines = ["### ItPay \u4ED8\u6B3E"];
  const attach = plan.ideImageAttach;
  if (attach?.status === "downloaded" && attach.localPath) {
    lines.push("", `![ItPay \u4ED8\u6B3E\u4E8C\u7EF4\u7801](<${attach.localPath}>)`);
  } else {
    lines.push("", `> \u4E8C\u7EF4\u7801\u6682\u4E0D\u53EF\u7528\uFF1A${attach?.error ?? attach?.status ?? "not prepared"}`);
  }
  const paymentLink = plan.platform.links[0]?.url;
  if (paymentLink)
    lines.push("", `[\u6253\u5F00 ItPay \u4ED8\u6B3E\u9875\u9762](${paymentLink})`);
  const totalMinor = plan.orderItems?.reduce((sum, item) => sum + item.amountMinor * item.quantity, 0) ?? 0;
  lines.push("", `\u91D1\u989D\uFF1A**${formatPrice(totalMinor, plan.orderCurrency ?? "CNY")}**`);
  if (plan.orderItems?.length) {
    lines.push(`\u9879\u76EE\uFF1A${plan.orderItems.map((item) => `${item.title} x${item.quantity}`).join("\u3001")}`);
  }
  if (plan.afterActionCommand) {
    lines.push("", `\u4ED8\u6B3E\u540E\u67E5\u8BE2\uFF1A\`${plan.afterActionCommand}\``);
  }
  return {
    type: "send_payment_handoff",
    must_send_to_user: true,
    instruction: "\u628A\u4E0B\u9762\u7684 Markdown \u539F\u6837\u53D1\u9001\u5230\u5F53\u524D\u804A\u5929\uFF1B\u4E8C\u7EF4\u7801\u548C\u4ED8\u6B3E\u94FE\u63A5\u90FD\u5BF9\u7528\u6237\u53EF\u89C1\u540E\uFF0C\u624D\u80FD\u7B49\u5F85\u4ED8\u6B3E\u3002\u4E0D\u8981\u53EA\u5C55\u793A\u5DE5\u5177\u8C03\u7528\u6216\u6587\u4EF6\u8DEF\u5F84\u3002",
    markdown: lines.join("\n"),
    ...plan.afterActionCommand ? { after_visible_action: { command: plan.afterActionCommand } } : {}
  };
}
function formatPrice(amountMinor, currency) {
  return `${(amountMinor / 100).toFixed(2)} ${currency}`;
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/render/plain_chat.js
function renderPlainChat(plan, options = {}) {
  const out = options.output ?? ((line) => process.stdout.write(line));
  if (plan.linkOnlyURL) {
    out(`${plan.summary}
open: ${plan.linkOnlyURL}
`);
    return;
  }
  const brand = plan.preferredQRSources.find((src) => src.length > 0);
  const lines = [];
  lines.push(plan.summary);
  if (plan.checkoutID)
    lines.push(`checkout_id: ${plan.checkoutID}`);
  if (plan.paymentIntentID)
    lines.push(`payment_intent_id: ${plan.paymentIntentID}`);
  lines.push(`open: ${plan.url}`);
  if (brand)
    lines.push(`qr_image: ${brand}`);
  if (plan.mobileWalletURL)
    lines.push(`wallet: ${plan.mobileWalletURL}`);
  for (const media of plan.platform.media ?? []) {
    lines.push(`image: ${media.url}`);
  }
  for (const link of plan.platform.links) {
    lines.push(`- ${link.label}: ${link.url}`);
  }
  for (const interaction of plan.platform.interactions ?? []) {
    lines.push("");
    lines.push(renderInteractionText(interaction));
  }
  if (plan.ideImageAttach) {
    lines.push("");
    for (const line of ideImageAttachBlock(plan.ideImageAttach)) {
      lines.push(line);
    }
  }
  out(lines.join("\n") + "\n");
}
function renderInteractionText(request) {
  const lines = [`${request.title}`, request.prompt];
  for (const media of request.media ?? []) {
    lines.push(`image: ${media.url}`);
  }
  if (request.kind === "input") {
    for (const field of request.fields) {
      lines.push(`field ${field.id}: ${field.label} (${field.inputType}${field.required ? ", required" : ""})`);
    }
    lines.push(`reply_json: ${JSON.stringify(Object.fromEntries(request.fields.map((field) => [field.id, `<${field.inputType}>`])))}`);
    return lines.join("\n");
  }
  lines.push(`selection_mode: ${request.selectionMode ?? "single"}`);
  request.options.forEach((option, index) => {
    lines.push(`${index + 1}. ${option.label} [${option.id}] => ${option.value}`);
  });
  return lines.join("\n");
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/render/telegram.js
function buttonsFor(plan) {
  if (plan.kind === "payment_qr" && plan.paymentIntentID) {
    return [
      { label: "\u652F\u4ED8\u9047\u5230\u95EE\u9898 / \u5237\u65B0", kind: "callback", intent: "refresh_payment_qr", ref: plan.paymentIntentID },
      { label: "\u6211\u5DF2\u4ED8\u6B3E\uFF0C\u67E5\u8BE2\u72B6\u6001", kind: "callback", intent: "check_payment_status", ref: plan.paymentIntentID }
    ];
  }
  if (plan.kind === "auth_qr" && plan.checkoutID) {
    return [
      { label: "\u6253\u5F00\u6388\u6743\u9875\u9762", kind: "url", url: plan.url },
      { label: "\u67E5\u8BE2\u6388\u6743\u72B6\u6001", kind: "callback", intent: "check_checkout_status", ref: plan.checkoutID }
    ];
  }
  return [
    { label: "\u{1F4F1} \u624B\u673A\u70B9\u8FD9\u513F\u652F\u4ED8", kind: "url", url: plan.url },
    ...plan.checkoutID ? [{ label: "\u{1F4CB} \u5DF2\u6388\u6743\u7ED9\u6211\u8BFB", kind: "callback", intent: "grant_confirmed", ref: plan.checkoutID }] : []
  ];
}
function nativeButton(button) {
  if (button.kind === "url") {
    return { label: button.label, url: button.url ?? "" };
  }
  const value = button.intent === "check_checkout_status" ? `itp:checkout:${button.ref ?? ""}` : `itp:${button.intent ?? "callback"}:${button.ref ?? ""}`;
  return { label: button.label, value };
}
function renderTelegram(plan, options) {
  const out = options.output ?? ((line) => process.stdout.write(line));
  const agentAction = buildOpenClawTelegramAction(plan, options.target);
  const presentation = agentAction.arguments.presentation;
  const media = collectTelegramMedia(plan);
  const text = agentAction.arguments.message;
  const openclawMessage = {
    command: [
      "openclaw",
      "message",
      "send",
      "--channel",
      "telegram",
      "--target",
      options.target,
      "--message",
      text,
      ...media.length > 0 ? ["--media", media[0].url] : [],
      "--presentation",
      JSON.stringify(presentation)
    ],
    // Keep the same Checkout visible if native buttons are unavailable.
    if_unavailable: "If `openclaw message send` is unavailable, send the same QR media and Checkout URL as ordinary Telegram content, report that inline buttons are unavailable, and stop. Do not create another Checkout."
  };
  out(JSON.stringify({ presentation, agent_action: agentAction, openclaw_message: openclawMessage }, null, 2) + "\n");
}
function buildOpenClawTelegramAction(plan, target) {
  const buttons = buttonsFor(plan).map(nativeButton);
  const media = collectTelegramMedia(plan);
  const message = plan.kind === "payment_qr" ? `ItPay payment QR \u2014 ${plan.summary}` : plan.kind === "auth_qr" ? `ItPay auth required \u2014 ${plan.summary}` : `ItPay checkout QR \u2014 ${plan.summary}`;
  const presentation = {
    blocks: [{ type: "buttons", buttons }]
  };
  const nativeTarget = target.trim().replace(/^telegram:/i, "");
  return {
    tool: "message",
    arguments: {
      action: "send",
      channel: "telegram",
      target: nativeTarget,
      message,
      ...media[0]?.url ? { media: media[0].url } : {},
      presentation
    }
  };
}
function collectTelegramMedia(plan) {
  const media = (plan.platform.media ?? []).map((item) => ({
    url: item.url,
    mimeType: item.mimeType ?? "image/png"
  }));
  if (plan.kind === "payment_qr" || media.length === 0) {
    media.unshift({
      url: plan.preferredQRSources.find((src) => src.length > 0) ?? plan.url,
      mimeType: "image/png"
    });
  }
  return media;
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/render/feishu.js
function actionFor(plan, button) {
  if (button.kind === "url" && button.url) {
    return {
      tag: "action",
      actions: [
        {
          tag: "button",
          text: { tag: "plain_text", content: button.label },
          type: "primary",
          url: button.url
        }
      ]
    };
  }
  return {
    tag: "action",
    actions: [
      {
        tag: "button",
        text: { tag: "plain_text", content: button.label },
        type: "default",
        value: {
          intent: button.intent ?? "noop",
          ref: button.ref ?? "",
          checkout_id: plan.checkoutID ?? "",
          payment_intent_id: plan.paymentIntentID ?? ""
        }
      }
    ]
  };
}
function buttonsFor2(plan) {
  if (plan.kind === "payment_qr" && plan.paymentIntentID) {
    return [
      { label: "\u652F\u4ED8\u9047\u5230\u95EE\u9898 / \u5237\u65B0", kind: "callback", intent: "refresh_payment_qr", ref: plan.paymentIntentID },
      { label: "\u6211\u5DF2\u4ED8\u6B3E\uFF0C\u67E5\u8BE2\u72B6\u6001", kind: "callback", intent: "check_payment_status", ref: plan.paymentIntentID }
    ];
  }
  if (plan.kind === "auth_qr" && plan.checkoutID) {
    return [
      { label: "\u6253\u5F00\u6388\u6743\u9875\u9762", kind: "url", url: plan.url },
      { label: "\u67E5\u8BE2\u6388\u6743\u72B6\u6001", kind: "callback", intent: "check_checkout_status", ref: plan.checkoutID }
    ];
  }
  return [
    { label: "\u6253\u5F00 ItPay \u6536\u94F6\u53F0", kind: "url", url: plan.url },
    ...plan.checkoutID ? [{ label: "\u67E5\u8BE2 Checkout \u72B6\u6001", kind: "callback", intent: "check_checkout_status", ref: plan.checkoutID }] : []
  ];
}
function renderFeishu(plan, options) {
  const out = options.output ?? ((line) => process.stdout.write(line));
  const host = options.host ?? "feishu";
  const buttons = buttonsFor2(plan);
  const media = collectFeishuMedia(plan);
  const title = plan.kind === "payment_qr" ? "ItPay \u652F\u4ED8\u4E8C\u7EF4\u7801" : plan.kind === "auth_qr" ? "ItPay \u9700\u8981\u4E70\u5BB6\u6388\u6743" : "ItPay Checkout \u4E8C\u7EF4\u7801";
  const card = {
    config: { wide_screen_mode: true },
    header: {
      template: "blue",
      title: { tag: "plain_text", content: title }
    },
    elements: [
      {
        tag: "div",
        text: { tag: "plain_text", content: plan.summary }
      },
      ...media.map((item) => ({
        tag: "img",
        img_key: item.url,
        alt: { tag: "plain_text", content: item.alt ?? item.label ?? `${title} (image)` }
      })),
      {
        tag: "note",
        elements: [
          { tag: "plain_text", content: `checkout_id: ${plan.checkoutID ?? "-"}` }
        ]
      },
      ...buttons.map((button) => actionFor(plan, button))
    ]
  };
  const message = {
    host,
    target: options.target,
    receive_id_type: host === "lark" ? "open_id" : "chat_id",
    msg_type: "interactive",
    card,
    ...plan.ideImageAttach ? {
      ide_image_attach: {
        status: plan.ideImageAttach.status,
        local_path: plan.ideImageAttach.localPath,
        mirrors: plan.ideImageAttach.mirrors,
        mime_type: plan.ideImageAttach.mimeType,
        source: plan.ideImageAttach.source,
        ...plan.ideImageAttach.caption ? { caption: plan.ideImageAttach.caption } : {},
        must_render_reason: plan.ideImageAttach.mustRenderReason,
        ...plan.ideImageAttach.error ? { error: plan.ideImageAttach.error } : {},
        action: "agent_must_render_into_ide_chat",
        instructions: ideImageAttachBlock(plan.ideImageAttach).filter((l) => l.length > 0)
      }
    } : {}
  };
  out(JSON.stringify({ message }, null, 2) + "\n");
}
function collectFeishuMedia(plan) {
  const media = [...plan.platform.media ?? []];
  const brand = plan.preferredQRSources.find((src) => src.length > 0);
  if (brand) {
    media.unshift({ url: brand, label: "QR image", alt: "ItPay QR" });
  }
  return media;
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/render/plan.js
function platformKeyForHost(host) {
  switch (host) {
    case "terminal":
      return "terminal";
    case "codex":
    case "claude-code":
      return "markdown";
    case "telegram":
      return "telegram";
    case "feishu":
      return "feishu";
    case "lark":
      return "lark";
    case "discord":
    case "whatsapp":
    case "plain-chat":
    default:
      return "plain_chat";
  }
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/render/index.js
async function dispatchRender(plan, options) {
  const key = platformKeyForHost(plan.host);
  if (key === "markdown" || key === "terminal") {
    await ensureIdeImageAttach(plan, options);
  }
  switch (key) {
    case "terminal": {
      const terminalOptions = {
        format: options.qrFormat ?? "terminal",
        isTTY: options.isTTY ?? Boolean(process.stdout.isTTY),
        ...options.asciiWidth ? { asciiWidth: options.asciiWidth } : {},
        ...options.fetchImpl ? { fetchImpl: options.fetchImpl } : {},
        ...options.qrFilePath ? { qrFilePath: options.qrFilePath } : {},
        ...options.output ? { output: options.output } : {},
        ...options.baseURL ? { baseURL: options.baseURL } : {}
      };
      await renderTerminal(plan, terminalOptions);
      return;
    }
    case "markdown":
      renderMarkdown(plan, options.output ? { output: options.output } : {});
      return;
    case "telegram":
      if (!options.target) {
        throw new Error(`--target is required for host ${plan.host}`);
      }
      renderTelegram(plan, {
        target: options.target,
        ...options.output ? { output: options.output } : {}
      });
      return;
    case "feishu":
    case "lark":
      if (!options.target) {
        throw new Error(`--target is required for host ${plan.host}`);
      }
      renderFeishu(plan, {
        target: options.target,
        host: key,
        ...options.output ? { output: options.output } : {}
      });
      return;
    case "plain_chat":
    default:
      renderPlainChat(plan, options.output ? { output: options.output } : {});
      return;
  }
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/render/locale.js
function normalizeCardLocale(value) {
  switch (value?.trim().toLowerCase()) {
    case void 0:
    case "":
    case "zh":
    case "zh-cn":
    case "zh_cn":
    case "cn":
      return "zh-CN";
    case "en":
    case "en-us":
    case "en_us":
      return "en";
    default:
      throw new Error(`unsupported card locale: ${value}; expected zh-CN or en`);
  }
}
function localizeCardURL(value, locale) {
  try {
    const parsed = new URL(value);
    parsed.searchParams.set("locale", locale);
    return parsed.toString();
  } catch {
    return value;
  }
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/render/output.js
function formatMoney(amountMinor, currency) {
  const major = (amountMinor / 100).toFixed(2);
  return `${major} ${currency}`;
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/commands/checkout_handoff.js
function shouldPrepareLocalCheckoutImage(platform) {
  return platform === "markdown";
}
function isWorkBuddyPlainChat(agentType, platform) {
  return agentType?.trim().toLowerCase() === "workbuddy" && platform === "plain_chat";
}
function buildCheckoutHandoff(input) {
  const handoff = { url: input.url };
  const workBuddyLinkOnly = isWorkBuddyPlainChat(input.agentType, input.platform);
  if (input.platform === "markdown") {
    if (input.localPath)
      handoff.qr_local_path = input.localPath;
    if (input.markdown)
      handoff.markdown = input.markdown;
  } else if (input.platform === "plain_chat" && input.qrImageURL && !workBuddyLinkOnly) {
    handoff.qr_image_url = input.qrImageURL;
  } else if (input.platform === "telegram" && input.qrImageURL) {
    handoff.qr_image_url = input.qrImageURL;
  }
  if (input.agentType?.trim().toLowerCase() === "openclaw" && input.platform === "telegram" && input.plan && input.target) {
    handoff.agent_action = buildOpenClawTelegramAction(input.plan, input.target);
  }
  return {
    handoff,
    instruction: checkoutHandoffInstruction(input.agentType, input.platform, input.amount)
  };
}
function checkoutHandoffInstruction(agentType, platform, amount) {
  if (isWorkBuddyPlainChat(agentType, platform)) {
    return `Backend \u5C1A\u672A\u786E\u8BA4\u4ED8\u6B3E\u3002\u5411\u7528\u6237\u8BF4\u660E\u91D1\u989D ${amount}\uFF0C\u76F4\u63A5\u53D1\u9001\u5E76\u6253\u5F00 handoff.url\uFF0C\u7136\u540E\u505C\u6B62\u7B49\u5F85\u3002\u4E0D\u8981\u8C03\u7528 present_files\uFF0C\u4E0D\u8981\u68C0\u67E5\u672C\u5730\u6587\u4EF6\uFF0C\u4E0D\u8981\u4E0B\u8F7D\u6216\u91CD\u5EFA\u4E8C\u7EF4\u7801\uFF0C\u4E0D\u8981\u8C03\u7528 pay\uFF0C\u4E0D\u8981\u521B\u5EFA\u65B0 Checkout\u3001Payment Intent \u6216 Execution\u3002\u53EA\u6709\u7528\u6237\u660E\u786E\u8868\u793A\u5DF2\u4ED8\u6B3E\u6216\u8981\u6C42\u67E5\u8BE2\u72B6\u6001\u65F6\uFF0C\u624D\u6267\u884C next.command\uFF1B\u7528\u6237\u7684\u8BDD\u4E0D\u662F\u4ED8\u6B3E\u6210\u529F\u8BC1\u660E\u3002`;
  }
  if (platform === "markdown") {
    return `Backend \u5C1A\u672A\u786E\u8BA4\u4ED8\u6B3E\u3002\u628A handoff.markdown \u539F\u6837\u53D1\u9001\u5230\u5F53\u524D\u684C\u9762\u5BF9\u8BDD\uFF0C\u786E\u8BA4\u4E8C\u7EF4\u7801\u3001\u4ED8\u6B3E\u94FE\u63A5\u548C\u91D1\u989D ${amount} \u5747\u5DF2\u5B9E\u9645\u5BF9\u7528\u6237\u53EF\u89C1\uFF0C\u7136\u540E\u505C\u6B62\u7B49\u5F85\u3002\u4E0D\u8981\u521B\u5EFA\u65B0 Checkout\u3001Payment Intent \u6216 Execution\uFF1B\u53EA\u6709\u7528\u6237\u660E\u786E\u8868\u793A\u5DF2\u4ED8\u6B3E\u6216\u8981\u6C42\u67E5\u8BE2\u72B6\u6001\u65F6\uFF0C\u624D\u6267\u884C next.command\uFF1B\u7528\u6237\u7684\u8BDD\u4E0D\u662F\u4ED8\u6B3E\u6210\u529F\u8BC1\u660E\u3002`;
  }
  if (platform === "terminal") {
    return `Backend \u5C1A\u672A\u786E\u8BA4\u4ED8\u6B3E\u3002\u5728\u7528\u6237\u53EF\u89C1\u7EC8\u7AEF\u5C55\u793A\u5F53\u524D Checkout \u7684\u4E8C\u7EF4\u7801\u3001handoff.url \u548C\u91D1\u989D ${amount}\uFF0C\u7136\u540E\u505C\u6B62\u7B49\u5F85\u3002\u4E0D\u8981\u521B\u5EFA\u65B0 Checkout\u3001Payment Intent \u6216 Execution\uFF1B\u53EA\u6709\u7528\u6237\u660E\u786E\u8868\u793A\u5DF2\u4ED8\u6B3E\u6216\u8981\u6C42\u67E5\u8BE2\u72B6\u6001\u65F6\uFF0C\u624D\u6267\u884C next.command\uFF1B\u7528\u6237\u7684\u8BDD\u4E0D\u662F\u4ED8\u6B3E\u6210\u529F\u8BC1\u660E\u3002`;
  }
  if (agentType?.trim().toLowerCase() === "openclaw" && platform === "telegram") {
    return `Backend \u5C1A\u672A\u786E\u8BA4\u4ED8\u6B3E\u6216\u6388\u6743\u72B6\u6001\u3002\u7ACB\u5373\u4F7F\u7528 OpenClaw \u539F\u751F message tool\uFF0C\u4E25\u683C\u6309 handoff.agent_action.tool \u548C handoff.agent_action.arguments \u539F\u6837\u6267\u884C\uFF1B\u5B83\u4F1A\u53D1\u9001\u91D1\u989D ${amount}\u3001\u4E8C\u7EF4\u7801\u3001\u{1F4F1} \u624B\u673A\u70B9\u8FD9\u513F\u652F\u4ED8\u548C \u{1F4CB} \u5DF2\u6388\u6743\u7ED9\u6211\u8BFB\u3002\u4E0D\u5F97\u6539\u5199 presentation\u3001\u6362\u7528\u5176\u4ED6\u6D88\u606F\u5DE5\u5177\u3001\u62C6\u5F00\u6309\u94AE\u53D1\u9001\u6216\u7528\u666E\u901A\u56DE\u590D\u58F0\u79F0\u6309\u94AE\u5DF2\u7ECF\u53D1\u9001\u3002\u786E\u8BA4 message tool \u8C03\u7528\u6210\u529F\u540E\u505C\u6B62\u7B49\u5F85\u3002\u6536\u5230 callback_data "itp:grant_confirmed:<checkout_id>" \u65F6\uFF0C\u8868\u793A\u7528\u6237\u58F0\u660E\u5DF2\u5728\u6536\u94F6\u53F0\u6388\u6743\u8BFB\u53D6\uFF1B\u7ACB\u5373\u6267\u884C next.command \u67E5\u8BE2\u540C\u4E00 Checkout\uFF0C\u518D\u53EA\u6267\u884C Backend \u8FD4\u56DE\u7684 next.command \u8FDB\u5165\u540C\u4E00 Execution \u7684 grant \u6D41\u7A0B\u3002\u8BE5 callback \u4E0D\u8BC1\u660E\u4ED8\u6B3E\u6210\u529F\u6216 grant \u5DF2\u751F\u6548\uFF1BBackend \u672A\u8FD4\u56DE grant_active \u524D\u4E0D\u5F97\u8BFB\u53D6\u6216\u731C\u6D4B\u7ED3\u679C\u3002\u82E5\u539F\u751F message tool \u660E\u786E\u5931\u8D25\u6216\u5F53\u524D Telegram \u672A\u542F\u7528 inline buttons\uFF0C\u53EA\u53D1\u9001\u73B0\u6709 handoff.qr_image_url\u3001\u91D1\u989D\u548C handoff.url\uFF0C\u62A5\u544A\u6309\u94AE\u4E0D\u53EF\u7528\u5E76\u505C\u6B62\uFF1B\u4E0D\u8981\u521B\u5EFA\u65B0\u7684 Checkout\u3001Payment Intent \u6216 Execution\u3002`;
  }
  return `Backend \u5C1A\u672A\u786E\u8BA4\u4ED8\u6B3E\u3002\u628A handoff.url \u548C\u53EF\u7528\u7684 handoff.qr_image_url \u5B9E\u9645\u53D1\u9001\u5230\u5F53\u524D\u4F1A\u8BDD\uFF0C\u8BF4\u660E\u91D1\u989D ${amount}\uFF0C\u7136\u540E\u505C\u6B62\u7B49\u5F85\u3002\u4E0D\u8981\u521B\u5EFA\u65B0 Checkout\u3001Payment Intent \u6216 Execution\uFF1B\u53EA\u6709\u7528\u6237\u660E\u786E\u8868\u793A\u5DF2\u4ED8\u6B3E\u6216\u8981\u6C42\u67E5\u8BE2\u72B6\u6001\u65F6\uFF0C\u624D\u6267\u884C next.command\uFF1B\u7528\u6237\u7684\u8BDD\u4E0D\u662F\u4ED8\u6B3E\u6210\u529F\u8BC1\u660E\u3002`;
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/commands/buy.js
async function runBuy(backend, config, options) {
  const err = validateContext(options.host, options.target);
  if (err) {
    throw new Error(`${err.code}: ${err.message}`);
  }
  const snap = options.cartSession.show();
  const resumableCartID = !options.cartID && snap.items.length === 0 ? snap.lastCartID : void 0;
  if (!options.cartID && !resumableCartID && snap.items.length === 0) {
    throw new CommandContractError("cart_empty", "no local draft or canonical cart is available", "\u6CA1\u6709\u53EF\u8D2D\u4E70\u7684\u666E\u901A Cart\uFF1B\u4ECE\u5DF2\u53D1\u5E03\u76EE\u5F55\u9009\u62E9\u9879\u76EE\uFF0C\u4E0D\u8981\u731C\u6D4B item\u3001variant \u6216 offer\u3002", [{ command: "itpay catalog list --json", reason: "\u8BFB\u53D6\u5DF2\u53D1\u5E03\u9879\u76EE" }]);
  }
  const missingContactFields = findMissingContactFields(options.contact, options.requiredContactFields ?? []);
  if (missingContactFields.length > 0) {
    throw new CommandContractError("missing_contact", `missing required contact fields: ${missingContactFields.join(", ")}`, `\u5411\u7528\u6237\u8BE2\u95EE ${missingContactFields.join(" \u548C ")}\uFF0C\u7136\u540E\u5728\u540C\u4E00 buy \u547D\u4EE4\u8865\u5145\u5BF9\u5E94 contact \u53C2\u6570\uFF1B\u7981\u6B62\u7F16\u9020\u3002`, [{ command: "itpay buy --help", reason: "\u67E5\u770B contact \u53C2\u6570" }]);
  }
  let cart2;
  if (options.cartID || resumableCartID) {
    cart2 = await backend.getCart(options.cartID ?? resumableCartID);
  } else {
    const request = options.cartSession.toCreateCartRequest();
    request.client_context = {
      host: options.host,
      target: options.target
    };
    cart2 = await backend.createCart(request);
  }
  const latestLine = cart2.items[cart2.items.length - 1];
  options.cartSession.rememberServerCart({
    cartID: cart2.cart_id,
    ...latestLine?.cart_item_id ? { cartItemID: latestLine.cart_item_id } : {},
    ...latestLine?.service_execution_id ? { serviceExecutionID: latestLine.service_execution_id } : {}
  });
  const unquotedServiceLine = cart2.items.find((item) => item.service_execution_id && !item.service_quote_lock_id);
  if (unquotedServiceLine?.service_execution_id) {
    throw new CommandContractError("service_quote_required", `cart ${cart2.cart_id} contains an unquoted service-backed line`, "\u8BE5\u670D\u52A1\u9879\u76EE\u5C1A\u672A\u7ED1\u5B9A Quote Lock\uFF1B\u56DE\u5230\u6765\u6E90 Execution \u5B8C\u6210\u5019\u9009\u9009\u62E9\u548C\u62A5\u4EF7\u3002", [{ command: `itpay services next ${unquotedServiceLine.service_execution_id} --json`, reason: "\u8BFB\u53D6\u5F53\u524D\u5408\u6CD5\u52A8\u4F5C" }]);
  }
  const idempotencyKey = await operationID(config, `checkout.create:${cart2.cart_id}`);
  const checkoutRequest = {
    cart_id: cart2.cart_id,
    client_reference_id: options.clientReferenceID ?? idempotencyKey,
    ...options.contact ? { delivery_contact: options.contact } : {}
  };
  const checkout = await backend.createCheckout(checkoutRequest, idempotencyKey);
  options.cartSession.rememberCheckout({
    checkoutID: checkout.checkout.checkout_id,
    displayToken: checkout.display_token,
    checkoutURL: tokenizedCheckoutURL(checkout.checkout_url, checkout.display_token, checkout.qr_payload)
  });
  const checkoutID = checkout.checkout.checkout_id;
  const displayToken = checkout.display_token;
  const locale = normalizeCardLocale(options.locale);
  const checkoutURL = tokenizedCheckoutURL(checkout.checkout_url, displayToken, checkout.qr_payload);
  const cardURL = localizeCardURL(absolutePublicURL(config.baseURL, checkout.card_url ?? fallbackCardURL(config.baseURL, checkoutID, displayToken)), locale);
  const qrPNGURL = localizeCardURL(absolutePublicURL(config.baseURL, checkout.card_png_url ?? checkout.qr_png_url ?? fallbackCardPNGURL(config.baseURL, checkoutID, displayToken)), locale);
  const orderItems = cart2.items.map((item) => ({
    title: item.title,
    quantity: item.quantity,
    amountMinor: item.amount_minor,
    currency: item.currency
  }));
  let paymentIntent;
  let waitStatus = "skipped";
  if (options.pay) {
    const method = options.payMethod ?? "alipay";
    paymentIntent = await backend.createPaymentIntent(checkoutID, { payment_method_type: method, display_token: displayToken });
    if (!options.jsonOutput) {
      process.stdout.write("\n--- payment intent ---\n");
      process.stdout.write(`  id:     ${paymentIntent.payment_intent_id}
`);
      process.stdout.write(`  method: ${paymentIntent.payment_method_type}
`);
      process.stdout.write(`  status: ${paymentIntent.status}
`);
      if (paymentIntent.action?.qr_image_url) {
        process.stdout.write(`  qr:     ${paymentIntent.action.qr_image_url}
`);
      }
      if (paymentIntent.action?.mobile_wallet_url) {
        process.stdout.write(`  wallet: ${paymentIntent.action.mobile_wallet_url}
`);
      }
    }
    if (!options.noWait) {
      waitStatus = await waitForPaymentSSE(backend, checkoutID, displayToken, options.payTimeoutSec ?? 120);
      if (!options.jsonOutput) {
        process.stdout.write(`  wait:    ${waitStatus}
`);
      }
    }
  }
  const planInput = {
    host: options.host,
    checkoutID,
    checkoutURL,
    cardURL,
    displayToken,
    qrPayload: checkout.qr_payload,
    nextAction: checkout.checkout.next_action,
    orderItems,
    orderCurrency: checkout.checkout.currency,
    ...options.agentType ? { agentType: options.agentType } : {},
    locale
  };
  if (qrPNGURL)
    planInput.qrPNGURL = qrPNGURL;
  if (paymentIntent) {
    planInput.paymentIntentID = paymentIntent.payment_intent_id;
    planInput.paymentMethod = paymentIntent.payment_method_type;
    planInput.paymentStatus = paymentIntent.status;
  }
  const plan = buildCheckoutQRPlan(planInput);
  if (shouldPrepareLocalCheckoutImage(platformKeyForHost(options.host))) {
    await ensureIdeImageAttach(plan, {
      enabled: config.ideImageAttach,
      ...config.baseURL ? { baseURL: config.baseURL } : {},
      ...options.fetchImpl ? { fetchImpl: options.fetchImpl } : {}
    });
  }
  if (options.jsonOutput) {
    const envelope = buildBuyEnvelope({
      cart: cart2,
      checkoutID,
      checkoutURL,
      displayToken,
      plan,
      waitStatus,
      qrPNGURL,
      ...paymentIntent ? { paymentIntent } : {},
      ...options.agentType ? { agentType: options.agentType } : {},
      ...options.target ? { target: options.target } : {}
    });
    writeCommandEnvelope(envelope, { jsonOutput: true, ...options.output ? { output: options.output } : {} });
    return {
      kind: "checkout_rendered",
      plan,
      checkoutID,
      displayToken,
      envelope
    };
  }
  const renderOptions = {
    host: options.host,
    isTTY: options.isTTY ?? Boolean(process.stdout.isTTY),
    ...options.target ? { target: options.target } : {},
    ...options.qrFormat ? { qrFormat: options.qrFormat } : {},
    ...options.qrFilePath ? { qrFilePath: options.qrFilePath } : {},
    ...options.output ? { output: options.output } : {},
    ...options.fetchImpl ? { fetchImpl: options.fetchImpl } : {},
    baseURL: config.baseURL
  };
  await dispatchRender(plan, renderOptions);
  return {
    kind: "checkout_rendered",
    plan,
    checkoutID,
    displayToken
  };
}
function buildBuyEnvelope(input) {
  const verified = input.waitStatus === "verified";
  const platform = platformKeyForHost(input.plan.host);
  const amount = formatMoney(input.cart.amount_minor, input.cart.currency);
  const result = {
    checkout_id: input.checkoutID,
    payment: verified ? "verified" : "pending",
    amount,
    item_count: input.cart.items.length,
    ...input.paymentIntent ? {
      payment_intent_id: input.paymentIntent.payment_intent_id,
      payment_intent_status: input.paymentIntent.status
    } : {},
    ...input.waitStatus === "timeout" ? { wait_status: "timeout" } : {}
  };
  if (verified) {
    return {
      status: "payment_event_observed",
      result,
      instruction: "\u5DF2\u89C2\u5BDF\u5230\u4ED8\u6B3E\u786E\u8BA4\u4E8B\u4EF6\uFF1B\u8BFB\u53D6\u540C\u4E00 Checkout \u7684\u6743\u5A01\u5B8C\u6210\u72B6\u6001\uFF0C\u4E0D\u8981\u518D\u6B21\u4ED8\u6B3E\u3002",
      next: { command: `itpay checkout --id ${input.checkoutID} --token ${input.displayToken} --json`, reason: "\u8BFB\u53D6\u8BA2\u5355\u548C\u5C65\u7EA6\u53E5\u67C4" },
      recovery: []
    };
  }
  const presentationHandoff = buildCheckoutHandoff({
    platform,
    url: input.plan.linkOnlyURL ?? input.checkoutURL,
    amount,
    plan: input.plan,
    ...input.agentType ? { agentType: input.agentType } : {},
    ...input.target ? { target: input.target } : {},
    ...input.qrPNGURL ? { qrImageURL: input.qrPNGURL } : {},
    ...input.plan.ideImageAttach?.status === "downloaded" && input.plan.ideImageAttach.localPath ? { localPath: input.plan.ideImageAttach.localPath } : {},
    ...platform === "markdown" ? { markdown: buildAgentChatHandoff(input.plan).markdown } : {}
  });
  return {
    status: "human_checkout_required",
    result,
    handoff: presentationHandoff.handoff,
    instruction: presentationHandoff.instruction,
    next: { command: input.plan.afterActionCommand ?? `itpay checkout --id ${input.checkoutID} --token ${input.displayToken} --json`, reason: "\u7A0D\u540E\u67E5\u8BE2\u540C\u4E00\u7B14 Checkout \u72B6\u6001" },
    recovery: []
  };
}
async function waitForPaymentSSE(backend, checkoutID, displayToken, timeoutSec) {
  return new Promise((resolve5) => {
    const controller = new AbortController();
    const timeout = setTimeout(() => {
      controller.abort();
      resolve5("timeout");
    }, timeoutSec * 1e3);
    backend.streamCheckoutEvents(checkoutID, displayToken, (event) => {
      if (event.type === "payment_intent.verified") {
        clearTimeout(timeout);
        controller.abort();
        resolve5("verified");
      }
    }, controller.signal).catch(() => {
    }).finally(() => {
      clearTimeout(timeout);
    });
  });
}
function buildCheckoutQRPlan(input) {
  const summary = `Scan the QR or open ${input.checkoutURL} to start the human checkout flow.`;
  const isPayment = input.paymentIntentID != null;
  const afterCommand = qualifyItPayCommand(`itpay checkout --id ${input.checkoutID} --token ${input.displayToken}${input.locale === "en" ? " --locale en" : ""} --json`, input.agentType);
  const platform = {
    text: summary,
    links: [
      { label: "\u6253\u5F00\u4ED8\u6B3E\u9875\u9762", url: input.checkoutURL }
    ],
    buttons: [
      { label: "\u6253\u5F00\u6536\u94F6\u53F0", kind: "url", url: input.checkoutURL },
      ...input.checkoutID ? [{ label: "\u67E5\u8BE2 Checkout \u72B6\u6001", kind: "callback", intent: "check_checkout_status", ref: input.checkoutID }] : []
    ],
    blocks: [],
    ...input.qrPNGURL ? { media: [{ url: input.qrPNGURL, label: "Branded QR", mimeType: "image/png" }] } : {}
  };
  const plan = {
    kind: isPayment ? "payment_qr" : "checkout_qr",
    host: input.host,
    summary,
    url: input.qrPayload,
    ...input.agentType?.trim().toLowerCase() === "workbuddy" && input.cardURL ? { linkOnlyURL: input.cardURL } : {},
    preferredQRSources: [input.qrPNGURL ?? input.qrPayload],
    checkoutID: input.checkoutID,
    platform,
    afterActionCommand: afterCommand,
    afterActionLabel: "\u626B\u7801\u6216\u70B9\u51FB\u94FE\u63A5\u5B8C\u6210\u652F\u4ED8\u540E\uFF0C\u6267\u884C\u4EE5\u4E0B\u547D\u4EE4\u67E5\u8BE2\u72B6\u6001\uFF1A"
  };
  if (input.orderItems)
    plan.orderItems = input.orderItems;
  if (input.orderCurrency)
    plan.orderCurrency = input.orderCurrency;
  if (input.paymentMethod)
    plan.paymentMethod = input.paymentMethod;
  if (input.paymentStatus)
    plan.paymentStatus = input.paymentStatus;
  if (input.paymentIntentID)
    plan.paymentIntentID = input.paymentIntentID;
  return plan;
}
function fallbackCardURL(baseURL, checkoutID, displayToken) {
  const root = baseURL.replace(/\/$/, "");
  return `${root}/v1/checkouts/${encodeURIComponent(checkoutID)}/card?display_token=${encodeURIComponent(displayToken)}`;
}
function fallbackCardPNGURL(baseURL, checkoutID, displayToken) {
  return `${fallbackCardURL(baseURL, checkoutID, displayToken)}.png`.replace("/card?", "/card.png?");
}
function findMissingContactFields(contact, fields) {
  return fields.filter((field) => {
    const value = contact?.[field];
    return typeof value !== "string" || value.trim().length === 0;
  });
}
function tokenizedCheckoutURL(checkoutURL, displayToken, qrPayload) {
  if (qrPayload.trim().length > 0) {
    return qrPayload;
  }
  if (checkoutURL.trim().length === 0 || displayToken.trim().length === 0) {
    return checkoutURL;
  }
  try {
    const parsed = new URL(checkoutURL);
    if (!parsed.searchParams.has("display_token")) {
      parsed.searchParams.set("display_token", displayToken);
    }
    return parsed.toString();
  } catch {
    const separator = checkoutURL.includes("?") ? "&" : "?";
    return `${checkoutURL}${separator}display_token=${encodeURIComponent(displayToken)}`;
  }
}
function absolutePublicURL(baseURL, value) {
  try {
    return new URL(value, baseURL.endsWith("/") ? baseURL : `${baseURL}/`).toString();
  } catch {
    return value;
  }
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/commands/catalog.js
async function runCatalogList(backend, options = {}) {
  const manifest = await backend.getCatalogManifest();
  const services2 = manifest.manifest.items.map(summarizeService);
  const firstServiceID = manifest.manifest.items.find((item) => item.service_id)?.service_id;
  const empty = services2.length === 0;
  const jsonFlag = options.jsonOutput ? " --json" : "";
  writeCommandEnvelope({
    status: empty ? "catalog_empty" : "listed",
    result: { catalog_version: manifest.version, services: services2 },
    instruction: empty ? "\u5F53\u524D\u6CA1\u6709\u5DF2\u53D1\u5E03\u670D\u52A1\uFF1B\u7A0D\u540E\u91CD\u8BD5\uFF0C\u4E0D\u8981\u731C\u6D4B service_id\u3002" : "\u5411\u7528\u6237\u89E3\u91CA\u4E3B\u670D\u52A1\u3001\u8F85\u52A9\u6B65\u9AA4\u548C\u4EF7\u683C\uFF1B\u5F97\u5230\u7528\u6237\u610F\u56FE\u540E\u518D\u542F\u52A8\u5BF9\u5E94 service_id\u3002",
    next: empty ? { command: `itpay catalog list${jsonFlag}`, reason: "\u7A0D\u540E\u91CD\u65B0\u8BFB\u53D6\u5DF2\u53D1\u5E03\u76EE\u5F55" } : {
      command: `itpay services start ${services2.length === 1 && firstServiceID ? firstServiceID : "<service_id>"}${jsonFlag}`,
      reason: "\u542F\u52A8\u7528\u6237\u9009\u62E9\u7684\u670D\u52A1"
    },
    recovery: []
  }, {
    ...options,
    plainResult: catalogPlainLines(manifest.version, services2)
  });
}
function summarizeService(item) {
  const flow = item.service_flow;
  return {
    service_id: item.service_id ?? null,
    title: item.title,
    description: item.description ?? "",
    ...flow ? {
      discovery: {
        title: flow.discovery.title,
        description: flow.discovery.description,
        ...flow.discovery.free_quota_limit !== void 0 ? { free_quota: flow.discovery.free_quota_limit } : {},
        ...flow.discovery.paid_continuation ? {
          paid_price: formatProductMoney(flow.discovery.paid_continuation.amount_minor, flow.discovery.paid_continuation.currency)
        } : {}
      },
      primary_offer: {
        title: flow.primary_service.title,
        description: flow.primary_service.description,
        price: formatProductMoney(flow.primary_service.amount_minor, flow.primary_service.currency)
      }
    } : {}
  };
}
function catalogPlainLines(version, services2) {
  const lines = [`catalog_version: ${version}`];
  for (const service of services2) {
    lines.push(`service: ${String(service.title)}`);
    lines.push(`  service_id: ${String(service.service_id ?? "unavailable")}`);
    if (service.description)
      lines.push(`  description: ${String(service.description)}`);
    const discovery = service.discovery;
    if (discovery) {
      const quota = discovery.free_quota !== void 0 ? `; free_quota: ${String(discovery.free_quota)}` : "";
      const paid = discovery.paid_price ? `; paid_price: ${String(discovery.paid_price)}` : "";
      lines.push(`  discovery: ${String(discovery.title)}${quota}${paid}`);
      lines.push(`    ${String(discovery.description)}`);
    }
    const primary = service.primary_offer;
    if (primary) {
      lines.push(`  primary_offer: ${String(primary.title)}; price: ${String(primary.price)}`);
      lines.push(`    ${String(primary.description)}`);
    }
  }
  return lines;
}
function formatProductMoney(amountMinor, currency) {
  return new Intl.NumberFormat("zh-CN", {
    style: "currency",
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amountMinor / 100);
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/commands/compatibility.js
async function requirePlatformCompatibility(backend) {
  const platform = await backend.compatibility();
  const compatible = platform.api_contract_revision === API_CONTRACT_REVISION && compareVersions(CLI_VERSION, platform.minimum_cli_version) >= 0 && versionMajor(CLI_VERSION) <= platform.maximum_cli_major;
  if (compatible)
    return;
  throw new HttpError(426, {
    code: "client_upgrade_required",
    message: `CLI ${CLI_VERSION} contract ${API_CONTRACT_REVISION} is incompatible with platform ${platform.platform_revision} contract ${platform.api_contract_revision} (minimum CLI ${platform.minimum_cli_version}, maximum major ${platform.maximum_cli_major})`,
    minimum_cli_version: platform.minimum_cli_version,
    maximum_cli_major: platform.maximum_cli_major,
    platform_revision: platform.platform_revision,
    api_contract_revision: platform.api_contract_revision
  }, "CLI is incompatible with the active ItPay platform release");
}
function compareVersions(left, right) {
  const a = versionParts(left);
  const b = versionParts(right);
  if (!a || !b)
    return -1;
  for (let index = 0; index < 3; index += 1) {
    if (a[index] !== b[index])
      return a[index] - b[index];
  }
  return 0;
}
function versionMajor(version) {
  return versionParts(version)?.[0] ?? Number.MAX_SAFE_INTEGER;
}
function versionParts(version) {
  const match = /^(\d+)\.(\d+)\.(\d+)$/.exec(version.trim());
  return match ? [Number(match[1]), Number(match[2]), Number(match[3])] : void 0;
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/commands/checkout.js
async function runCheckoutPresentation(backend, options) {
  const locale = normalizeCardLocale(options.locale);
  const presentation = await backend.getCheckoutPresentation(options.checkoutID, options.displayToken, locale === "en" ? locale : void 0);
  const host = options.host ?? "terminal";
  if (!checkoutNeedsHumanHandoff(presentation.checkout.status)) {
    const envelope2 = terminalCheckoutEnvelope(presentation);
    writeCommandEnvelope(envelope2, {
      ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
      ...options.output ? { output: options.output } : {},
      plainResult: checkoutPlainResult(envelope2.result)
    });
    return;
  }
  const checkoutURL = checkoutPageURL(options.baseURL, options.checkoutID, options.displayToken);
  const cardURL = localizeCardURL(absolutePublicURL2(options.baseURL, presentation.card_url ?? checkoutCardURL(options.baseURL, options.checkoutID, options.displayToken)), locale);
  const qrPNGURL = absolutePublicURL2(options.baseURL, presentation.card_png_url ?? presentation.qr_png_url ?? checkoutCardPNGURL(options.baseURL, options.checkoutID, options.displayToken));
  const localizedPNGURL = localizeCardURL(qrPNGURL, locale);
  const nextCommand = `itpay checkout --id ${options.checkoutID} --token ${options.displayToken}${locale === "en" ? " --locale en" : ""} --json`;
  const plan = buildCheckoutQRPlan({
    host,
    checkoutID: options.checkoutID,
    checkoutURL,
    cardURL,
    displayToken: options.displayToken,
    qrPayload: checkoutURL,
    qrPNGURL: localizedPNGURL,
    nextAction: presentation.checkout.next_action,
    orderItems: presentation.items.map((item) => ({
      title: item.title,
      quantity: item.quantity,
      amountMinor: item.amount_minor,
      currency: item.currency
    })),
    orderCurrency: presentation.checkout.currency,
    ...options.agentType ? { agentType: options.agentType } : {}
  });
  const platform = platformKeyForHost(host);
  if (shouldPrepareLocalCheckoutImage(platform)) {
    await ensureIdeImageAttach(plan, {
      ...options.baseURL ? { baseURL: options.baseURL } : {}
    });
  }
  const envelope = pendingCheckoutEnvelope(presentation, checkoutURL, plan, nextCommand, options.agentType, options.target);
  const plainResult = checkoutPlainResult(envelope.result);
  if (!options.jsonOutput && platformKeyForHost(host) === "terminal") {
    plainResult.push("qr:", await renderTerminalQR(checkoutURL, "terminal"));
  }
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {},
    plainResult
  });
}
function pendingCheckoutEnvelope(presentation, checkoutURL, plan, nextCommand, agentType, target) {
  const platform = platformKeyForHost(plan.host);
  const amount = formatMoney2(presentation.checkout.amount_minor, presentation.checkout.currency);
  const presentationHandoff = buildCheckoutHandoff({
    platform,
    url: plan.linkOnlyURL ?? checkoutURL,
    amount,
    plan,
    ...agentType ? { agentType } : {},
    ...target ? { target } : {},
    ...plan.preferredQRSources[0] ? { qrImageURL: plan.preferredQRSources[0] } : {},
    ...plan.ideImageAttach?.status === "downloaded" && plan.ideImageAttach.localPath ? { localPath: plan.ideImageAttach.localPath } : {},
    ...platform === "markdown" ? { markdown: buildAgentChatHandoff(plan).markdown } : {}
  });
  return {
    status: "human_checkout_required",
    result: {
      checkout_id: presentation.checkout.checkout_id,
      payment: "pending",
      amount
    },
    handoff: presentationHandoff.handoff,
    instruction: presentationHandoff.instruction,
    next: { command: nextCommand, reason: "\u7A0D\u540E\u53EA\u67E5\u8BE2\u540C\u4E00 Checkout" },
    recovery: []
  };
}
function terminalCheckoutEnvelope(presentation) {
  const checkout = presentation.checkout;
  const serviceExecutionIDs = [...new Set(presentation.items.map((item) => item.service_execution_id).filter((id) => Boolean(id)))];
  const payment = checkout.status === "refunded" ? "refunded" : checkout.status === "payment_succeeded" || checkout.status === "completed" ? "verified" : checkout.status;
  const result = {
    checkout_id: checkout.checkout_id,
    payment,
    ...presentation.completed_order_id ? { order_id: presentation.completed_order_id } : {},
    ...serviceExecutionIDs.length === 1 ? { service_execution_id: serviceExecutionIDs[0] } : {},
    ...serviceExecutionIDs.length > 1 ? { service_execution_ids: serviceExecutionIDs } : {}
  };
  let status = checkout.status;
  let instruction = "Checkout \u5DF2\u7ED3\u675F\uFF1B\u4E0D\u8981\u518D\u6B21\u5C55\u793A\u4ED8\u6B3E\u4E8C\u7EF4\u7801\u3002";
  let next = null;
  const recovery = [];
  if (payment === "verified") {
    status = "completed";
    instruction = "Backend \u5DF2\u786E\u8BA4\u8FD9\u7B14\u4ED8\u6B3E\u3002\u4E0D\u8981\u518D\u6B21\u5C55\u793A\u4ED8\u6B3E\u5165\u53E3\uFF0C\u4E0D\u8981\u8C03\u7528 pay\uFF0C\u4E0D\u8981\u521B\u5EFA\u65B0 Checkout \u6216 Execution\u3002\u73B0\u5728\u53EA\u6267\u884C next.command\uFF0C\u8BFB\u53D6\u540C\u4E00 Execution \u7684\u5C65\u7EA6\u7ED3\u679C\u3002";
    next = serviceExecutionIDs.length === 1 ? { command: `itpay services next ${serviceExecutionIDs[0]} --json`, reason: "\u8BFB\u53D6\u540C\u4E00\u7B14\u5DF2\u4ED8\u6B3E Service Execution" } : presentation.completed_order_id ? { command: `itpay order ${presentation.completed_order_id}`, reason: "\u8BFB\u53D6\u5DF2\u521B\u5EFA\u8BA2\u5355" } : { command: "itpay orders", reason: "\u6062\u590D\u5DF2\u4ED8\u6B3E\u8BA2\u5355" };
  } else if (checkout.status === "refunded") {
    instruction = "\u8BE5 Checkout \u5DF2\u9000\u6B3E\uFF0C\u4E0D\u8981\u518D\u6B21\u4ED8\u6B3E\u6216\u5C55\u793A\u4E8C\u7EF4\u7801\u3002";
    if (presentation.completed_order_id)
      next = { command: `itpay order ${presentation.completed_order_id}`, reason: "\u8BFB\u53D6\u8BA2\u5355\u4E0E\u9000\u6B3E\u72B6\u6001" };
  } else if (checkout.status === "failed" || checkout.status === "expired") {
    instruction = "\u8BE5 Checkout \u5DF2\u5931\u6548\uFF1B\u4E0D\u8981\u7EE7\u7EED\u4F7F\u7528\u5F53\u524D\u4ED8\u6B3E\u5165\u53E3\u3002";
    if (serviceExecutionIDs.length === 1) {
      recovery.push({ command: `itpay services next ${serviceExecutionIDs[0]} --json`, reason: "\u7531\u670D\u52A1\u7AEF\u51B3\u5B9A\u662F\u5426\u53EF\u6062\u590D Checkout" });
    }
  }
  return { status, result, instruction, next, recovery };
}
function checkoutNeedsHumanHandoff(status) {
  return !(/* @__PURE__ */ new Set(["payment_succeeded", "completed", "failed", "expired", "refunded"])).has(status);
}
function checkoutPlainResult(result) {
  return Object.entries(result).map(([key, value]) => `${key}: ${typeof value === "string" ? value : JSON.stringify(value)}`);
}
function formatMoney2(amountMinor, currency) {
  return `${(amountMinor / 100).toFixed(2)} ${currency}`;
}
function checkoutPageURL(baseURL, checkoutID, displayToken) {
  const root = publicRoot(baseURL);
  return `${root}/checkout/${encodeURIComponent(checkoutID)}?display_token=${encodeURIComponent(displayToken)}`;
}
function checkoutCardURL(baseURL, checkoutID, displayToken) {
  const root = publicRoot(baseURL);
  return `${root}/v1/checkouts/${encodeURIComponent(checkoutID)}/card?display_token=${encodeURIComponent(displayToken)}`;
}
function checkoutCardPNGURL(baseURL, checkoutID, displayToken) {
  const root = publicRoot(baseURL);
  return `${root}/v1/checkouts/${encodeURIComponent(checkoutID)}/card.png?display_token=${encodeURIComponent(displayToken)}`;
}
function publicRoot(baseURL) {
  return (baseURL ?? DEFAULT_BASE_URL).replace(/\/$/, "");
}
function absolutePublicURL2(baseURL, value) {
  try {
    const root = publicRoot(baseURL);
    return new URL(value, `${root}/`).toString();
  } catch {
    return value;
  }
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/commands/pay.js
async function runPay(backend, options) {
  const intent = await backend.createPaymentIntent(options.checkoutID, {
    payment_method_type: options.method,
    display_token: options.displayToken,
    ...options.refreshAction ? { refresh_action: true } : {}
  });
  const envelope = payEnvelope(intent, options);
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {}
  });
}
function payEnvelope(intent, options) {
  const terminal = ["failed", "expired", "refunded"].includes(intent.status);
  const verified = intent.status === "verified" || intent.status === "partially_refunded";
  const handoff = {};
  const workBuddyLinkOnly = isWorkBuddyPlainChat(options.agentType, platformKeyForHost(options.host));
  if (!terminal && !verified && workBuddyLinkOnly) {
    const url = intent.action?.mobile_wallet_url ?? intent.action?.qr_image_url;
    if (url)
      handoff.url = url;
  } else {
    if (!terminal && !verified && intent.action?.qr_image_url)
      handoff.qr_image_url = intent.action.qr_image_url;
    if (!terminal && !verified && intent.action?.mobile_wallet_url)
      handoff.mobile_wallet_url = intent.action.mobile_wallet_url;
  }
  const hasAction = Object.keys(handoff).length > 0;
  const amount = formatMoney(intent.amount_minor, intent.currency);
  return {
    status: verified ? "payment_verified" : terminal ? "payment_unavailable" : hasAction ? "payment_action_ready" : "payment_action_pending",
    result: {
      checkout_id: options.checkoutID,
      payment_intent_id: intent.payment_intent_id,
      payment: verified ? "verified" : intent.status,
      amount
    },
    ...hasAction ? { handoff } : {},
    instruction: payInstruction(options, verified, terminal, hasAction, amount),
    next: {
      command: `itpay checkout --id ${options.checkoutID} --token ${options.displayToken} --json`,
      reason: verified ? "\u8BFB\u53D6\u6743\u5A01\u8BA2\u5355\u548C\u5C65\u7EA6\u72B6\u6001" : "\u8BFB\u53D6\u540C\u4E00 Checkout \u7684\u6743\u5A01\u4ED8\u6B3E\u72B6\u6001"
    },
    recovery: []
  };
}
function payInstruction(options, verified, terminal, hasAction, amount) {
  if (verified)
    return "\u4ED8\u6B3E\u5DF2\u786E\u8BA4\uFF1B\u4E0D\u8981\u518D\u6B21\u5C55\u793A\u4ED8\u6B3E\u52A8\u4F5C\uFF0C\u7EE7\u7EED\u8BFB\u53D6\u540C\u4E00 Checkout\u3002";
  if (terminal)
    return "Payment Intent \u5DF2\u7EC8\u6B62\uFF1B\u4E0D\u8981\u81EA\u884C\u521B\u5EFA\u66FF\u4EE3\u4ED8\u6B3E\uFF0C\u56DE\u5230\u540C\u4E00 Checkout \u8BFB\u53D6\u6062\u590D\u65B9\u5411\u3002";
  if (!hasAction)
    return "Payment Intent \u5C1A\u672A\u8FD4\u56DE\u53EF\u5C55\u793A\u52A8\u4F5C\uFF1B\u4E0D\u8981\u731C\u6D4B\u6E20\u9053\u94FE\u63A5\uFF0C\u56DE\u5230\u540C\u4E00 Checkout \u67E5\u8BE2\u3002";
  const platform = platformKeyForHost(options.host);
  if (isWorkBuddyPlainChat(options.agentType, platform)) {
    return `\u8FD9\u662F\u53D7\u63A7\u9003\u751F\u5165\u53E3\u3002\u8BF4\u660E\u91D1\u989D ${amount}\uFF0C\u628A handoff.url \u4F5C\u4E3A\u53EF\u70B9\u51FB\u94FE\u63A5\u53D1\u9001\u7ED9\u7528\u6237\uFF0C\u7136\u540E\u505C\u6B62\u7B49\u5F85\u3002\u4E0D\u8981\u8C03\u7528 present_files\uFF0C\u4E0D\u8981\u7ACB\u5373\u67E5\u8BE2\u3001\u521B\u5EFA\u66FF\u4EE3 Checkout \u6216 Payment Intent\u3002`;
  }
  if (options.host === "codex" || options.host === "claude-code")
    return "\u8FD9\u662F\u53D7\u63A7\u9003\u751F\u5165\u53E3\uFF1B\u628A handoff \u4E2D\u7684\u4E8C\u7EF4\u7801\u6216\u94B1\u5305\u94FE\u63A5\u5B9E\u9645\u53D1\u5230\u5F53\u524D\u684C\u9762\u5BF9\u8BDD\uFF0C\u7136\u540E\u505C\u6B62\u7B49\u5F85\u3002";
  if (options.host === "terminal")
    return "\u8FD9\u662F\u53D7\u63A7\u9003\u751F\u5165\u53E3\uFF1B\u53EA\u5728\u7528\u6237\u53EF\u89C1\u7EC8\u7AEF\u5C55\u793A handoff\uFF0C\u7136\u540E\u505C\u6B62\u7B49\u5F85\u3002";
  return "\u8FD9\u662F\u53D7\u63A7\u9003\u751F\u5165\u53E3\uFF1B\u628A handoff \u4E2D\u7684\u4E8C\u7EF4\u7801\u6216\u94B1\u5305\u94FE\u63A5\u53D1\u9001\u5230\u5F53\u524D\u4F1A\u8BDD\uFF0C\u7136\u540E\u505C\u6B62\u7B49\u5F85\u3002";
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/commands/order.js
async function runOrder(backend, orderID, options = {}) {
  const order = await backend.getOrder(orderID);
  const [delivery, refundResponse] = await Promise.all([
    order.status === "delivered" ? backend.getOrderDeliveryAccess(orderID) : Promise.resolve(void 0),
    backend.listOrderRefunds(orderID)
  ]);
  const lockedRefund = refundResponse.refunds.find((refund2) => refund2.access_locked);
  const envelope = orderEnvelope(order, delivery, lockedRefund);
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {},
    plainResult: orderPlainResult(envelope.result)
  });
}
function orderEnvelope(order, delivery, lockedRefund) {
  const refundTerminal = lockedRefund && ["succeeded", "failed", "cancelled", "rejected"].includes(lockedRefund.status);
  let instruction = "\u8BA2\u5355\u72B6\u6001\u5DF2\u8BFB\u53D6\uFF1B\u5F53\u524D\u6CA1\u6709\u53EF\u7528\u4EA4\u4ED8\u5165\u53E3\u3002";
  let next = null;
  if (lockedRefund) {
    instruction = "\u9000\u6B3E\u8BBF\u95EE\u9501\u5DF2\u751F\u6548\uFF1B\u4E0D\u8981 reveal\u3001\u521B\u5EFA grant \u6216\u8BFB\u53D6\u4EA4\u4ED8\u7ED3\u679C\u3002";
    if (!refundTerminal) {
      next = { command: `itpay refund get ${lockedRefund.refund_request_id} --json`, reason: "\u8BFB\u53D6\u9000\u6B3E\u7684\u670D\u52A1\u5668\u72B6\u6001" };
    }
  } else if (delivery?.service_execution_id) {
    instruction = "\u6839\u636E delivery_mode \u4F7F\u7528\u5BF9\u5E94\u8BFB\u53D6\u5165\u53E3\uFF1B\u4E0D\u8981\u4ECE\u8BA2\u5355\u6458\u8981\u731C\u6D4B\u53D7\u4FDD\u62A4\u5185\u5BB9\u3002";
    next = { command: `itpay services next ${delivery.service_execution_id} --json`, reason: "\u8BFB\u53D6\u4EA4\u4ED8\u72B6\u6001" };
  } else if (!["delivered", "refunded", "failed", "cancelled"].includes(order.status)) {
    instruction = "\u8BA2\u5355\u5C1A\u672A\u8FDB\u5165\u4EA4\u4ED8\u7EC8\u6001\uFF1B\u7A0D\u540E\u67E5\u8BE2\u540C\u4E00\u8BA2\u5355\uFF0C\u4E0D\u8981\u521B\u5EFA\u66FF\u4EE3\u8BA2\u5355\u3002";
    next = { command: `itpay order ${order.order_id} --json`, reason: "\u5237\u65B0\u8BA2\u5355\u72B6\u6001" };
  }
  return {
    status: order.status,
    result: {
      order_id: order.order_id,
      ...order.order_code ? { order_code: order.order_code } : {},
      amount: formatMoney(order.amount_minor, order.currency),
      ...delivery ? { delivery_mode: delivery.delivery_mode } : {},
      access_locked: Boolean(lockedRefund),
      ...delivery?.service_execution_id ? { service_execution_id: delivery.service_execution_id } : {},
      ...lockedRefund ? { refund: { refund_request_id: lockedRefund.refund_request_id, status: lockedRefund.status } } : {}
    },
    instruction,
    next,
    recovery: []
  };
}
function orderPlainResult(result) {
  return Object.entries(result).map(([key, value]) => `${key}: ${typeof value === "string" ? value : JSON.stringify(value)}`);
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/commands/orders.js
var ORDER_STATUSES = /* @__PURE__ */ new Set([
  "pending_payment",
  "paid",
  "delivery_pending",
  "delivered",
  "failed",
  "partially_refunded",
  "refunded",
  "cancelled"
]);
async function runListOrders(backend, config, options) {
  const out = resolveOutput(options.output);
  if (!Number.isInteger(options.limit) || options.limit < 1 || options.limit > 100) {
    throw new CommandContractError("limit_invalid", "--limit must be an integer from 1 to 100", "\u4F7F\u7528 1 \u5230 100 \u7684\u6574\u6570 limit\uFF1B\u672C\u6B21\u672A\u8BFB\u53D6\u8BA2\u5355\u5217\u8868\u3002", [{ command: "itpay orders --limit 20 --json", reason: "\u4F7F\u7528\u9ED8\u8BA4\u4E0A\u9650\u91CD\u8BD5" }]);
  }
  if (options.status && !ORDER_STATUSES.has(options.status)) {
    throw new CommandContractError("order_status_invalid", `unsupported order status: ${options.status}`, "\u4F7F\u7528\u8BA2\u5355\u5408\u540C\u4E2D\u7684\u6709\u6548 status\uFF1B\u672C\u6B21\u672A\u8BFB\u53D6\u8BA2\u5355\u5217\u8868\u3002", [{ command: "itpay orders --limit 20 --json", reason: "\u79FB\u9664\u72B6\u6001\u8FC7\u6EE4\u540E\u91CD\u8BD5" }]);
  }
  if (!config.bearerToken) {
    throw new CommandContractError("session_required", "account-scoped Buyer session is required", "\u8BA2\u5355\u5386\u53F2\u53EA\u5BF9\u7F51\u9875\u767B\u5F55\u8D26\u53F7\u5F00\u653E\uFF1B\u4E0D\u8981\u4F2A\u9020 Buyer token\u3002Agent \u53EF\u6539\u4E3A\u6062\u590D\u5F53\u524D\u8BBE\u5907\u7ED1\u5B9A\u7684 Service Execution\u3002", [{ command: "itpay services list --json", reason: "\u6062\u590D\u5F53\u524D Agent \u8BBE\u5907\u53EF\u89C1\u7684\u6267\u884C" }]);
  }
  const response = await backend.listAccountOrders(options.limit, options.status, config.bearerToken);
  const orders = response.orders.map((order) => ({
    order_id: order.order_id,
    ...order.order_code ? { order_code: order.order_code } : {},
    status: order.status,
    amount: formatMoney(order.amount_minor, order.currency),
    created_at: order.created_at
  }));
  const latest = orders[0];
  const envelope = {
    status: latest ? "listed" : "no_orders",
    result: { orders },
    instruction: latest ? "\u7ED3\u679C\u6309\u6700\u65B0\u5230\u6700\u65E7\u6392\u5217\uFF1B\u6309\u9875\u9762\u7F16\u53F7\u3001\u65F6\u95F4\u548C\u72B6\u6001\u9009\u62E9\u76EE\u6807\u8BA2\u5355\uFF0C\u4E0D\u8981\u5047\u8BBE\u7B2C\u4E00\u7B14\u5C31\u662F\u5F53\u524D\u4EFB\u52A1\u3002" : "\u5F53\u524D\u8D26\u53F7\u6CA1\u6709\u7B26\u5408\u6761\u4EF6\u7684\u8BA2\u5355\uFF1B\u4E0D\u8981\u731C\u6D4B\u8BA2\u5355 ID\u3002",
    next: latest ? { command: `itpay order ${latest.order_id} --json`, reason: "\u9ED8\u8BA4\u8BFB\u53D6\u6700\u65B0\u8BA2\u5355" } : null,
    recovery: latest ? [] : [{ command: "itpay services list --json", reason: "\u6062\u590D\u5F53\u524D Agent \u8BBE\u5907\u53EF\u89C1\u7684\u6267\u884C" }]
  };
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    output: out,
    plainResult: orders.map((order) => `${order.order_code ?? order.order_id}: ${order.status} ${order.amount} created=${order.created_at}`)
  });
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/commands/refund.js
async function runRefund(backend, config, options) {
  const reason = options.reason?.trim() || "buyer_requested";
  const refund2 = await backend.createRefund(options.orderID, { reason }, config.bearerToken, await operationID(config, `refund.create:${options.orderID}:${reason}`));
  const envelope = refundStateEnvelope(refund2, "requested");
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {},
    plainResult: Object.entries(envelope.result).map(([key, value]) => `${key}: ${typeof value === "string" ? value : JSON.stringify(value)}`)
  });
}
function refundStateEnvelope(refund2, status) {
  const terminal = ["succeeded", "failed", "cancelled", "rejected"].includes(refund2.status);
  let instruction = "\u9000\u6B3E\u5904\u7406\u4E2D\uFF0C\u4EA4\u4ED8\u5DF2\u51BB\u7ED3\uFF1B\u4E0D\u8981 reveal\u3001\u6388\u6743\u6216\u8BFB\u53D6\u7ED3\u679C\u3002";
  if (refund2.decision_mode === "manual")
    instruction = "\u9000\u6B3E\u5DF2\u8FDB\u5165\u4EBA\u5DE5\u5BA1\u6838\uFF0C\u4EA4\u4ED8\u4FDD\u6301\u51BB\u7ED3\uFF1B\u7B49\u5F85\u670D\u52A1\u5668\u51B3\u5B9A\u3002";
  if (!refund2.access_locked)
    instruction = "\u9000\u6B3E\u5F53\u524D\u672A\u9501\u5B9A\u4EA4\u4ED8\uFF1B\u6309\u670D\u52A1\u5668\u72B6\u6001\u5904\u7406\uFF0C\u4E0D\u8981\u81EA\u884C\u63A8\u65AD\u9000\u6B3E\u7ED3\u679C\u3002";
  if (refund2.status === "succeeded")
    instruction = "\u9000\u6B3E\u5DF2\u6210\u529F\uFF1B\u4EA4\u4ED8\u6C38\u4E45\u5173\u95ED\u3002";
  if (refund2.status === "cancelled" || refund2.status === "rejected")
    instruction = "\u9000\u6B3E\u672A\u6267\u884C\uFF0C\u4EA4\u4ED8\u8D44\u683C\u53EF\u6062\u590D\uFF1B\u65E7 grant \u4E0D\u4F1A\u590D\u6D3B\uFF0C\u9700\u8981\u7528\u6237\u91CD\u65B0\u6388\u6743\u3002";
  if (refund2.status === "failed") {
    if (refund2.failure_class === "known_no_effect")
      instruction = "\u9000\u6B3E\u6E20\u9053\u8BF7\u6C42\u786E\u8BA4\u672A\u53D1\u9001\uFF1B\u4E0D\u8981\u81EA\u884C\u91CD\u8BD5\u3002\u8BF7\u7528\u6237\u8054\u7CFB\u5E73\u53F0\u7BA1\u7406\u5458\u51B3\u5B9A\u662F\u5426\u91CD\u65B0\u6267\u884C\u3002";
    else if (refund2.failure_class === "retryable")
      instruction = "\u9000\u6B3E\u6E20\u9053\u660E\u786E\u8FD4\u56DE\u53EF\u91CD\u8BD5\u5931\u8D25\uFF1B\u4E0D\u8981\u81EA\u884C\u91CD\u8BD5\u3002\u8BF7\u7528\u6237\u7B49\u5F85\u5E73\u53F0\u7BA1\u7406\u5458\u5904\u7406\u3002";
    else if (refund2.failure_class === "outcome_unknown")
      instruction = "\u9000\u6B3E\u8BF7\u6C42\u7ED3\u679C\u672A\u77E5\uFF0C\u4EA4\u4ED8\u7EE7\u7EED\u9501\u5B9A\uFF1B\u5FC5\u987B\u5148\u7531\u5E73\u53F0\u5BF9\u8D26\uFF0C\u7981\u6B62\u91CD\u8BD5\u6216\u91CD\u590D\u7533\u8BF7\u3002";
    else if (refund2.failure_class === "permanent")
      instruction = "\u9000\u6B3E\u6E20\u9053\u660E\u786E\u62D2\u7EDD\u672C\u6B21\u9000\u6B3E\uFF1B\u4E0D\u8981\u91CD\u8BD5\u3002\u8BF7\u7528\u6237\u8054\u7CFB\u5E73\u53F0\u652F\u6301\u3002";
    else
      instruction = "\u9000\u6B3E\u6267\u884C\u5931\u8D25\uFF1B\u4E0D\u8981\u91CD\u8BD5\u6216\u91CD\u590D\u7533\u8BF7\uFF0C\u8BF7\u7528\u6237\u8054\u7CFB\u5E73\u53F0\u652F\u6301\u3002";
  }
  return {
    status,
    result: {
      refund_request_id: refund2.refund_request_id,
      order_id: refund2.order_id,
      decision_mode: refund2.decision_mode,
      refund_status: refund2.status,
      consumption_state: refund2.consumption_state,
      ...refund2.failure_class ? { failure_class: refund2.failure_class } : {},
      access_locked: refund2.access_locked,
      can_cancel: refund2.can_cancel
    },
    instruction,
    next: terminal ? null : { command: `itpay refund watch ${refund2.refund_request_id} --json`, reason: "\u8DDF\u8E2A\u540C\u4E00\u9000\u6B3E" },
    recovery: []
  };
}
async function runListRefunds(backend, options) {
  const out = resolveOutput(options.output);
  const response = await backend.listOrderRefunds(options.orderID);
  const refunds = response.refunds.map((refund2) => ({
    refund_request_id: refund2.refund_request_id,
    status: refund2.status,
    amount: formatMoney(refund2.amount_minor, refund2.currency),
    created_at: refund2.created_at
  }));
  const active = refunds.find((refund2) => !["succeeded", "failed", "cancelled", "rejected"].includes(refund2.status));
  const selected = active ?? refunds[0];
  const envelope = {
    status: selected ? "listed" : "empty",
    result: { order_id: options.orderID, refunds },
    instruction: active ? "\u5DF2\u6709\u6D3B\u8DC3\u9000\u6B3E\uFF1B\u7EE7\u7EED\u8DDF\u8E2A\u540C\u4E00\u7B14\uFF0C\u4E0D\u8981\u4E3A\u8BE5\u8BA2\u5355\u91CD\u590D\u521B\u5EFA\u3002" : selected ? "\u7ED3\u679C\u6309\u6700\u65B0\u5230\u6700\u65E7\u6392\u5217\uFF1B\u6309\u65F6\u95F4\u548C\u72B6\u6001\u9009\u62E9\u9000\u6B3E\u8BB0\u5F55\uFF0C\u518D\u8BFB\u53D6\u6743\u5A01\u8BE6\u60C5\u3002" : "\u8BE5\u8BA2\u5355\u6CA1\u6709\u9000\u6B3E\u8BB0\u5F55\uFF1B\u786E\u8BA4\u7528\u6237\u786E\u5B9E\u8981\u6C42\u9000\u6B3E\u540E\u518D\u521B\u5EFA\u3002",
    next: selected ? { command: `itpay refund get ${selected.refund_request_id} --json`, reason: active ? "\u8BFB\u53D6\u6D3B\u8DC3\u9000\u6B3E" : "\u8BFB\u53D6\u6700\u65B0\u9000\u6B3E" } : { command: `itpay refund create --order ${options.orderID} --json`, reason: "\u4E3A\u8BE5\u8BA2\u5355\u521B\u5EFA\u9000\u6B3E" },
    recovery: []
  };
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    output: out,
    plainResult: [
      `order_id: ${options.orderID}`,
      ...refunds.map((refund2) => `${refund2.refund_request_id}: ${refund2.status} ${refund2.amount} created=${refund2.created_at}`)
    ]
  });
}
async function runGetRefund(backend, refundID, options = {}) {
  const envelope = refundStateEnvelope(await backend.getRefund(refundID), "shown");
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {},
    plainResult: Object.entries(envelope.result).map(([key, value]) => `${key}: ${typeof value === "string" ? value : JSON.stringify(value)}`)
  });
}
async function runCancelRefund(backend, refundID, reason, options = {}) {
  const refund2 = await backend.cancelRefund(refundID, reason?.trim() || "buyer_cancelled");
  const envelope = {
    status: "cancelled",
    result: {
      refund_request_id: refund2.refund_request_id,
      order_id: refund2.order_id,
      access_locked: refund2.access_locked
    },
    instruction: "\u9000\u6B3E\u5DF2\u53D6\u6D88\uFF1B\u5982\u9700\u4EA4\u4ED8\uFF0C\u91CD\u65B0\u8FDB\u5165\u8BA2\u5355\u5E76\u53D6\u5F97\u65B0\u7684\u6388\u6743\u3002",
    next: { command: `itpay order ${refund2.order_id} --json`, reason: "\u786E\u8BA4\u8BA2\u5355\u8BBF\u95EE\u72B6\u6001" },
    recovery: []
  };
  writeRefundEnvelope(envelope, options);
}
async function runWatchRefund(backend, refundID, options = {}) {
  const intervalSeconds = options.intervalSeconds ?? 2;
  const timeoutSeconds = options.timeoutSeconds ?? 120;
  if (!Number.isFinite(intervalSeconds) || intervalSeconds < 1)
    throw new Error("--interval must be at least 1 second");
  if (!Number.isFinite(timeoutSeconds) || timeoutSeconds <= 0)
    throw new Error("--timeout must be a positive number");
  const deadline = Date.now() + timeoutSeconds * 1e3;
  let refund2;
  for (; ; ) {
    refund2 = await backend.getRefund(refundID);
    if (["succeeded", "failed", "cancelled", "rejected"].includes(refund2.status)) {
      writeRefundEnvelope(refundStateEnvelope(refund2, "watch_complete"), options);
      return;
    }
    const remaining = deadline - Date.now();
    if (remaining <= 0)
      break;
    await new Promise((resolve5) => setTimeout(resolve5, Math.min(intervalSeconds * 1e3, remaining)));
  }
  writeRefundEnvelope({
    status: "watch_timeout",
    result: {
      refund_request_id: refund2.refund_request_id,
      last_status: refund2.status,
      access_locked: refund2.access_locked,
      can_cancel: refund2.can_cancel
    },
    instruction: "\u9000\u6B3E\u4ECD\u5728\u5904\u7406\uFF0C\u7A0D\u540E\u7EE7\u7EED\u8DDF\u8E2A\u540C\u4E00\u9000\u6B3E\uFF1B\u4E0D\u8981\u91CD\u590D\u7533\u8BF7\u3002",
    next: { command: `itpay refund watch ${refund2.refund_request_id} --json`, reason: "\u6062\u590D\u8F6E\u8BE2" },
    recovery: []
  }, options);
}
function writeRefundEnvelope(envelope, options) {
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {},
    plainResult: Object.entries(envelope.result).map(([key, value]) => `${key}: ${typeof value === "string" ? value : JSON.stringify(value)}`)
  });
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/commands/cart.js
function runCartAdd(session, options) {
  const out = resolveOutput(options.output);
  const item = {
    catalogItemID: options.catalogItemID,
    catalogVariantID: options.catalogVariantID,
    offerID: options.offerID,
    quantity: options.quantity,
    ...options.input ? { input: options.input } : {}
  };
  session.add(item);
  const envelope = {
    status: "added_local",
    result: {
      catalog_item_id: item.catalogItemID,
      catalog_variant_id: item.catalogVariantID,
      offer_id: item.offerID,
      quantity: item.quantity
    },
    instruction: "\u4EC5\u5199\u5165\u672C\u5730\u517C\u5BB9\u8349\u7A3F\uFF0C\u672A\u9A8C\u8BC1\u76EE\u5F55\u3001\u4EF7\u683C\u6216\u670D\u52A1\u5408\u540C\uFF1B\u4E0D\u8981\u628A\u5B83\u5F53\u4F5C canonical Cart\u3002",
    next: { command: "itpay cart show --local", reason: "\u68C0\u67E5\u672C\u5730\u8349\u7A3F" },
    recovery: []
  };
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    output: out
  });
}
async function runCartAddServer(options) {
  const out = resolveOutput(options.output);
  const item = {
    catalog_item_id: options.catalogItemID,
    catalog_variant_id: options.catalogVariantID,
    offer_id: options.offerID,
    quantity: options.quantity,
    ...options.input ? { input: options.input } : {}
  };
  const clientContext = {
    host: options.host,
    ...options.target ? { target: options.target } : {}
  };
  const cart2 = options.session.lastCartID ? await options.backend.addCartItem(options.session.lastCartID, {
    ...item,
    client_context: clientContext
  }) : await options.backend.createCart({
    currency: options.config.checkoutCurrency,
    client_context: clientContext,
    items: [item]
  });
  const line = cart2.items[cart2.items.length - 1];
  options.session.rememberServerCart({
    cartID: cart2.cart_id,
    ...line?.cart_item_id ? { cartItemID: line.cart_item_id } : {},
    ...line?.service_execution_id ? { serviceExecutionID: line.service_execution_id } : {}
  });
  if (!line?.cart_item_id) {
    throw new Error("backend did not return the added cart item");
  }
  const serviceExecutionID = line.service_execution_id;
  const envelope = {
    status: "added",
    result: {
      cart_id: cart2.cart_id,
      cart_item_id: line.cart_item_id,
      ...serviceExecutionID ? { service_execution_id: serviceExecutionID } : {},
      title: line.title,
      amount: formatMoney(line.amount_minor, line.currency)
    },
    instruction: serviceExecutionID ? "\u670D\u52A1\u578B\u9879\u76EE\u5DF2\u521B\u5EFA Service Execution\uFF1B\u5148\u8BFB\u53D6\u5176\u5F53\u524D\u6B65\u9AA4\uFF0C\u4E0D\u8981\u76F4\u63A5\u8FDB\u5165\u666E\u901A buy\u3002" : "\u666E\u901A\u9879\u76EE\u5DF2\u52A0\u5165 canonical Cart\uFF1B\u5148\u68C0\u67E5\u8D2D\u7269\u8F66\uFF0C\u518D\u521B\u5EFA Checkout\u3002",
    next: serviceExecutionID ? { command: `itpay services next ${serviceExecutionID} --json`, reason: "\u8BFB\u53D6\u670D\u52A1\u6267\u884C\u7684\u5F53\u524D\u6B65\u9AA4" } : { command: "itpay cart next --json", reason: "\u68C0\u67E5 canonical Cart" },
    recovery: []
  };
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    output: out,
    plainResult: Object.entries(envelope.result).map(([key, value]) => `${key}: ${String(value)}`)
  });
  return cart2;
}
async function runCartAddQuoteServer(options) {
  const out = resolveOutput(options.output);
  const clientContext = {
    host: options.host,
    ...options.target ? { target: options.target } : {}
  };
  const quoteItem = { service_quote_lock_id: options.serviceQuoteLockID };
  const cart2 = options.session.lastCartID ? await options.backend.addCartItem(options.session.lastCartID, {
    ...quoteItem,
    client_context: clientContext
  }) : await options.backend.createCart({
    currency: options.config.checkoutCurrency,
    client_context: clientContext,
    items: [quoteItem]
  });
  const line = cart2.items[cart2.items.length - 1];
  if (!line?.cart_item_id) {
    throw new Error("backend did not return the added cart item");
  }
  options.session.rememberServerCart({
    cartID: cart2.cart_id,
    cartItemID: line.cart_item_id,
    ...line.service_execution_id ? { serviceExecutionID: line.service_execution_id } : {}
  });
  const envelope = {
    status: "quote_added",
    result: {
      cart_id: cart2.cart_id,
      item_count: cart2.items.length,
      total: formatMoney(cart2.amount_minor, cart2.currency)
    },
    instruction: "\u4ED8\u8D39\u670D\u52A1\u62A5\u4EF7\u5DF2\u52A0\u5165\u540C\u4E00 Cart\uFF1B\u6BCF\u4E2A\u9879\u76EE\u4ECD\u4FDD\u6301\u72EC\u7ACB Execution \u548C\u4EA4\u4ED8\u3002",
    next: { command: `itpay buy --cart ${cart2.cart_id} --json`, reason: "\u786E\u8BA4\u9879\u76EE\u9F50\u5168\u540E\u521B\u5EFA\u4E00\u6B21\u5408\u5E76\u4ED8\u6B3E" },
    recovery: [{ command: "itpay cart show --json", reason: "\u68C0\u67E5\u5F53\u524D\u5408\u5E76 Cart" }]
  };
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    output: out,
    plainResult: [
      `cart_id: ${cart2.cart_id}`,
      `item_count: ${cart2.items.length}`,
      `total: ${formatMoney(cart2.amount_minor, cart2.currency)}`
    ]
  });
  return cart2;
}
function runCartRemove(session, options) {
  const out = resolveOutput(options.output);
  session.remove(options.catalogVariantID, options.offerID);
  writeCommandEnvelope({
    status: "removed_local",
    result: {
      catalog_variant_id: options.catalogVariantID,
      offer_id: options.offerID
    },
    instruction: "\u672C\u5730\u517C\u5BB9\u8349\u7A3F\u5DF2\u66F4\u65B0\uFF1B\u8FD9\u4E0D\u4EE3\u8868\u4EFB\u4F55 canonical Cart \u6216 Service Execution \u5DF2\u53D8\u66F4\u3002",
    next: { command: "itpay cart show --local --json", reason: "\u68C0\u67E5\u5269\u4F59\u672C\u5730\u8349\u7A3F" },
    recovery: []
  }, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    output: out
  });
}
async function runCartRemoveServer(backend, session, cartItemID, options = {}) {
  const out = resolveOutput(options.output);
  const cartID = session.lastCartID;
  if (!cartID) {
    throw new Error("no canonical server cart is remembered; use --local for local draft removal");
  }
  const lineID = cartItemID || session.lastCartItemID;
  if (!lineID) {
    throw new Error("missing cart item id; pass --line <cart_item_id>");
  }
  const cart2 = await backend.removeCartItem(cartID, lineID);
  const latestLine = cart2.items[cart2.items.length - 1];
  session.rememberServerCart({
    cartID: cart2.cart_id,
    ...latestLine?.cart_item_id ? { cartItemID: latestLine.cart_item_id } : {},
    ...latestLine?.service_execution_id ? { serviceExecutionID: latestLine.service_execution_id } : {}
  });
  const envelope = {
    status: "removed",
    result: {
      cart_id: cart2.cart_id,
      cart_item_id: lineID,
      remaining_item_count: cart2.items.length
    },
    instruction: "canonical Cart \u5DF2\u66F4\u65B0\uFF1B\u88AB\u5220\u9664\u7684\u6700\u540E\u4E00\u4E2A service-backed line \u5BF9\u5E94\u6267\u884C\u4F1A\u7531\u670D\u52A1\u7AEF\u4E00\u81F4\u6027\u4E8B\u52A1\u53D6\u6D88\u3002",
    next: { command: "itpay cart next --json", reason: "\u68C0\u67E5\u5269\u4F59\u5185\u5BB9" },
    recovery: []
  };
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    output: out
  });
  return cart2;
}
function runCartShow(session, options = {}) {
  const snap = session.show();
  const items = snap.items.map((item) => ({
    catalog_item_id: item.catalogItemID,
    catalog_variant_id: item.catalogVariantID,
    offer_id: item.offerID,
    quantity: item.quantity
  }));
  const envelope = {
    status: items.length > 0 ? "shown_local" : "local_empty",
    result: { currency: snap.currency, items },
    instruction: items.length > 0 ? "\u8FD9\u662F\u672A\u9A8C\u8BC1\u7684\u672C\u5730\u517C\u5BB9\u8349\u7A3F\uFF0C\u53EA\u80FD\u7528\u4E8E\u660E\u786E\u7684\u666E\u901A\u5546\u54C1\u6D41\u7A0B\uFF1B\u4E0D\u8981\u628A\u5B83\u5F53\u4F5C canonical Cart\u3002" : "\u672C\u5730\u517C\u5BB9\u8349\u7A3F\u4E3A\u7A7A\uFF1B\u4ECE\u5DF2\u53D1\u5E03\u76EE\u5F55\u91CD\u65B0\u9009\u62E9\u9879\u76EE\u3002",
    next: items.length > 0 ? { command: "itpay buy --json", reason: "\u5C06\u666E\u901A\u672C\u5730\u8349\u7A3F\u63D0\u4EA4\u4E3A canonical Cart" } : { command: "itpay catalog list --json", reason: "\u8BFB\u53D6\u5DF2\u53D1\u5E03\u76EE\u5F55" },
    recovery: []
  };
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {}
  });
}
async function runCartShowServer(backend, session, options = {}) {
  if (!session.lastCartID) {
    writeCommandEnvelope({
      status: "cart_handle_missing",
      result: {},
      instruction: "\u672C\u5730\u6CA1\u6709 canonical Cart \u53E5\u67C4\uFF1B\u4E0D\u8981\u628A\u672C\u5730\u8349\u7A3F\u9ED8\u8BA4\u4E3A\u670D\u52A1\u7AEF Cart\u3002",
      next: { command: "itpay catalog list --json", reason: "\u8BFB\u53D6\u5DF2\u53D1\u5E03\u76EE\u5F55" },
      recovery: [{ command: "itpay cart show --local --json", reason: "\u4EC5\u5728\u660E\u786E\u9700\u8981\u65F6\u68C0\u67E5\u672C\u5730\u517C\u5BB9\u8349\u7A3F" }]
    }, {
      ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
      ...options.output ? { output: options.output } : {}
    });
    return void 0;
  }
  const cart2 = await backend.getCart(session.lastCartID);
  const items = cart2.items.map((item) => ({
    ...item.cart_item_id ? { cart_item_id: item.cart_item_id } : {},
    title: item.title,
    quantity: item.quantity,
    ...item.service_execution_id ? { service_execution_id: item.service_execution_id } : {}
  }));
  const envelope = {
    status: "shown",
    result: {
      cart_id: cart2.cart_id,
      status: cart2.status,
      amount: formatMoney(cart2.amount_minor, cart2.currency),
      items
    },
    instruction: items.length > 0 ? "\u4F7F\u7528 line \u6216 execution \u53E5\u67C4\u7EE7\u7EED\uFF1B\u4E0D\u8981\u4F7F\u7528\u5185\u90E8 quote lock ID\u3002" : "canonical Cart \u5F53\u524D\u4E3A\u7A7A\uFF1B\u4ECE\u5DF2\u53D1\u5E03\u76EE\u5F55\u9009\u62E9\u9879\u76EE\u3002",
    next: items.length > 0 ? { command: "itpay cart next --json", reason: "\u53D6\u5F97\u5F53\u524D\u9996\u9009\u52A8\u4F5C" } : { command: "itpay catalog list --json", reason: "\u8BFB\u53D6\u5DF2\u53D1\u5E03\u76EE\u5F55" },
    recovery: []
  };
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {},
    plainResult: [
      `cart_id: ${cart2.cart_id}`,
      `state: ${cart2.status}`,
      `amount: ${formatMoney(cart2.amount_minor, cart2.currency)}`,
      ...items.map((item) => `${item.cart_item_id ?? "line"}: ${item.title} x${item.quantity}${item.service_execution_id ? ` service_execution=${item.service_execution_id}` : ""}`)
    ]
  });
  return cart2;
}
function runCartClear(session, options = {}) {
  session.clear();
  const envelope = {
    status: "cleared_local",
    result: { server_abandoned: false, local_state_cleared: true },
    instruction: "\u4EC5\u6E05\u9664\u4E86\u672C\u5730\u8349\u7A3F\u548C\u6062\u590D\u53E5\u67C4\uFF1BBackend Cart\u3001Checkout \u548C Service Execution \u5747\u672A\u6539\u53D8\u3002",
    next: { command: "itpay catalog list --json", reason: "\u4EC5\u5728\u7528\u6237\u63D0\u51FA\u65B0\u9700\u6C42\u65F6\u91CD\u65B0\u9009\u62E9" },
    recovery: []
  };
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {}
  });
}
async function runCartAbandonServer(backend, session, options = {}) {
  if (!session.lastCartID) {
    writeCommandEnvelope({
      status: "cart_handle_missing",
      result: {},
      instruction: "\u672C\u5730\u6CA1\u6709 canonical Cart \u53E5\u67C4\uFF1B\u672A\u4FEE\u6539\u4EFB\u4F55 Backend \u6216\u672C\u5730\u8D44\u6E90\u3002",
      next: { command: "itpay next --json", reason: "\u68C0\u67E5\u5176\u4ED6\u53EF\u6062\u590D\u53E5\u67C4" },
      recovery: [{ command: "itpay cart clear --local --json", reason: "\u4EC5\u5728\u660E\u786E\u653E\u5F03\u672C\u5730\u8349\u7A3F\u548C\u53E5\u67C4\u65F6\u6267\u884C" }]
    }, {
      ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
      ...options.output ? { output: options.output } : {}
    });
    return void 0;
  }
  const cart2 = await backend.abandonCart(session.lastCartID);
  session.clear();
  const envelope = {
    status: "abandoned",
    result: { cart_id: cart2.cart_id, server_abandoned: true },
    instruction: "canonical Cart \u5DF2\u653E\u5F03\uFF1BBackend \u5DF2\u5728\u540C\u4E00\u4E8B\u52A1\u4E2D\u8F6F\u5220\u9664 active lines\uFF0C\u5E76\u53D6\u6D88\u5176\u672A\u4ED8\u6B3E Service Execution\u3002",
    next: { command: "itpay catalog list --json", reason: "\u4EC5\u5728\u7528\u6237\u63D0\u51FA\u65B0\u9700\u6C42\u65F6\u91CD\u65B0\u9009\u62E9" },
    recovery: []
  };
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {},
    plainResult: [`cart_id: ${cart2.cart_id}`, "server_abandoned: true"]
  });
  return cart2;
}
async function runCartNext(backend, session, options = {}) {
  if (!session.lastCartID) {
    writeCartNextEnvelope({
      status: "cart_handle_missing",
      result: {},
      instruction: "\u672C\u5730\u6CA1\u6709 canonical Cart \u53E5\u67C4\uFF1B\u5148\u6062\u590D\u5DF2\u6709\u8D44\u6E90\uFF0C\u4E0D\u8981\u521B\u5EFA\u91CD\u590D Cart\u3002",
      next: { command: "itpay next --json", reason: "\u68C0\u67E5\u5176\u4ED6\u53EF\u6062\u590D\u53E5\u67C4" },
      recovery: [{ command: "itpay services list --json", reason: "\u4ECE\u670D\u52A1\u7AEF\u6062\u590D\u5F53\u524D\u8BBE\u5907\u7684\u6267\u884C" }]
    }, options);
    return;
  }
  const cart2 = await backend.getCart(session.lastCartID);
  const unquotedServiceLine = [...cart2.items].reverse().find((item) => item.service_execution_id && !item.service_quote_lock_id);
  let envelope;
  if (unquotedServiceLine?.service_execution_id) {
    envelope = {
      status: "action_available",
      result: {
        cart_id: cart2.cart_id,
        cart_status: cart2.status,
        service_execution_id: unquotedServiceLine.service_execution_id
      },
      instruction: "\u8BE5 Cart \u5305\u542B service-backed line\uFF1B\u7EE7\u7EED Service Execution\uFF0C\u4E0D\u8981\u4ECE Cart \u731C capability\u3002",
      next: {
        command: `itpay services next ${unquotedServiceLine.service_execution_id} --json`,
        reason: "\u8BFB\u53D6\u670D\u52A1\u7AEF\u6700\u65B0\u6267\u884C\u72B6\u6001"
      },
      recovery: []
    };
  } else if (cart2.items.length === 0) {
    envelope = {
      status: "cart_empty",
      result: { cart_id: cart2.cart_id, cart_status: cart2.status },
      instruction: "Cart \u5F53\u524D\u4E3A\u7A7A\uFF1B\u5148\u8BFB\u53D6\u5DF2\u53D1\u5E03\u76EE\u5F55\uFF0C\u4E0D\u8981\u731C\u6D4B item \u6216 variant\u3002",
      next: { command: "itpay catalog list --json", reason: "\u9009\u62E9\u5DF2\u53D1\u5E03\u670D\u52A1" },
      recovery: []
    };
  } else {
    envelope = {
      status: "action_available",
      result: {
        cart_id: cart2.cart_id,
        cart_status: cart2.status,
        item_count: cart2.items.length,
        amount_minor: cart2.amount_minor,
        currency: cart2.currency
      },
      instruction: cart2.items.some((item) => item.service_quote_lock_id) ? "\u670D\u52A1\u62A5\u4EF7\u5DF2\u9501\u5B9A\u8F93\u5165\u548C\u4EF7\u683C\uFF1B\u786E\u8BA4\u9879\u76EE\u9F50\u5168\u540E\u4F7F\u7528\u540C\u4E00 Cart \u521B\u5EFA\u4E00\u6B21 Checkout\u3002" : "\u8BE5 Cart \u662F\u666E\u901A\u8D2D\u4E70\u6D41\u7A0B\uFF1B\u4F7F\u7528\u540C\u4E00 Cart \u521B\u5EFA Checkout\uFF0C\u4E0D\u8981\u91CD\u590D\u6DFB\u52A0\u5546\u54C1\u3002",
      next: { command: `itpay buy --cart ${cart2.cart_id} --json`, reason: "\u7EE7\u7EED canonical Cart \u7ED3\u7B97" },
      recovery: []
    };
  }
  writeCartNextEnvelope(envelope, options);
}
function writeCartNextEnvelope(envelope, options) {
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {}
  });
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/commands/docs.js
import { existsSync as existsSync4, readFileSync as readFileSync6, readdirSync } from "node:fs";
import { dirname as dirname4, resolve as resolve3 } from "node:path";
import { fileURLToPath } from "node:url";
var commandDir = dirname4(fileURLToPath(import.meta.url));
function runDocsList(options = {}) {
  const topics = loadDocs().map(({ topic, title, purpose }) => ({ topic, title, purpose }));
  writeCommandEnvelope({
    status: "listed",
    result: { topics },
    instruction: "\u9009\u62E9\u4E0E\u5F53\u524D\u6B65\u9AA4\u6700\u63A5\u8FD1\u7684\u4E00\u4E2A topic\uFF1B\u4E0D\u8981\u4E00\u6B21\u52A0\u8F7D\u5168\u90E8\u6587\u6863\u3002",
    next: null,
    recovery: []
  }, {
    ...options,
    plainResult: topics.flatMap((doc) => [`${doc.topic}: ${doc.title}`, `  ${doc.purpose}`])
  });
}
function runDocsShow(topic, options = {}) {
  const normalized = topic.trim();
  const doc = loadDocs().find((candidate) => candidate.topic === normalized);
  if (!doc) {
    throw new CommandContractError("doc_not_found", `doc topic not found: ${topic}`, "\u4F7F\u7528\u7A33\u5B9A topic \u540D\u79F0\uFF1B\u4E0D\u8981\u6839\u636E\u6807\u9898\u731C topic\u3002", [
      { command: "itpay docs list --json", reason: "\u5217\u51FA\u5168\u90E8 topic" },
      { command: `itpay docs search ${shellWord(normalized || "topic")} --json`, reason: "\u6309\u5173\u952E\u8BCD\u91CD\u65B0\u641C\u7D22" }
    ]);
  }
  const envelope = {
    status: "shown",
    result: { topic: doc.topic, content: doc },
    instruction: "\u53EA\u6267\u884C\u6587\u6863\u4E2D\u4E0E\u5F53\u524D\u670D\u52A1\u7AEF\u72B6\u6001\u5339\u914D\u7684\u6B65\u9AA4\uFF1B\u670D\u52A1\u7AEF\u8FD4\u56DE\u7684\u5F53\u524D next \u4F18\u5148\u3002",
    next: null,
    recovery: []
  };
  if (options.jsonOutput) {
    writeCommandEnvelope(envelope, options);
    return;
  }
  const out = resolveOutput(options.output);
  out("shown\n");
  out(`${JSON.stringify(doc, null, 2)}
`);
  out(`instruction: ${envelope.instruction}
`);
}
function runDocsSearch(query, options = {}) {
  const normalized = query.trim().toLowerCase();
  if (!normalized) {
    throw new CommandContractError("docs_query_required", "docs search query must not be empty", "\u63D0\u4F9B\u4E00\u4E2A topic\u3001\u6807\u9898\u3001\u7528\u9014\u6216 search term \u5173\u952E\u8BCD\u3002", [{ command: "itpay docs list --json", reason: "\u4E0D\u786E\u5B9A\u5173\u952E\u8BCD\u65F6\u5217\u51FA topic" }]);
  }
  const topics = loadDocs().filter((doc) => searchableText(doc).includes(normalized)).map(({ topic, title, purpose }) => ({ topic, title, purpose }));
  if (topics.length === 0) {
    writeCommandEnvelope({
      status: "no_match",
      result: { query, topics: [] },
      instruction: "\u6CA1\u6709\u5339\u914D\u6587\u6863\uFF1B\u7F29\u77ED\u5173\u952E\u8BCD\uFF0C\u6216\u5217\u51FA\u5168\u90E8 topic\u3002",
      next: { command: "itpay docs list --json", reason: "\u6D4F\u89C8\u7A33\u5B9A topic" },
      recovery: []
    }, options);
    return;
  }
  writeCommandEnvelope({
    status: "matched",
    result: { query, topics },
    instruction: topics.length === 1 ? "\u5DF2\u552F\u4E00\u5339\u914D\uFF1B\u8BFB\u53D6\u8BE5 topic\u3002" : "\u9009\u62E9\u6700\u76F8\u5173\u7684\u4E00\u4E2A topic\uFF1B\u4E0D\u8981\u540C\u65F6\u5C55\u5F00\u5168\u90E8\u7ED3\u679C\u3002",
    next: topics.length === 1 ? { command: `itpay docs show ${topics[0].topic} --json`, reason: "\u8BFB\u53D6\u552F\u4E00\u5339\u914D\u6587\u6863" } : null,
    recovery: []
  }, {
    ...options,
    plainResult: topics.map((doc) => `${doc.topic}: ${doc.title}`)
  });
}
function loadDocs() {
  const docsDir = findDocsDir();
  const files = readdirSync(docsDir).filter((file) => file.endsWith(".json")).sort();
  return files.map((file) => parseDoc(readFileSync6(resolve3(docsDir, file), "utf8"), file)).sort((left, right) => left.topic.localeCompare(right.topic));
}
function findDocsDir() {
  if (process.env.ITPAY_CLI_DOCS_DIR)
    return resolve3(process.env.ITPAY_CLI_DOCS_DIR);
  const packagePath = resolve3(commandDir, "..", "..", "..", "docs", "agent", "buyer");
  if (existsSync4(packagePath))
    return packagePath;
  return resolve3(commandDir, "..", "..", "docs", "agent", "buyer");
}
function parseDoc(raw, file) {
  const value = JSON.parse(raw);
  if (typeof value.schema_version !== "string" || typeof value.product_scope !== "string" || typeof value.topic !== "string" || typeof value.title !== "string" || typeof value.purpose !== "string") {
    throw new Error(`invalid agent doc: ${file}`);
  }
  return value;
}
function searchableText(doc) {
  return [doc.topic, doc.title, doc.purpose, ...doc.search_terms ?? []].join(" ").toLowerCase();
}
function shellWord(value) {
  return /^[a-zA-Z0-9._-]+$/.test(value) ? value : JSON.stringify(value);
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/commands/install.js
var INSTALL_AGENT_TYPES = [
  "codex-desktop",
  "codex-cli",
  "claude-code-desktop",
  "claude-code-cli",
  "workbuddy",
  "kimi-code",
  "openclaw"
];
var INSTRUCTIONS = {
  "codex-desktop": "\u5728 Codex Desktop \u4E2D\u59CB\u7EC8\u4F20\u8FD9\u4E2A Agent Type\uFF1B\u4ED8\u6B3E\u65F6\u628A\u8FD4\u56DE\u7684\u4E8C\u7EF4\u7801\u548C\u94FE\u63A5\u5B9E\u9645\u5C55\u793A\u5230\u5F53\u524D\u5BF9\u8BDD\u3002",
  "codex-cli": "\u5728 Codex CLI \u4E2D\u59CB\u7EC8\u4F20\u8FD9\u4E2A Agent Type\uFF1B\u4ED8\u6B3E\u4EA4\u63A5\u53EA\u5E94\u663E\u793A\u5728\u7528\u6237\u53EF\u89C1\u7EC8\u7AEF\u3002",
  "claude-code-desktop": "\u5728 Claude Code Desktop \u4E2D\u59CB\u7EC8\u4F20\u8FD9\u4E2A Agent Type\uFF1B\u4ED8\u6B3E\u65F6\u628A\u8FD4\u56DE\u7684\u4E8C\u7EF4\u7801\u548C\u94FE\u63A5\u5B9E\u9645\u5C55\u793A\u5230\u5F53\u524D\u5BF9\u8BDD\u3002",
  "claude-code-cli": "\u5728 Claude Code CLI \u4E2D\u59CB\u7EC8\u4F20\u8FD9\u4E2A Agent Type\uFF1B\u4ED8\u6B3E\u4EA4\u63A5\u53EA\u5E94\u663E\u793A\u5728\u7528\u6237\u53EF\u89C1\u7EC8\u7AEF\u3002",
  workbuddy: "\u5728 WorkBuddy \u4E2D\u59CB\u7EC8\u4F20\u8FD9\u4E2A Agent Type\u3002\u8FD0\u884C\u4F1A\u6301\u4E45\u5316 ~/.itpay-v3 \u7684 ItPay Bash \u547D\u4EE4\u524D\uFF0C\u628A Shell \u5DE5\u5177\u53C2\u6570 dangerouslyDisableSandbox \u8BBE\u4E3A true\uFF1B\u7528\u6237\u62D2\u7EDD\u6743\u9650\u65F6\u505C\u6B62\uFF0C\u4E0D\u8981\u5207\u6362 Node\u3001\u5220\u9664 identity \u6216\u5904\u7406 lock\u3002Checkout \u53EA\u8FD4\u56DE\u5DF2\u6E32\u67D3\u7684\u4ED8\u6B3E Card Link\uFF1B\u76F4\u63A5\u6253\u5F00 handoff.url\uFF0C\u4E0D\u8981\u8C03\u7528 present_files\uFF0C\u4E5F\u4E0D\u8981\u68C0\u67E5\u672C\u5730\u4E8C\u7EF4\u7801\u6587\u4EF6\u3002",
  "kimi-code": "\u4FDD\u6301 kimi-code Agent Type\uFF0C\u4F7F\u7528\u6807\u51C6 CLI \u547D\u4EE4\u548C\u7EC8\u7AEF\u4ED8\u6B3E\u4EA4\u63A5\uFF1B\u4E0D\u8981\u5207\u6362\u5230\u5176\u4ED6\u5E73\u53F0\u8EAB\u4EFD\u3002",
  openclaw: "\u4FDD\u6301 openclaw Agent Type\uFF1B\u6BCF\u4E2A\u5C55\u793A\u547D\u4EE4\u90FD\u4ECE\u5F53\u524D\u53EF\u4FE1\u4F1A\u8BDD\u4E0A\u4E0B\u6587\u663E\u5F0F\u4F20 --host\uFF0CIM \u5165\u53E3\u540C\u65F6\u4F20 --target\u3002Telegram \u4F7F\u7528\u8FD4\u56DE\u7684\u539F\u751F message action\uFF0C\u5176\u4ED6\u5165\u53E3\u5C55\u793A\u6807\u51C6\u4E8C\u7EF4\u7801\u548C\u4ED8\u6B3E\u94FE\u63A5\u3002"
};
function runInstall(target, options = {}) {
  if (!target || target === "list") {
    const agentTypes = INSTALL_AGENT_TYPES.map(installDefinition);
    writeCommandEnvelope({
      status: "install_targets",
      result: { agent_types: agentTypes },
      instruction: "\u9009\u62E9\u5F53\u524D\u771F\u5B9E\u8FD0\u884C\u73AF\u5883\uFF1B\u540C\u4E00 Agent \u4E0D\u8981\u4E34\u65F6\u66F4\u6362 Agent Type\u3002",
      next: null,
      recovery: [{ command: "itpay docs show install-and-setup", reason: "\u67E5\u770B\u5B89\u88C5\u4E0E\u73AF\u5883\u8BF4\u660E" }]
    }, {
      ...options,
      plainResult: agentTypes.map((item) => `${item.agent_type}: ${item.default_host ?? "explicit --host required"}`)
    });
    return;
  }
  const normalized = target.trim().toLowerCase();
  if (!isInstallAgentType(normalized)) {
    throw new CommandContractError("unsupported_agent_type", `unsupported install target: ${target}`, `target \u53EA\u63A5\u53D7\uFF1A${INSTALL_AGENT_TYPES.join(", ")}\u3002`, [{ command: "itpay install --json", reason: "\u5217\u51FA\u6B63\u5F0F\u652F\u6301\u7684 Agent Type" }]);
  }
  writeCommandEnvelope({
    status: "instructions_ready",
    result: {
      ...installDefinition(normalized),
      default_api: DEFAULT_BASE_URL
    },
    instruction: INSTRUCTIONS[normalized],
    next: {
      command: `itpay --agent-type ${normalized} readyz --json`,
      reason: "\u9A8C\u8BC1\u5F53\u524D\u5B98\u65B9 ItPay API \u7684\u53EF\u7528\u6027"
    },
    recovery: [{ command: "itpay docs show install-and-setup", reason: "\u67E5\u770B\u5B98\u65B9 Backend \u548C\u9996\u6B21\u4F7F\u7528\u8BF4\u660E" }]
  }, options);
}
function isInstallAgentType(value) {
  return INSTALL_AGENT_TYPES.includes(value);
}
function installDefinition(agentType) {
  if (agentType === "openclaw") {
    return { agent_type: agentType, default_host: null, host_required: true, native_hosts: ["telegram"] };
  }
  return { agent_type: agentType, default_host: defaultHostForAgentType(agentType) ?? null };
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/commands/skill.js
import { existsSync as existsSync5, readFileSync as readFileSync7 } from "node:fs";
import { dirname as dirname5, resolve as resolve4 } from "node:path";
import { fileURLToPath as fileURLToPath2 } from "node:url";
var commandDir2 = dirname5(fileURLToPath2(import.meta.url));
var ITPAY_SKILL = "itpay";
function runSkillShow(name, options = {}) {
  const normalized = name.trim().toLowerCase();
  if (normalized !== ITPAY_SKILL) {
    throw new CommandContractError("skill_not_found", `skill not found: ${name}`, `\u5F53\u524D CLI \u53EA\u5185\u7F6E ${ITPAY_SKILL}\uFF1B\u4E0D\u8981\u731C\u6D4B Skill \u540D\u79F0\u3002`, [{ command: `itpay skill show ${ITPAY_SKILL} --json`, reason: "\u8BFB\u53D6\u5B8C\u6574 ItPay Skill" }]);
  }
  let content;
  try {
    content = readFileSync7(findSkillPath(), "utf8");
  } catch {
    throw new Error("packaged skill is unavailable: itpay");
  }
  validateSkill(content);
  const agentType = options.agentType ?? declaredAgentType();
  const envelope = {
    status: "shown",
    result: { skill: ITPAY_SKILL, content },
    instruction: agentType ? agentType === "workbuddy" ? "\u5B8C\u6574\u8BFB\u53D6\u5E76\u9075\u5B88 Skill\uFF1B\u4FDD\u6301 workbuddy \u548C\u540C\u4E00 Node/CLI launcher\u3002\u8FD0\u884C\u4F1A\u6301\u4E45\u5316 ~/.itpay-v3 \u7684 ItPay Bash \u547D\u4EE4\u524D\uFF0C\u628A Shell \u5DE5\u5177\u53C2\u6570 dangerouslyDisableSandbox \u8BBE\u4E3A true\uFF1B\u7528\u6237\u62D2\u7EDD\u6743\u9650\u65F6\u505C\u6B62\uFF0C\u4E0D\u8981\u5207\u6362 Node\u3001\u5220\u9664 identity \u6216\u5904\u7406 lock\u3002" : `\u5B8C\u6574\u8BFB\u53D6\u5E76\u9075\u5B88 Skill\uFF1B\u5F53\u524D Agent Type \u662F ${agentType}\uFF0C\u540E\u7EED\u547D\u4EE4\u4FDD\u6301\u4E0D\u53D8\u3002` : "\u5B8C\u6574\u8BFB\u53D6\u5E76\u9075\u5B88 Skill\uFF1B\u5148\u5982\u5B9E\u9009\u62E9\u5F53\u524D\u8FD0\u884C\u73AF\u5883\u5BF9\u5E94\u7684 Agent Type\u3002",
    next: agentType ? { command: "itpay catalog list --json", reason: "\u6309 Skill \u5F00\u59CB\u53D1\u73B0\u670D\u52A1" } : { command: "itpay install --json", reason: "\u9009\u62E9\u771F\u5B9E\u4E14\u7A33\u5B9A\u7684 Agent Type" },
    recovery: []
  };
  writeCommandEnvelope(envelope, {
    ...options,
    ...agentType ? { agentType } : {},
    plainResult: content.replace(/\r\n/g, "\n").replace(/\n$/, "").split("\n")
  });
}
function findSkillPath() {
  if (process.env.ITPAY_CLI_SKILLS_DIR) {
    const configuredRoot = resolve4(process.env.ITPAY_CLI_SKILLS_DIR);
    const directPath = resolve4(configuredRoot, "SKILL.md");
    if (existsSync5(directPath))
      return directPath;
    return resolve4(configuredRoot, ITPAY_SKILL, "SKILL.md");
  }
  const packagePath = resolve4(commandDir2, "..", "..", "..", "skills", ITPAY_SKILL, "SKILL.md");
  if (existsSync5(packagePath))
    return packagePath;
  return resolve4(commandDir2, "..", "..", "skills", ITPAY_SKILL, "SKILL.md");
}
function validateSkill(content) {
  const frontmatter = content.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/)?.[1];
  if (!frontmatter || !/^name:\s*itpay\s*$/m.test(frontmatter) || !/^description:\s*(?:>|\S)/m.test(frontmatter)) {
    throw new Error("invalid packaged skill: itpay");
  }
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/commands/next.js
function runNext(session, options = {}) {
  const envelope = nextEnvelope(session);
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {}
  });
}
function nextEnvelope(session) {
  if (session.stateLoadFailed) {
    return {
      status: "local_state_invalid",
      result: {},
      instruction: "\u672C\u5730\u6062\u590D\u53E5\u67C4\u65E0\u6CD5\u8BFB\u53D6\uFF1B\u4E0D\u8981\u731C\u6D4B\u8D44\u6E90 ID\uFF0C\u6539\u4ECE\u5F53\u524D\u8BBE\u5907\u53EF\u89C1\u7684\u670D\u52A1\u6267\u884C\u6062\u590D\u3002",
      next: { command: "itpay services list --json", reason: "\u4ECE\u670D\u52A1\u7AEF\u6062\u590D\u5F53\u524D\u8BBE\u5907\u53EF\u89C1\u7684\u6267\u884C" },
      recovery: []
    };
  }
  const state = session.show();
  if (state.lastServiceExecutionID) {
    return resumeEnvelope("service_execution", state.lastServiceExecutionID, `itpay services next ${state.lastServiceExecutionID} --json`, "\u8BFB\u53D6\u670D\u52A1\u7AEF\u6700\u65B0\u72B6\u6001");
  }
  if (state.lastCheckoutID && state.lastDisplayToken) {
    return resumeEnvelope("checkout", state.lastCheckoutID, `itpay checkout --id ${state.lastCheckoutID} --token ${state.lastDisplayToken} --json`, "\u6062\u590D\u540C\u4E00 Checkout");
  }
  if (state.lastCartID) {
    return resumeEnvelope("cart", state.lastCartID, "itpay cart next --json", "\u8BFB\u53D6\u540C\u4E00 Cart \u7684\u670D\u52A1\u7AEF\u72B6\u6001");
  }
  return {
    status: "nothing_to_resume",
    result: {},
    instruction: "\u672C\u5730\u6CA1\u6709\u53EF\u6062\u590D\u53E5\u67C4\uFF1B\u5148\u8BFB\u53D6\u5DF2\u53D1\u5E03\u76EE\u5F55\uFF0C\u4E0D\u8981\u731C\u6D4B service_id\u3002",
    next: { command: "itpay catalog list --json", reason: "\u9009\u62E9\u5DF2\u53D1\u5E03\u670D\u52A1" },
    recovery: []
  };
}
function resumeEnvelope(resourceType, resourceID, command, reason) {
  return {
    status: "resume_available",
    result: { resource_type: resourceType, resource_id: resourceID },
    instruction: "\u7EE7\u7EED\u5DF2\u6709\u8D44\u6E90\uFF0C\u4E0D\u8981\u521B\u5EFA\u91CD\u590D\u8BA2\u5355\u6216 Checkout\u3002",
    next: { command, reason },
    recovery: []
  };
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/commands/services.js
var serviceActionStatuses = /* @__PURE__ */ new Set(["pending", "approved", "rejected", "expired", "cancelled"]);
async function runServicesStart(backend, serviceID, options = {}) {
  const host = options.host ?? "terminal";
  const response = await backend.startServiceExecution({
    service_id: serviceID,
    client_context: {
      host,
      ...options.target ? { target: options.target } : {},
      ...options.clientContext ?? {}
    }
  });
  const capability = response.capabilities.find((item) => item.phase === response.execution.phase && !item.requires_payment);
  const requiredInput = requiredInputFields(capability?.input_schema);
  const command = capability ? `itpay services invoke ${response.execution.service_execution_id} --capability ${capability.capability_id}${requiredInput.map((field) => ` --input ${field}=<value>`).join("")} --json` : `itpay services next ${response.execution.service_execution_id} --json`;
  const capabilitySummary = capability ? {
    capability_id: capability.capability_id,
    required_input: requiredInput,
    ...capability.free_quota_limit !== void 0 ? { free_quota_limit: capability.free_quota_limit } : {}
  } : null;
  writeCommandEnvelope({
    status: "ready",
    result: {
      service_execution_id: response.execution.service_execution_id,
      service_id: response.execution.service_id,
      phase: response.execution.phase,
      capability: capabilitySummary
    },
    instruction: capability ? "\u586B\u5199\u9996\u9009 capability \u7684 required_input\uFF1B\u4E00\u6B21\u53EA\u63D0\u4EA4\u5F53\u524D execution \u6240\u4EE3\u8868\u7684\u670D\u52A1\u610F\u56FE\u3002" : "\u5F53\u524D\u6CA1\u6709\u53EF\u76F4\u63A5\u8C03\u7528\u7684 capability\uFF1B\u8BFB\u53D6\u670D\u52A1\u7AEF\u4E0B\u4E00\u6B65\uFF0C\u4E0D\u8981\u731C\u6D4B capability\u3002",
    next: {
      command,
      reason: capability ? "\u6267\u884C\u5F53\u524D\u5141\u8BB8\u7684\u80FD\u529B" : "\u8BFB\u53D6\u670D\u52A1\u7AEF\u8BA1\u7B97\u7684\u4E0B\u4E00\u6B65"
    },
    recovery: []
  }, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {},
    plainResult: [
      `service_execution_id: ${response.execution.service_execution_id}`,
      `service_id: ${response.execution.service_id}`,
      `phase: ${response.execution.phase}`,
      ...capability ? [
        `capability: ${capability.capability_id}`,
        `required_input: ${requiredInput.length > 0 ? requiredInput.join(",") : "none"}`,
        ...capability.free_quota_limit !== void 0 ? [`free_quota_limit: ${capability.free_quota_limit}`] : []
      ] : []
    ]
  });
}
function requiredInputFields(schema) {
  const required = schema?.required;
  return Array.isArray(required) ? required.filter((field) => typeof field === "string") : [];
}
async function runServicesInvoke(backend, config, serviceExecutionID, capabilityID, input, options = {}) {
  const readModel = await backend.getServiceExecution(serviceExecutionID);
  const requestedCapability = readModel.capabilities.find((capability) => capability.capability_id === capabilityID);
  if (!requestedCapability) {
    throw new CommandContractError("capability_not_found", `capability ${capabilityID} is not available on service execution ${serviceExecutionID}`, "\u4F7F\u7528 Service Execution \u5F53\u524D\u8FD4\u56DE\u7684 capability_id\uFF0C\u4E0D\u8981\u731C\u6D4B\u540D\u79F0\u3002", [{ command: `itpay services next ${serviceExecutionID} --json`, reason: "\u8BFB\u53D6\u5F53\u524D\u53EF\u7528 capability" }]);
  }
  if (requestedCapability.requires_payment) {
    throw new CommandContractError("checkout_required", `capability ${capabilityID} requires checkout and cannot be invoked directly`, "\u4ED8\u8D39 capability \u4E0D\u80FD\u76F4\u63A5 invoke\u3002\u4E0D\u8981\u5C1D\u8BD5 quote\u3001cart\u3001buy\u3001checkout \u6216 pay \u4F5C\u4E3A\u65C1\u8DEF\uFF1B\u53EA\u6062\u590D\u540C\u4E00 Execution \u7684\u5F53\u524D\u5408\u6CD5\u52A8\u4F5C\u3002", [{ command: `itpay services next ${serviceExecutionID} --json`, reason: "\u8BFB\u53D6\u540C\u4E00 Execution \u7684\u5F53\u524D\u5408\u6CD5\u52A8\u4F5C" }]);
  }
  const missingInput = missingRequiredInput(requestedCapability.input_schema, input);
  if (missingInput.length > 0) {
    const correctedInput = { ...input };
    for (const field of missingInput)
      correctedInput[field] = "<value>";
    throw new CommandContractError("capability_input_invalid", `missing required capability input: ${missingInput.join(", ")}`, "\u8865\u9F50 required_input \u540E\u91CD\u8BD5\u540C\u4E00\u4E2A execution\uFF1B\u672C\u6B21\u6CA1\u6709\u8C03\u7528 Provider\u3002", [{
      command: `itpay services invoke ${serviceExecutionID} --capability ${capabilityID}${formatInputOptions(correctedInput)} --json`,
      reason: "\u63D0\u4EA4\u5B8C\u6574 capability \u8F93\u5165"
    }]);
  }
  const idempotencyKey = await operationID(config, `service.invoke:${serviceExecutionID}:${capabilityID}:${stableInput(input)}`);
  const response = await backend.invokeServiceCapability(serviceExecutionID, capabilityID, {
    idempotency_key: idempotencyKey,
    redacted_summary: input
  });
  const envelope = invokedEnvelope(response, requestedCapability, readModel.capabilities, input);
  writeCommandEnvelope(envelope.value, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {},
    plainResult: envelope.plainResult
  });
}
function invokedEnvelope(response, requestedCapability, capabilities, input) {
  const items = response.result_items.map((item) => ({
    rank: item.rank,
    title: item.display_title,
    safe_payload: item.safe_payload
  }));
  const quota = response.effective_quota ? { remaining: response.effective_quota.remaining, limit: response.effective_quota.limit } : void 0;
  const baseResult = {
    service_execution_id: response.execution.service_execution_id,
    capability_id: requestedCapability.capability_id,
    query: input,
    items,
    ...quota ? { quota } : {}
  };
  let status = items.length > 0 ? "result_ready" : "no_result";
  let instruction = items.length > 0 ? "\u5411\u7528\u6237\u5C55\u793A\u7F16\u53F7\u548C safe_payload\uFF1B\u82E5\u5019\u9009\u5217\u8868\u5DF2\u6EE1\u8DB3\u7528\u6237\u76EE\u6807\uFF0C\u5728\u6B64\u505C\u6B62\u3002\u4EC5\u5728\u7528\u6237\u660E\u786E\u9009\u62E9\u5E76\u5E0C\u671B\u7EE7\u7EED\u65F6\uFF0C\u624D\u5728\u5F53\u524D Execution \u63D0\u4EA4\u5BF9\u5E94 rank\u3002" : `\u6CA1\u6709\u627E\u5230\u4E0E\u201C${queryText(input)}\u201D\u5339\u914D\u7684\u7ED3\u679C\u3002\u5411\u7528\u6237\u5C55\u793A\u672C\u6B21\u4E3A 0 \u4E2A\u7ED3\u679C\u5E76\u505C\u6B62\u3002\u4E0D\u8981\u4FEE\u6539\u3001\u7F29\u77ED\u6216\u731C\u6D4B\u5176\u4ED6\u8F93\u5165\uFF1B\u53EA\u6709\u7528\u6237\u660E\u786E\u63D0\u4F9B\u65B0\u8F93\u5165\u540E\uFF0C\u624D\u80FD\u542F\u52A8\u65B0\u7684\u67E5\u8BE2\u3002`;
  let next = null;
  if (response.effective_quota?.exhausted) {
    status = "quota_exhausted";
    instruction = "\u514D\u8D39\u989D\u5EA6\u5DF2\u7528\u5B8C\u4E14\u672C\u6B21\u6CA1\u6709\u8C03\u7528 Provider\u3002\u5F53\u524D\u6CA1\u6709\u53EF\u8D2D\u4E70\u7684 continuation\uFF1B\u53EA\u8BFB\u53D6\u540C\u4E00 Execution \u7684\u670D\u52A1\u7AEF\u6062\u590D\u65B9\u5411\u3002";
    const checkoutAction = response.next_actions?.find((action) => action.kind === "create_checkout");
    const checkoutCapability = capabilities.find((capability) => capability.capability_id === checkoutAction?.capability_id);
    if (checkoutCapability) {
      baseResult.checkout = {
        capability_id: checkoutCapability.capability_id,
        ...checkoutCapability.price_amount_minor !== void 0 && checkoutCapability.price_currency ? {
          price: { amount_minor: checkoutCapability.price_amount_minor, currency: checkoutCapability.price_currency }
        } : {},
        delivery_email_required: checkoutCapability.delivery_email_required
      };
      const price = capabilityPrice(checkoutCapability);
      instruction = purchaseConfirmationInstruction("quota_exhausted", price, checkoutCapability.delivery_email_required, checkoutCapability.delivery_email_purpose);
      next = {
        command: checkoutCommand(response.execution.service_execution_id, checkoutCapability, input),
        reason: `\u4EC5\u5728\u7528\u6237\u660E\u786E\u540C\u610F\u652F\u4ED8 ${price} \u540E\u6267\u884C\uFF1B\u5426\u5219\u505C\u6B62`
      };
    } else {
      next = {
        command: `itpay services next ${response.execution.service_execution_id} --json`,
        reason: "\u8BFB\u53D6\u670D\u52A1\u7AEF\u63D0\u4F9B\u7684\u4ED8\u8D39\u6062\u590D\u5165\u53E3"
      };
    }
  } else if (items.length > 0 && requestedCapability.requires_human_action) {
    next = {
      command: `itpay services action ${response.execution.service_execution_id} --action select_candidate --actor-type human --status approved --candidate <rank> --json`,
      reason: "\u5728\u5F53\u524D Execution \u8BB0\u5F55\u7528\u6237\u9009\u62E9"
    };
  } else if (items.length === 0) {
    next = null;
  }
  return {
    value: { status, result: baseResult, instruction, next, recovery: [] },
    plainResult: serviceResultPlainLines(baseResult)
  };
}
function serviceResultPlainLines(result) {
  const lines = [
    `service_execution_id: ${String(result.service_execution_id)}`,
    `capability_id: ${String(result.capability_id)}`
  ];
  const items = result.items;
  const query = result.query;
  if (query) {
    for (const [key, value] of Object.entries(query))
      lines.push(`${key}: ${String(value)}`);
  }
  if (items.length === 0)
    lines.push("results: 0");
  if (result.quota)
    lines.push(`quota: ${JSON.stringify(result.quota)}`);
  if (result.checkout)
    lines.push(`checkout: ${JSON.stringify(result.checkout)}`);
  if (items.length > 0) {
    lines.push("items:");
    for (const item of items) {
      lines.push(`  ${item.rank}. ${item.title}`);
      for (const [key, value] of Object.entries(item.safe_payload)) {
        lines.push(`     ${key}: ${typeof value === "string" ? value : JSON.stringify(value)}`);
      }
    }
  }
  return lines;
}
function queryText(input) {
  const value = Object.values(input).find((item) => typeof item === "string" && item.trim() !== "");
  return typeof value === "string" ? value : JSON.stringify(input);
}
function missingRequiredInput(schema, input) {
  return requiredInputFields(schema).filter((field) => {
    if (!(field in input) || input[field] === null || input[field] === void 0)
      return true;
    return typeof input[field] === "string" && String(input[field]).trim() === "";
  });
}
function checkoutCommand(serviceExecutionID, capability, input, fillMissing = true) {
  const lockedInput = { ...input };
  if (fillMissing) {
    for (const field of missingRequiredInput(capability.input_schema, lockedInput))
      lockedInput[field] = "<value>";
  }
  return `itpay services checkout ${serviceExecutionID} --capability ${capability.capability_id}${formatInputOptions(lockedInput)}${capability.delivery_email_required ? " --email <email>" : ""} --json`;
}
function capabilityPrice(capability) {
  return capability.price_amount_minor !== void 0 && capability.price_currency ? formatMoney3(capability.price_amount_minor, capability.price_currency) : "\u5F53\u524D\u53D1\u5E03\u4EF7\u683C";
}
function purchaseConfirmationInstruction(context, price, deliveryEmailRequired, deliveryEmailPurpose, candidateTitle = "") {
  const emailPurpose = deliveryEmailPurposeText(deliveryEmailPurpose);
  if (context === "quota_exhausted") {
    return deliveryEmailRequired ? `\u514D\u8D39\u989D\u5EA6\u5DF2\u7528\u5B8C\uFF0C\u672C\u6B21\u6CA1\u6709\u8C03\u7528 Provider\uFF0C\u4E5F\u5C1A\u672A\u521B\u5EFA Quote \u6216 Checkout\u3002\u73B0\u5728\u53EA\u5411\u7528\u6237\u8BF4\u660E\uFF1A\u7EE7\u7EED\u5F53\u524D\u8BF7\u6C42\u9700\u8981\u652F\u4ED8 ${price}\uFF0C\u5E76\u63D0\u4F9B${emailPurpose}\uFF1B\u8BF7\u786E\u8BA4\u662F\u5426\u8D2D\u4E70\u5E76\u63D0\u4F9B\u90AE\u7BB1\u3002\u7136\u540E\u505C\u6B62\u5E76\u7B49\u5F85\u3002\u7528\u6237\u660E\u786E\u540C\u610F\u5E76\u63D0\u4F9B\u771F\u5B9E\u90AE\u7BB1\u524D\uFF0C\u4E0D\u8981\u6267\u884C next.command\uFF0C\u4E0D\u8981\u65B0\u5EFA Execution\uFF0C\u4E0D\u8981\u5C1D\u8BD5\u5176\u4ED6 capability\u3001quote\u3001cart\u3001buy\u3001checkout \u6216 pay \u547D\u4EE4\u3002` : `\u514D\u8D39\u989D\u5EA6\u5DF2\u7528\u5B8C\uFF0C\u672C\u6B21\u6CA1\u6709\u8C03\u7528 Provider\uFF0C\u4E5F\u5C1A\u672A\u521B\u5EFA Quote \u6216 Checkout\u3002\u73B0\u5728\u53EA\u5411\u7528\u6237\u8BF4\u660E\uFF1A\u201C\u7EE7\u7EED\u5F53\u524D\u8BF7\u6C42\u9700\u8981\u652F\u4ED8 ${price}\uFF0C\u662F\u5426\u8D2D\u4E70\uFF1F\u201D\u7136\u540E\u505C\u6B62\u5E76\u7B49\u5F85\u7528\u6237\u660E\u786E\u56DE\u590D\u3002\u7528\u6237\u660E\u786E\u540C\u610F\u524D\uFF0C\u4E0D\u8981\u6267\u884C next.command\uFF0C\u4E0D\u8981\u65B0\u5EFA Execution\uFF0C\u4E0D\u8981\u5C1D\u8BD5\u5176\u4ED6 capability\u3001quote\u3001cart\u3001buy\u3001checkout \u6216 pay \u547D\u4EE4\u3002`;
  }
  const selected = candidateTitle ? `\u5DF2\u9009\u62E9 ${candidateTitle}\u3002` : "\u5F53\u524D\u5019\u9009\u5DF2\u7ECF\u786E\u8BA4\u3002";
  return deliveryEmailRequired ? `${selected}\u5019\u9009\u5DF2\u7ED1\u5B9A\u5230\u5F53\u524D Execution\uFF0C\u4F46\u5C1A\u672A\u8D2D\u4E70\u540E\u7EED\u670D\u52A1\u3002\u73B0\u5728\u53EA\u5411\u7528\u6237\u8BF4\u660E\uFF1A\u7EE7\u7EED\u8D2D\u4E70\u540E\u7EED\u670D\u52A1\u9700\u8981\u652F\u4ED8 ${price}\uFF0C\u5E76\u63D0\u4F9B${emailPurpose}\uFF1B\u8BF7\u786E\u8BA4\u662F\u5426\u8D2D\u4E70\u5E76\u63D0\u4F9B\u90AE\u7BB1\u3002\u7136\u540E\u505C\u6B62\u3002\u7528\u6237\u660E\u786E\u540C\u610F\u5E76\u63D0\u4F9B\u771F\u5B9E\u90AE\u7BB1\u524D\uFF0C\u4E0D\u8981\u6267\u884C next.command\uFF0C\u4E0D\u8981\u521B\u5EFA\u65B0 Execution \u6216 Checkout\u3002` : `${selected}\u5019\u9009\u5DF2\u7ED1\u5B9A\u5230\u5F53\u524D Execution\uFF0C\u4F46\u5C1A\u672A\u8D2D\u4E70\u540E\u7EED\u670D\u52A1\u3002\u73B0\u5728\u53EA\u5411\u7528\u6237\u8BF4\u660E\uFF1A\u201C\u7EE7\u7EED\u8D2D\u4E70\u540E\u7EED\u670D\u52A1\u9700\u8981\u652F\u4ED8 ${price}\uFF0C\u662F\u5426\u8D2D\u4E70\uFF1F\u201D\u7136\u540E\u505C\u6B62\u3002\u7528\u6237\u660E\u786E\u540C\u610F\u524D\uFF0C\u4E0D\u8981\u6267\u884C next.command\uFF0C\u4E0D\u8981\u521B\u5EFA\u65B0 Execution \u6216 Checkout\u3002`;
}
function deliveryEmailPurposeText(purpose) {
  switch (purpose) {
    case "receipt":
      return "\u7528\u4E8E\u53D1\u9001\u8BA2\u5355\u6536\u636E\u7684\u771F\u5B9E\u90AE\u7BB1";
    case "claim":
      return "\u7528\u4E8E\u53D1\u9001\u4EA4\u4ED8\u8BA4\u9886\u94FE\u63A5\u7684\u771F\u5B9E\u90AE\u7BB1";
    case "receipt_and_claim":
      return "\u7528\u4E8E\u53D1\u9001\u8BA2\u5355\u6536\u636E\u548C\u4EA4\u4ED8\u8BA4\u9886\u94FE\u63A5\u7684\u771F\u5B9E\u90AE\u7BB1";
    default:
      return "\u670D\u52A1\u7AEF\u58F0\u660E\u7528\u9014\u7684\u771F\u5B9E\u90AE\u7BB1";
  }
}
function paidContinuation(model, action, input) {
  if (!action.capability_id)
    return null;
  const capability = model.capabilities.find((item) => item.capability_id === action.capability_id && item.requires_payment);
  if (!capability)
    return null;
  const price = capabilityPrice(capability);
  const stateBacked = model.execution.status === "quota_exhausted" || model.execution.status === "human_action_approved";
  return {
    capability,
    price,
    checkout: {
      capability_id: capability.capability_id,
      ...capability.price_amount_minor !== void 0 && capability.price_currency ? {
        price: { amount_minor: capability.price_amount_minor, currency: capability.price_currency }
      } : {},
      delivery_email_required: capability.delivery_email_required,
      ...capability.delivery_email_purpose ? { delivery_email_purpose: capability.delivery_email_purpose } : {}
    },
    next: {
      command: checkoutCommand(model.execution.service_execution_id, capability, input, !stateBacked),
      reason: `\u4EC5\u5728\u7528\u6237\u660E\u786E\u540C\u610F\u652F\u4ED8 ${price}${capability.delivery_email_required ? " \u5E76\u63D0\u4F9B\u771F\u5B9E\u90AE\u7BB1" : ""}\u540E\u6267\u884C\uFF1B\u5426\u5219\u505C\u6B62`
    }
  };
}
function quoteCommand(serviceExecutionID, capability, input) {
  const lockedInput = { ...input };
  for (const field of missingRequiredInput(capability.input_schema, lockedInput))
    lockedInput[field] = "<value>";
  return `itpay services quote ${serviceExecutionID} --capability ${capability.capability_id}${formatInputOptions(lockedInput)}${capability.delivery_email_required ? " --email <email>" : ""} --json`;
}
function stableInput(input) {
  return JSON.stringify(Object.fromEntries(Object.entries(input).sort(([left], [right]) => left.localeCompare(right))));
}
function formatInputOptions(input) {
  return Object.entries(input).sort(([left], [right]) => left.localeCompare(right)).map(([key, value]) => String(value) === "<value>" ? ` --input ${key}=<value>` : ` --input ${shellArgument(`${key}=${String(value)}`)}`).join("");
}
function shellArgument(value) {
  if (/^[\p{L}\p{N}._:=/-]+$/u.test(value))
    return value;
  return `'${value.replaceAll("'", `'"'"'`)}'`;
}
async function runServicesAction(backend, serviceExecutionID, actionType, input, options = {}) {
  const selection = await resolveCandidateSelection(backend, serviceExecutionID, actionType, options);
  const request = {
    action_type: actionType,
    input_snapshot: input
  };
  if (options.actorType)
    request.actor_type = options.actorType;
  if (options.actorID)
    request.actor_id = options.actorID;
  if (options.status)
    request.status = normalizeServiceActionStatus(options.status, serviceExecutionID);
  const resultItemID = selection?.resultItemID ?? options.resultItemID;
  if (resultItemID)
    request.result_item_id = resultItemID;
  if (options.requiredBefore)
    request.required_before = options.requiredBefore;
  const response = await backend.recordServiceExecutionAction(serviceExecutionID, request);
  if (selection && actionType === "select_candidate" && response.status === "approved") {
    const updated = await backend.getServiceExecution(serviceExecutionID);
    const preferred = updated.allowed_actions?.[0];
    const continuation = preferred?.type === "prepare_quote" ? paidContinuation(updated, preferred, {}) : null;
    const next = continuation?.next ?? (preferred ? serviceAllowedActionCommand(updated, preferred) : null);
    writeCommandEnvelope({
      status: "candidate_selected",
      result: {
        service_execution_id: response.service_execution_id,
        candidate: { rank: selection.rank, title: selection.title },
        ...continuation ? { checkout: continuation.checkout } : {}
      },
      instruction: continuation ? purchaseConfirmationInstruction("candidate_selected", continuation.price, continuation.capability.delivery_email_required, continuation.capability.delivery_email_purpose, selection.title) : "\u5019\u9009\u5DF2\u7ED1\u5B9A\u5230\u6765\u6E90 Execution\uFF1B\u540E\u7EED\u52A8\u4F5C\u5FC5\u987B\u7EE7\u7EED\u4F7F\u7528\u8BE5 Execution\u3002",
      next,
      recovery: [{
        command: `itpay services next ${response.service_execution_id} --json`,
        reason: "\u91CD\u65B0\u8BFB\u53D6\u670D\u52A1\u7AEF\u5141\u8BB8\u7684\u52A8\u4F5C"
      }]
    }, {
      ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
      ...options.output ? { output: options.output } : {}
    });
    return;
  }
  writeCommandEnvelope({
    status: "action_recorded",
    result: {
      service_execution_id: response.service_execution_id,
      action_type: response.action_type,
      action_status: response.status
    },
    instruction: "\u52A8\u4F5C\u5DF2\u8BB0\u5F55\uFF0C\u8BFB\u53D6\u670D\u52A1\u7AEF\u8BA1\u7B97\u7684\u65B0\u72B6\u6001\uFF1B\u4E0D\u8981\u81EA\u884C\u5047\u8BBE\u4E0B\u4E00 capability\u3002",
    next: {
      command: `itpay services next ${response.service_execution_id} --json`,
      reason: "\u53D6\u5F97\u66F4\u65B0\u540E\u7684\u9996\u9009\u52A8\u4F5C"
    },
    recovery: []
  }, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {}
  });
}
async function resolveCandidateSelection(backend, serviceExecutionID, actionType, options) {
  if (options.candidateRank === void 0)
    return void 0;
  if (actionType !== "select_candidate") {
    throw actionInputError(serviceExecutionID, "--candidate is only valid with --action select_candidate");
  }
  if (options.resultItemID) {
    throw actionInputError(serviceExecutionID, "--candidate cannot be combined with --result-item");
  }
  if (!Number.isInteger(options.candidateRank) || options.candidateRank < 1) {
    throw actionInputError(serviceExecutionID, "--candidate must be a positive integer result rank");
  }
  const execution = await backend.getServiceExecution(serviceExecutionID);
  const currentItems = execution.current_result_items ?? [];
  const result = currentItems.find((item) => item.rank === options.candidateRank);
  if (!result) {
    throw actionInputError(serviceExecutionID, `candidate ${options.candidateRank} is not available on service execution ${serviceExecutionID}`, "candidate_not_found");
  }
  return {
    resultItemID: result.service_capability_result_item_id,
    rank: result.rank,
    title: result.display_title
  };
}
function actionInputError(serviceExecutionID, message, code = "service_action_invalid") {
  return new CommandContractError(code, message, code === "candidate_not_found" ? "\u5F53\u524D rank \u4E0D\u5B58\u5728\u6216\u5F53\u524D\u5019\u9009\u96C6\u4E0D\u53EF\u7528\u3002\u4E0D\u8981\u65B0\u5EFA Execution\uFF0C\u4E0D\u8981\u91CD\u65B0 invoke\uFF0C\u4E0D\u8981\u6784\u9020\u5019\u9009 ID\uFF1B\u53EA\u6062\u590D\u540C\u4E00 Execution \u5F53\u524D\u4ECD\u7136\u6709\u6548\u7684\u5019\u9009\u3002" : "\u4F7F\u7528\u5F53\u524D safe result \u4E2D\u7684\u5408\u6CD5 action \u548C candidate rank\uFF1B\u9700\u8981\u4EBA\u786E\u8BA4\u65F6\u5148\u8BE2\u95EE\u7528\u6237\u3002", [{ command: `itpay services next ${serviceExecutionID} --json`, reason: "\u91CD\u65B0\u8BFB\u53D6\u540C\u4E00 Execution \u7684\u5F53\u524D\u53EF\u9009\u52A8\u4F5C" }]);
}
async function runServicesCheckout(backend, config, serviceExecutionID, capabilityID, options = {}) {
  const host = options.host ?? "terminal";
  const contextError = validateContext(host, options.target);
  if (contextError) {
    throw new CommandContractError(contextError.code, contextError.message, "\u4ECE\u5F53\u524D\u53EF\u4FE1\u4F1A\u8BDD\u4E0A\u4E0B\u6587\u8865\u9F50 Host/target\uFF1B\u672C\u6B21\u672A\u521B\u5EFA Checkout\u3002", []);
  }
  const deliveryContact = {
    ...options.deliveryContact ?? {},
    ...options.email ? { email: options.email } : {}
  };
  if (!options.resume && !capabilityID) {
    throw new CommandContractError("capability_required", "--capability is required when creating a service checkout", "\u4F7F\u7528\u5F53\u524D Service Execution \u8FD4\u56DE\u7684\u4ED8\u8D39 capability\uFF1B\u6062\u590D\u5DF2\u6709 Checkout \u65F6\u6539\u7528 --resume\u3002", [{ command: `itpay services next ${serviceExecutionID} --json`, reason: "\u8BFB\u53D6\u5F53\u524D\u5141\u8BB8\u7684\u4ED8\u8D39 capability" }]);
  }
  if (!options.resume) {
    const readModel = await backend.getServiceExecution(serviceExecutionID);
    const capability = readModel.capabilities.find((item) => item.capability_id === capabilityID);
    if (!capability || !capability.requires_payment) {
      throw new CommandContractError("capability_not_checkoutable", `capability ${capabilityID} is not available for checkout on service execution ${serviceExecutionID}`, "\u53EA\u4E3A\u5F53\u524D Service Execution \u8FD4\u56DE\u7684 requires_payment capability \u521B\u5EFA Checkout\u3002", [{ command: `itpay services next ${serviceExecutionID} --json`, reason: "\u8BFB\u53D6\u5F53\u524D\u5141\u8BB8\u7684\u4E0B\u4E00\u6B65" }]);
    }
    const lockedInput = options.lockedInput ?? {};
    const missingInput = missingRequiredInput(capability.input_schema, lockedInput);
    if (missingInput.length > 0 && readModel.execution.next_action !== "create_checkout") {
      throw new CommandContractError("capability_input_invalid", `missing required capability input: ${missingInput.join(", ")}`, "\u8865\u9F50\u4ED8\u8D39 capability \u7684 required_input\uFF1B\u672C\u6B21\u6CA1\u6709\u521B\u5EFA quote\u3001Checkout \u6216\u8BA2\u5355\u3002", [{ command: checkoutCommand(serviceExecutionID, capability, lockedInput), reason: "\u63D0\u4EA4\u5B8C\u6574\u4E14\u4F1A\u88AB\u9501\u5B9A\u7684\u670D\u52A1\u8F93\u5165" }]);
    }
    if (capability.delivery_email_required && String(deliveryContact.email ?? "").trim() === "") {
      throw new CommandContractError("delivery_email_required", "delivery email is required before creating this service checkout", "\u8BE5 capability \u7684\u4EA4\u4ED8\u94FE\u63A5\u4F1A\u53D1\u9001\u5230\u7528\u6237\u90AE\u7BB1\uFF1B\u5148\u5411\u7528\u6237\u8BF4\u660E\u7528\u9014\u5E76\u8BE2\u95EE\u90AE\u7BB1\uFF0C\u4E0D\u8981\u4EE3\u586B\u3002", [{
        command: `itpay services checkout ${serviceExecutionID} --capability ${capability.capability_id}${formatInputOptions(lockedInput)} --email <email> --json`,
        reason: "\u4F7F\u7528\u7528\u6237\u63D0\u4F9B\u7684\u90AE\u7BB1\u521B\u5EFA Checkout"
      }]);
    }
  }
  const response = await backend.createServiceExecutionCheckout(serviceExecutionID, {
    ...capabilityID ? { capability_id: capabilityID } : {},
    ...Object.keys(deliveryContact).length > 0 ? { delivery_contact: deliveryContact } : {},
    ...options.lockedInput && Object.keys(options.lockedInput).length > 0 ? { locked_input: options.lockedInput } : {},
    ...options.resume ? { resume: true } : {}
  });
  const checkout = response.checkout;
  const checkoutID = checkout.checkout.checkout_id;
  const displayToken = checkout.display_token;
  const locale = normalizeCardLocale(options.locale);
  const checkoutURL = tokenizedCheckoutURL2(checkout.checkout_url, displayToken, checkout.qr_payload);
  const cardURL = localizeCardURL(absolutePublicURL3(config.baseURL, checkout.card_url ?? fallbackCardURL2(config.baseURL, checkoutID, displayToken)), locale);
  const cardPNGURL = localizeCardURL(absolutePublicURL3(config.baseURL, checkout.card_png_url ?? checkout.qr_png_url ?? fallbackCardPNGURL2(config.baseURL, checkoutID, displayToken)), locale);
  const plan = buildCheckoutQRPlan({
    host,
    checkoutID,
    checkoutURL,
    cardURL,
    displayToken,
    qrPayload: checkout.qr_payload,
    qrPNGURL: cardPNGURL,
    nextAction: checkout.checkout.next_action,
    orderItems: response.cart.items.map((item) => ({
      title: item.title,
      quantity: item.quantity,
      amountMinor: item.amount_minor,
      currency: item.currency
    })),
    orderCurrency: checkout.checkout.currency,
    ...options.agentType ? { agentType: options.agentType } : {},
    locale
  });
  options.persistHandoff?.({
    serviceExecutionID,
    cartID: response.cart.cart_id,
    checkoutID,
    displayToken,
    checkoutURL
  });
  const platform = platformKeyForHost(plan.host);
  if (!options.jsonOutput && (platform === "telegram" || platform === "feishu" || platform === "lark")) {
    await dispatchRender(plan, {
      host,
      ...options.target ? { target: options.target } : {},
      ...options.qrFormat ? { qrFormat: options.qrFormat } : {},
      ...options.qrFilePath ? { qrFilePath: options.qrFilePath } : {},
      ...options.output ? { output: options.output } : {},
      ...options.fetchImpl ? { fetchImpl: options.fetchImpl } : {},
      baseURL: config.baseURL
    });
    return;
  }
  if (shouldPrepareLocalCheckoutImage(platform)) {
    await ensureIdeImageAttach(plan, {
      enabled: config.ideImageAttach,
      ...config.baseURL ? { baseURL: config.baseURL } : {},
      ...options.fetchImpl ? { fetchImpl: options.fetchImpl } : {}
    });
  }
  const envelope = buildServicesCheckoutEnvelope(response, checkoutURL, plan, options.agentType, options.target);
  const plainResult = [
    `service_execution_id: ${response.binding.service_execution_id}`,
    `checkout_id: ${checkoutID}`,
    `capability_id: ${checkoutCapabilityID(response, capabilityID)}`,
    `locked_input: ${JSON.stringify(response.locked_input)}`,
    `amount: ${formatMoney3(checkout.checkout.amount_minor, checkout.checkout.currency)}`
  ];
  if (!options.jsonOutput && platform === "terminal") {
    plainResult.push("qr:", await renderTerminalQR(checkoutURL, options.qrFormat ?? "terminal"));
  }
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {},
    plainResult
  });
}
async function runServicesQuote(backend, serviceExecutionID, capabilityID, input, options = {}) {
  const model = await backend.getServiceExecution(serviceExecutionID);
  const capability = model.capabilities.find((item) => item.capability_id === capabilityID);
  if (!capability || !capability.requires_payment) {
    throw new CommandContractError("capability_not_quoteable", `capability ${capabilityID} is not available for quote on service execution ${serviceExecutionID}`, "\u53EA\u4E3A\u5F53\u524D Service Execution \u8FD4\u56DE\u7684\u4ED8\u8D39 capability \u521B\u5EFA\u62A5\u4EF7\u3002", [{ command: `itpay services next ${serviceExecutionID} --json`, reason: "\u8BFB\u53D6\u5F53\u524D\u5408\u6CD5\u52A8\u4F5C" }]);
  }
  const selectionBacked = model.execution.status === "human_action_approved" && model.allowed_actions?.some((action) => action.type === "prepare_quote" && action.capability_id === capabilityID);
  const missingInput = missingRequiredInput(capability.input_schema, input);
  if (missingInput.length > 0 && !selectionBacked) {
    throw new CommandContractError("capability_input_invalid", `missing required capability input: ${missingInput.join(", ")}`, "\u8865\u9F50\u4ED8\u8D39 capability \u8F93\u5165\uFF1B\u672C\u6B21\u6CA1\u6709\u521B\u5EFA Quote\u3001Cart \u6216 Checkout\u3002", [{ command: quoteCommand(serviceExecutionID, capability, input), reason: "\u63D0\u4EA4\u5B8C\u6574\u4E14\u4F1A\u88AB\u9501\u5B9A\u7684\u8F93\u5165" }]);
  }
  const deliveryContact = {
    ...options.deliveryContact ?? {},
    ...options.email ? { email: options.email } : {}
  };
  if (capability.delivery_email_required && String(deliveryContact.email ?? "").trim() === "") {
    throw new CommandContractError("delivery_email_required", "delivery email is required before preparing this service quote", "\u4EA4\u4ED8\u94FE\u63A5\u4F1A\u53D1\u9001\u5230\u7528\u6237\u90AE\u7BB1\uFF1B\u8BF4\u660E\u7528\u9014\u5E76\u8BE2\u95EE\u90AE\u7BB1\uFF0C\u4E0D\u8981\u4EE3\u586B\u3002", [{ command: quoteCommand(serviceExecutionID, capability, input), reason: "\u4F7F\u7528\u7528\u6237\u63D0\u4F9B\u7684\u90AE\u7BB1\u521B\u5EFA\u62A5\u4EF7" }]);
  }
  const quote = await backend.prepareServiceQuote(serviceExecutionID, {
    capability_id: capabilityID,
    ...Object.keys(deliveryContact).length > 0 ? { delivery_contact: deliveryContact } : {},
    ...Object.keys(input).length > 0 ? { locked_input: input } : {}
  });
  const result = {
    service_quote_lock_id: quote.service_quote_lock_id,
    service_execution_id: quote.service_execution_id,
    capability_id: quote.capability_id,
    price: formatMoney3(quote.amount_minor, quote.currency),
    expires_at: quote.expires_at
  };
  writeCommandEnvelope({
    status: "quote_ready",
    result,
    instruction: "\u62A5\u4EF7\u5DF2\u9501\u5B9A\u5F53\u524D Execution \u7684\u53EF\u4FE1\u8F93\u5165\u548C\u4EF7\u683C\uFF1B\u53EF\u5355\u72EC\u4ED8\u6B3E\uFF0C\u4E5F\u53EF\u4E0E\u5176\u4ED6\u72EC\u7ACB Execution \u7684\u62A5\u4EF7\u5408\u5E76\u3002",
    next: {
      command: `itpay cart add --quote ${quote.service_quote_lock_id} --json`,
      reason: "\u52A0\u5165 canonical Cart"
    },
    recovery: [{ command: `itpay services next ${serviceExecutionID} --json`, reason: "\u91CD\u65B0\u8BFB\u53D6\u5F53\u524D Execution \u72B6\u6001" }]
  }, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {},
    plainResult: Object.entries(result).map(([key, value]) => `${key}: ${String(value)}`)
  });
}
async function runServicesGet(backend, serviceExecutionID, options = {}) {
  const response = await backend.getServiceExecution(serviceExecutionID);
  const execution = response.execution;
  const timeline = response.events.slice(-20).map((event) => ({
    sequence: event.sequence,
    step: event.type,
    status: event.status,
    phase: event.phase,
    ...event.capability_id ? { capability_id: event.capability_id } : {},
    occurred_at: event.occurred_at
  }));
  const deliveryMode = serviceDeliveryMode(response);
  const lockedRefund = response.refunds.find((refund2) => refund2.access_locked);
  const nextState = servicesNextEnvelope(response);
  const result = {
    service_execution_id: execution.service_execution_id,
    service_id: execution.service_id,
    status: execution.status,
    phase: execution.phase,
    ...execution.current_capability_id ? { current_capability_id: execution.current_capability_id } : {},
    updated_at: execution.updated_at,
    timeline,
    ...response.events.length > timeline.length ? { timeline_truncated: true } : {},
    ...deliveryMode ? { delivery_mode: deliveryMode } : {},
    ...lockedRefund ? {
      access_locked: true,
      refund: { refund_request_id: lockedRefund.refund_request_id, status: lockedRefund.status }
    } : {}
  };
  const envelope = {
    status: "shown",
    result,
    instruction: lockedRefund || isTerminalServiceExecutionStatus(execution.status) ? nextState.instruction : "\u65F6\u95F4\u7EBF\u4EC5\u7528\u4E8E\u89E3\u91CA\u548C\u6062\u590D\uFF1B\u6309\u5F53\u524D\u9996\u9009\u52A8\u4F5C\u7EE7\u7EED\uFF0C\u4E0D\u8981\u91CD\u653E\u5DF2\u5B8C\u6210\u6B65\u9AA4\u3002",
    next: nextState.next ? { command: nextState.next.command, reason: "\u7EE7\u7EED\u5F53\u524D\u9996\u9009\u52A8\u4F5C" } : null,
    recovery: [{ command: `itpay services events ${serviceExecutionID} --json`, reason: "\u4EC5\u5728\u9700\u8981\u5B8C\u6574\u8BCA\u65AD\u4E8B\u4EF6\u65F6\u4F7F\u7528" }]
  };
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {},
    plainResult: [
      `service_execution_id: ${execution.service_execution_id}`,
      `service_id: ${execution.service_id}`,
      `state: ${execution.status}/${execution.phase}`,
      ...execution.current_capability_id ? [`current_capability_id: ${execution.current_capability_id}`] : [],
      ...timeline.map((event) => `${event.sequence}. ${event.step} ${event.status}/${event.phase} ${event.occurred_at}`)
    ]
  });
}
async function runServicesNext(backend, serviceExecutionID, options = {}) {
  const response = await backend.getServiceExecution(serviceExecutionID);
  const envelope = servicesNextEnvelope(response);
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {},
    plainResult: servicesNextPlainResult(envelope.result)
  });
}
async function runServicesList(backend, options = {}) {
  const limit = options.limit ?? 10;
  if (!Number.isInteger(limit) || limit < 1 || limit > 100) {
    throw new CommandContractError("limit_invalid", "--limit must be an integer from 1 to 100", "\u4F7F\u7528 1 \u5230 100 \u7684\u6574\u6570 limit\uFF1B\u672C\u6B21\u672A\u8BFB\u53D6\u670D\u52A1\u7AEF\u5217\u8868\u3002", [{ command: "itpay services list --limit 10 --json", reason: "\u4F7F\u7528\u9ED8\u8BA4\u4E0A\u9650\u91CD\u8BD5" }]);
  }
  const response = await backend.listServiceExecutions(limit);
  const executions = response.executions.map(({ execution }) => ({
    service_execution_id: execution.service_execution_id,
    service_id: execution.service_id,
    status: execution.status,
    phase: execution.phase,
    updated_at: execution.updated_at
  }));
  const latest = executions[0];
  const envelope = {
    status: latest ? "listed" : "no_executions",
    result: { executions },
    instruction: latest ? "\u7ED3\u679C\u6309\u6700\u65B0\u5230\u6700\u65E7\u6392\u5217\uFF0C\u9ED8\u8BA4\u53EA\u5217\u6700\u8FD1 10 \u6761\uFF1B\u627E\u4E0D\u5230\u76EE\u6807\u65F6\u518D\u6269\u5927 limit\u3002" : "\u5F53\u524D\u8BBE\u5907\u6CA1\u6709\u53EF\u6062\u590D\u7684 Service Execution\uFF1B\u5148\u8BFB\u53D6\u5DF2\u53D1\u5E03\u76EE\u5F55\uFF0C\u4E0D\u8981\u731C\u6D4B ID\u3002",
    next: latest ? { command: `itpay services next ${latest.service_execution_id} --json`, reason: "\u9ED8\u8BA4\u6062\u590D\u6700\u65B0\u6267\u884C" } : { command: "itpay catalog list --json", reason: "\u9009\u62E9\u5DF2\u53D1\u5E03\u670D\u52A1" },
    recovery: []
  };
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {},
    plainResult: executions.map((execution) => `${execution.service_execution_id}: ${execution.service_id} ${execution.status}/${execution.phase} updated=${execution.updated_at}`)
  });
}
async function runServicesReadResult(backend, serviceExecutionID, options = {}) {
  const envelope = grantedResultEnvelope(await backend.getGrantedServiceResult(serviceExecutionID));
  writeCommandEnvelope(envelope, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {},
    plainResult: servicesNextPlainResult(envelope.result)
  });
}
function servicesNextEnvelope(model) {
  const execution = model.execution;
  const lockedRefund = model.refunds.find((refund2) => refund2.access_locked);
  if (lockedRefund) {
    const terminal = lockedRefund.status === "succeeded";
    return {
      status: "delivery_locked",
      result: {
        service_execution_id: execution.service_execution_id,
        access_locked: true,
        refund: {
          refund_request_id: lockedRefund.refund_request_id,
          status: lockedRefund.status
        }
      },
      instruction: terminal ? "\u9000\u6B3E\u5DF2\u6210\u529F\uFF0C\u4EA4\u4ED8\u6C38\u4E45\u5173\u95ED\uFF1B\u4E0D\u8981 reveal\u3001\u521B\u5EFA grant \u6216\u8BFB\u53D6\u7ED3\u679C\u3002" : "\u9000\u6B3E\u5904\u7406\u4E2D\uFF0C\u4EA4\u4ED8\u5DF2\u51BB\u7ED3\uFF1B\u4E0D\u8981 reveal\u3001\u521B\u5EFA grant \u6216\u8BFB\u53D6\u7ED3\u679C\u3002",
      next: terminal ? null : {
        command: `itpay refund get ${lockedRefund.refund_request_id} --json`,
        reason: "\u8BFB\u53D6\u9000\u6B3E\u6743\u5A01\u72B6\u6001"
      },
      recovery: []
    };
  }
  if (isTerminalServiceExecutionStatus(execution.status)) {
    return {
      status: execution.status,
      result: {
        service_execution_id: execution.service_execution_id,
        service_id: execution.service_id,
        phase: execution.phase
      },
      instruction: execution.status === "refunded" ? "\u8BE5\u670D\u52A1\u6267\u884C\u5DF2\u9000\u6B3E\u5E76\u6C38\u4E45\u7ED3\u675F\uFF1B\u4E0D\u8981\u91CD\u653E capability \u6216\u521B\u5EFA Checkout\u3002" : "\u8BE5\u670D\u52A1\u6267\u884C\u5DF2\u7ED3\u675F\uFF1B\u4E0D\u8981\u91CD\u653E capability \u6216\u521B\u5EFA Checkout\u3002",
      next: null,
      recovery: [{
        command: `itpay services events ${execution.service_execution_id} --json`,
        reason: "\u4EC5\u5728\u9700\u8981\u8BCA\u65AD\u7EC8\u6B62\u539F\u56E0\u65F6\u8BFB\u53D6\u4E8B\u4EF6"
      }]
    };
  }
  const currentItems = model.current_result_items ?? [];
  const delivery = model.current_delivery ?? model.delivery_bindings.at(-1);
  const deliveryMode = serviceDeliveryMode(model);
  const candidateSelection = model.allowed_actions?.find((action) => action.type === "select_candidate");
  if (candidateSelection && currentItems.length > 0) {
    const paidCapability = delivery?.capability_id ? model.capabilities.find((capability) => capability.capability_id === delivery.capability_id && capability.requires_payment) : void 0;
    return {
      status: "candidate_selection_available",
      result: {
        service_execution_id: execution.service_execution_id,
        ...delivery?.capability_id ? { capability_id: delivery.capability_id } : {},
        ...deliveryMode ? { delivery_mode: deliveryMode } : {},
        items: currentItems.map((item) => ({
          rank: item.rank,
          title: item.display_title,
          safe_payload: item.safe_payload
        }))
      },
      instruction: paidCapability ? "\u4ED8\u8D39 Agent-visible \u641C\u7D22\u5DF2\u5B8C\u6210\u3002\u73B0\u5728\u628A items \u4E2D\u7684\u7F16\u53F7\u3001title \u548C safe_payload \u5C55\u793A\u7ED9\u7528\u6237\uFF0C\u7136\u540E\u505C\u6B62\uFF1B\u4E0D\u8981\u8C03\u7528 read-result\u3002\u82E5\u7528\u6237\u76EE\u6807\u53EA\u662F\u5019\u9009\u641C\u7D22\uFF0C\u4EFB\u52A1\u5DF2\u7ECF\u5B8C\u6210\u3002\u53EA\u6709\u7528\u6237\u4E4B\u540E\u660E\u786E\u9009\u62E9\u67D0\u4E2A\u5019\u9009\u5E76\u8981\u6C42\u7EE7\u7EED\u65F6\uFF0C\u624D\u6267\u884C next.command\uFF1B\u4E0D\u8981\u81EA\u52A8\u8D2D\u4E70\u540E\u7EED\u62A5\u544A\u3002" : "\u5411\u7528\u6237\u5C55\u793A\u7F16\u53F7\u548C safe_payload\uFF1B\u82E5\u5019\u9009\u5217\u8868\u5DF2\u6EE1\u8DB3\u7528\u6237\u76EE\u6807\uFF0C\u5728\u6B64\u505C\u6B62\u3002\u4EC5\u5728\u7528\u6237\u660E\u786E\u9009\u62E9\u5E76\u5E0C\u671B\u7EE7\u7EED\u65F6\uFF0C\u624D\u5728\u5F53\u524D Execution \u63D0\u4EA4\u5BF9\u5E94 rank\u3002",
      next: {
        command: `itpay services action ${execution.service_execution_id} --action select_candidate --actor-type human --status approved --candidate <rank> --json`,
        reason: paidCapability ? "\u4EC5\u5728\u7528\u6237\u660E\u786E\u9009\u62E9\u5019\u9009\u5E76\u8981\u6C42\u7EE7\u7EED\u65F6\u6267\u884C" : "\u4EC5\u5728\u7528\u6237\u660E\u786E\u9009\u62E9\u540E\u9501\u5B9A\u6765\u6E90\u5019\u9009"
      },
      recovery: []
    };
  }
  if (deliveryMode === "agent_visible_result") {
    const items = currentItems.map((item) => ({
      rank: item.rank,
      title: item.display_title,
      safe_payload: item.safe_payload
    }));
    const selection = model.allowed_actions?.find((action) => action.type === "select_candidate");
    return {
      status: items.length > 0 ? "result_ready" : "no_result",
      result: {
        service_execution_id: execution.service_execution_id,
        ...delivery?.capability_id ? { capability_id: delivery.capability_id } : {},
        delivery_mode: deliveryMode,
        items
      },
      instruction: items.length > 0 ? selection ? "Agent-visible \u641C\u7D22\u5DF2\u5B8C\u6210\u3002\u5411\u7528\u6237\u5C55\u793A items \u4E2D\u7684\u7F16\u53F7\u3001title \u548C safe_payload\uFF0C\u7136\u540E\u505C\u6B62\uFF1B\u4E0D\u8981\u8C03\u7528 read-result\u3002\u53EA\u6709\u7528\u6237\u660E\u786E\u9009\u62E9\u5019\u9009\u5E76\u8981\u6C42\u7EE7\u7EED\u65F6\uFF0C\u624D\u6267\u884C next.command\u3002" : "\u8FD9\u662F\u5F53\u524D Graph \u6B65\u9AA4\u5BF9\u5E94\u7684\u4EA4\u4ED8\uFF1B\u7ED3\u679C\u5DF2\u53EF\u4F9B Agent \u4F7F\u7528\uFF0C\u53EA\u4F7F\u7528 safe_payload\u3002" : "Agent-visible \u4EA4\u4ED8\u5DF2\u5B8C\u6210\u4F46\u6709 0 \u4E2A\u7ED3\u679C\u3002\u5411\u7528\u6237\u5C55\u793A\u7A7A\u7ED3\u679C\u5E76\u505C\u6B62\uFF1B\u4E0D\u8981\u8C03\u7528 read-result\u3001\u91CD\u653E\u5F53\u524D Execution\u3001\u4FEE\u6539\u8F93\u5165\u6216\u521B\u5EFA\u65B0 Execution\u3002",
      next: selection ? {
        command: `itpay services action ${execution.service_execution_id} --action select_candidate --actor-type human --status approved --candidate <rank> --json`,
        reason: "\u4EC5\u5728\u7528\u6237\u660E\u786E\u9009\u62E9\u540E\u9501\u5B9A\u6765\u6E90\u5019\u9009"
      } : null,
      recovery: []
    };
  }
  if (deliveryMode === "vault_artifact") {
    const grantStatus = normalizeGrantStatus(delivery?.grant_status);
    const grantActive = grantStatus === "active";
    const grantPending = grantStatus === "pending";
    return {
      status: grantActive ? "grant_active" : grantPending ? "result_preparing" : "human_authorization_required",
      result: {
        service_execution_id: execution.service_execution_id,
        ...delivery?.capability_id ? { capability_id: delivery.capability_id } : {},
        delivery_mode: deliveryMode,
        grant_status: grantStatus,
        ...delivery?.preparation ? { preparation: delivery.preparation } : {},
        ...grantActive && delivery?.grant_expires_at ? { grant_expires_at: delivery.grant_expires_at } : {}
      },
      instruction: grantActive ? "\u8FD9\u662F\u5F53\u524D Graph \u6B65\u9AA4\u5BF9\u5E94\u7684\u4EA4\u4ED8\uFF1B\u7528\u6237\u6388\u6743\u6709\u6548\uFF0C\u7ACB\u5373\u8BFB\u53D6\u5E76\u9075\u5B88\u5B57\u6BB5\u8303\u56F4\u4E0E\u5230\u671F\u65F6\u95F4\u3002" : grantPending ? "\u7528\u6237\u5DF2\u7ECF\u5B8C\u6210\u6388\u6743\uFF0C\u670D\u52A1\u7AEF\u6B63\u5728\u6309\u5DF2\u53D1\u5E03\u6267\u884C\u56FE\u51C6\u5907\u4EA4\u4ED8\u5185\u5BB9\u3002\u4E0D\u8981\u518D\u6B21\u4ED8\u6B3E\u3001\u518D\u6B21\u6388\u6743\u3001\u65B0\u5EFA Execution \u6216\u8C03\u7528 read-result\uFF1B\u53EA\u6267\u884C next.command \u67E5\u8BE2\u540C\u4E00 Execution\u3002" : "\u8FD9\u662F\u5F53\u524D Graph \u6B65\u9AA4\u5BF9\u5E94\u7684\u4EA4\u4ED8\uFF1B\u8BF7\u7528\u6237\u5728\u8BA2\u5355\u9875\u9762\u6388\u6743\uFF0C\u672A\u6388\u6743\u524D\u4E0D\u8981\u8BFB\u53D6\u6216\u731C\u6D4B\u5185\u5BB9\u3002",
      next: grantPending ? {
        command: `itpay services next ${execution.service_execution_id} --json`,
        reason: "\u7B49\u5F85\u540C\u4E00 Execution \u7684\u4EA4\u4ED8\u51C6\u5907\u5B8C\u6210"
      } : {
        command: `itpay services read-result ${execution.service_execution_id} --json`,
        reason: grantActive ? "\u8BFB\u53D6\u5F53\u524D\u6709\u6548 grant \u7684\u7ED3\u679C" : "\u4EC5\u5728\u7528\u6237\u786E\u8BA4\u6388\u6743\u540E\u6267\u884C"
      },
      recovery: []
    };
  }
  const allowedActions = model.allowed_actions ?? [];
  const preferred = allowedActions[0];
  if (preferred?.type === "prepare_quote") {
    const continuation = paidContinuation(model, preferred, {});
    if (continuation) {
      return {
        status: execution.status,
        result: {
          service_execution_id: execution.service_execution_id,
          service_id: execution.service_id,
          phase: execution.phase,
          checkout: continuation.checkout
        },
        instruction: purchaseConfirmationInstruction(execution.status === "quota_exhausted" ? "quota_exhausted" : "candidate_selected", continuation.price, continuation.capability.delivery_email_required, continuation.capability.delivery_email_purpose),
        next: continuation.next,
        recovery: []
      };
    }
  }
  const next = preferred ? serviceAllowedActionCommand(model, preferred) : null;
  return {
    status: execution.status,
    result: {
      service_execution_id: execution.service_execution_id,
      service_id: execution.service_id,
      phase: execution.phase,
      allowed_actions: allowedActions.map((action) => ({
        type: action.type,
        ...action.capability_id ? { capability_id: action.capability_id } : {},
        requires_human: action.requires_human
      }))
    },
    instruction: preferred?.type === "resume_checkout" ? "\u5F53\u524D Execution \u5DF2\u7ECF\u6709\u4E00\u7B14 Checkout\u3002\u4E0D\u8981\u521B\u5EFA\u65B0\u7684 Quote\u3001Cart\u3001Checkout \u6216 Execution\u3002\u73B0\u5728\u53EA\u6267\u884C next.command\uFF0C\u6062\u590D\u5E76\u5C55\u793A\u540C\u4E00 Checkout \u7684\u4ED8\u6B3E\u5165\u53E3\u3002" : preferred?.type === "wait" ? "\u4ED8\u6B3E\u5DF2\u786E\u8BA4\uFF0CProvider \u6B63\u5728\u5904\u7406\u5F53\u524D Execution\u3002\u4E0D\u8981\u65B0\u5EFA Execution\u3001Checkout \u6216\u518D\u6B21\u4ED8\u6B3E\uFF1B\u7A0D\u540E\u53EA\u6267\u884C next.command \u67E5\u8BE2\u540C\u4E00 Execution\u3002" : preferred?.requires_human ? "\u5F53\u524D\u4E0B\u4E00\u6B65\u9700\u8981\u7528\u6237\u660E\u786E\u9009\u62E9\uFF1B\u5148\u5C55\u793A\u5FC5\u8981\u4FE1\u606F\u5E76\u7B49\u5F85\u786E\u8BA4\u3002" : preferred ? "\u6267\u884C\u670D\u52A1\u7AEF\u8FD4\u56DE\u7684\u552F\u4E00\u9996\u9009\u52A8\u4F5C\uFF1B\u4E0D\u8981\u731C\u6D4B\u5176\u4ED6 capability\u3002" : "\u5F53\u524D\u6CA1\u6709\u540E\u7EED\u52A8\u4F5C\u3002",
    next,
    recovery: [{ command: `itpay services get ${execution.service_execution_id} --json`, reason: "\u4EC5\u5728\u5F53\u524D\u52A8\u4F5C\u5F02\u5E38\u65F6\u68C0\u67E5\u65F6\u95F4\u7EBF" }]
  };
}
function serviceAllowedActionCommand(model, action) {
  const executionID = model.execution.service_execution_id;
  const capability = action.capability_id ? model.capabilities.find((item) => item.capability_id === action.capability_id) : void 0;
  switch (action.type) {
    case "invoke_capability": {
      if (!capability)
        return null;
      const input = Object.fromEntries(requiredInputFields(capability.input_schema).map((field) => [field, "<value>"]));
      return {
        command: `itpay services invoke ${executionID} --capability ${capability.capability_id}${formatInputOptions(input)} --json`,
        reason: "\u6267\u884C\u5F53\u524D\u5141\u8BB8\u7684 Agent-visible capability"
      };
    }
    case "select_candidate":
      return {
        command: `itpay services action ${executionID} --action select_candidate --actor-type human --status approved --candidate <rank> --json`,
        reason: "\u4EC5\u5728\u7528\u6237\u660E\u786E\u9009\u62E9\u540E\u63D0\u4EA4\u5F53\u524D\u5019\u9009 rank"
      };
    case "prepare_quote": {
      return paidContinuation(model, action, {})?.next ?? null;
    }
    case "resume_checkout":
      return { command: `itpay services checkout ${executionID} --resume --json`, reason: "\u6062\u590D\u540C\u4E00 Checkout\uFF0C\u4E0D\u521B\u5EFA\u7B2C\u4E8C\u7B14" };
    case "wait":
      return { command: `itpay services next ${executionID} --json`, reason: "\u7B49\u5F85 durable execution \u63A8\u8FDB" };
    case "view_delivery":
      return { command: `itpay services next ${executionID} --json`, reason: "\u8BFB\u53D6\u5F53\u524D\u4EA4\u4ED8\u6A21\u5F0F" };
    default:
      return null;
  }
}
function serviceDeliveryMode(model) {
  const delivery = model.current_delivery ?? model.delivery_bindings.at(-1);
  const explicit = String(delivery?.redacted_summary?.delivery_mode ?? "");
  if (explicit)
    return explicit;
  return delivery?.vault_artifact_id ? "vault_artifact" : "";
}
function normalizeGrantStatus(status) {
  return !status || status === "missing" ? "none" : status;
}
function grantedResultEnvelope(response) {
  return {
    status: "granted_result_ready",
    result: {
      service_execution_id: response.service_execution_id,
      ...response.expires_at ? { grant_expires_at: response.expires_at } : {},
      granted_fields: Object.keys(response.result),
      payload: response.result
    },
    instruction: "\u7ED3\u679C\u6765\u81EA\u5F53\u524D\u6709\u6548 Vault Grant\uFF1B\u53EA\u4F7F\u7528\u672C\u6B21\u6388\u6743\u5B57\u6BB5\uFF0C\u8FC7\u671F\u540E\u505C\u6B62\u8BFB\u53D6\u5E76\u91CD\u65B0\u8BF7\u6C42\u7528\u6237\u540C\u610F\u3002",
    next: null,
    recovery: []
  };
}
function servicesNextPlainResult(result) {
  const lines = [];
  for (const [key, value] of Object.entries(result)) {
    if (key === "items" && Array.isArray(value)) {
      lines.push("items:");
      for (const item of value) {
        lines.push(`  ${item.rank}. ${item.title}`);
        for (const [field, fieldValue] of Object.entries(item.safe_payload)) {
          lines.push(`     ${field}: ${typeof fieldValue === "string" ? fieldValue : JSON.stringify(fieldValue)}`);
        }
      }
      continue;
    }
    lines.push(`${key}: ${typeof value === "string" ? value : JSON.stringify(value)}`);
  }
  return lines;
}
async function runServicesEvents(backend, serviceExecutionID, options = {}) {
  const afterSequence = options.afterSequence ?? 0;
  const limit = options.limit ?? 50;
  if (!serviceExecutionID.trim()) {
    throw new CommandContractError("service_execution_id_required", "service execution id is required", "\u4F7F\u7528 services list \u8FD4\u56DE\u7684 execution ID\uFF1B\u4E0D\u8981\u731C\u6D4B\u3002", [{ command: "itpay services list --json", reason: "\u5217\u51FA\u5F53\u524D\u8EAB\u4EFD\u53EF\u89C1\u6267\u884C" }]);
  }
  if (!Number.isSafeInteger(afterSequence) || afterSequence < 0) {
    throw new CommandContractError("events_parameter_invalid", "after_sequence must be a non-negative integer", "--after-sequence \u5FC5\u987B\u662F\u975E\u8D1F\u6574\u6570\uFF1B\u672C\u6B21\u672A\u8BFB\u53D6\u4E8B\u4EF6\u3002", [{ command: `itpay services events ${serviceExecutionID} --help`, reason: "\u67E5\u770B\u8BCA\u65AD\u53C2\u6570" }]);
  }
  if (!Number.isSafeInteger(limit) || limit < 1 || limit > 100) {
    throw new CommandContractError("events_parameter_invalid", "limit must be an integer between 1 and 100", "--limit \u5FC5\u987B\u662F 1 \u5230 100 \u7684\u6574\u6570\uFF1B\u672C\u6B21\u672A\u8BFB\u53D6\u4E8B\u4EF6\u3002", [{ command: `itpay services events ${serviceExecutionID} --help`, reason: "\u67E5\u770B\u8BCA\u65AD\u53C2\u6570" }]);
  }
  const response = await backend.listServiceExecutionEvents(serviceExecutionID, afterSequence, limit);
  const events = response.events.map((event) => ({
    sequence: event.sequence,
    type: event.type,
    status: event.status,
    phase: event.phase,
    ...event.capability_id ? { capability_id: event.capability_id } : {},
    occurred_at: event.occurred_at
  }));
  writeCommandEnvelope({
    status: "listed",
    result: {
      service_execution_id: serviceExecutionID,
      after_sequence: afterSequence,
      returned_count: events.length,
      events
    },
    instruction: "\u4E8B\u4EF6\u4EC5\u7528\u4E8E\u8BCA\u65AD\uFF1B\u4E0D\u8981\u4ECE\u4E8B\u4EF6\u91CD\u653E\u4E1A\u52A1\u6B65\u9AA4\uFF0C\u56DE\u5230 services next \u83B7\u53D6\u5F53\u524D\u52A8\u4F5C\u3002",
    next: {
      command: `itpay services next ${serviceExecutionID} --json`,
      reason: "\u6062\u590D\u6B63\u5E38\u670D\u52A1\u6D41\u7A0B"
    },
    recovery: events.length === limit && events.length > 0 ? [{
      command: `itpay services events ${serviceExecutionID} --after-sequence ${events.at(-1).sequence} --limit ${limit} --json`,
      reason: "\u7EE7\u7EED\u8BFB\u53D6\u4E0B\u4E00\u9875\u8BCA\u65AD\u4E8B\u4EF6"
    }] : []
  }, {
    ...options.jsonOutput !== void 0 ? { jsonOutput: options.jsonOutput } : {},
    ...options.output ? { output: options.output } : {},
    plainResult: [
      `service_execution_id: ${serviceExecutionID}`,
      `returned_count: ${events.length}`,
      ...events.map((event) => `${event.sequence} ${event.occurred_at} ${event.type} ${event.status}/${event.phase}`)
    ]
  });
}
function parseKeyValueList(values) {
  const result = {};
  for (const value of values ?? []) {
    const index = value.indexOf("=");
    if (index <= 0) {
      throw new Error(`invalid --input "${value}", expected key=value`);
    }
    result[value.slice(0, index)] = parseValue(value.slice(index + 1));
  }
  return result;
}
function collectOption(value, previous = []) {
  previous.push(value);
  return previous;
}
function parseValue(value) {
  if (value === "true")
    return true;
  if (value === "false")
    return false;
  if (/^-?\d+(\.\d+)?$/.test(value))
    return Number(value);
  return value;
}
function buildServicesCheckoutEnvelope(response, checkoutURL, plan, agentType, target) {
  const checkout = response.checkout;
  const platform = platformKeyForHost(plan.host);
  const amount = formatMoney3(checkout.checkout.amount_minor, checkout.checkout.currency);
  const presentationHandoff = buildCheckoutHandoff({
    platform,
    url: plan.linkOnlyURL ?? checkoutURL,
    amount,
    plan,
    ...agentType ? { agentType } : {},
    ...target ? { target } : {},
    ...plan.preferredQRSources[0] ? { qrImageURL: plan.preferredQRSources[0] } : {},
    ...plan.ideImageAttach?.status === "downloaded" && plan.ideImageAttach.localPath ? { localPath: plan.ideImageAttach.localPath } : {},
    ...platform === "markdown" ? { markdown: buildAgentChatHandoff(plan).markdown } : {}
  });
  return {
    status: "human_checkout_required",
    result: {
      service_execution_id: response.binding.service_execution_id,
      checkout_id: checkout.checkout.checkout_id,
      capability_id: checkoutCapabilityID(response),
      locked_input: response.locked_input,
      amount
    },
    handoff: presentationHandoff.handoff,
    instruction: presentationHandoff.instruction,
    next: {
      command: plan.afterActionCommand ?? `itpay checkout --id ${checkout.checkout.checkout_id} --token ${checkout.display_token} --json`,
      reason: "\u4EC5\u5728\u7528\u6237\u5B8C\u6210\u4ED8\u6B3E\u64CD\u4F5C\u6216\u8981\u6C42\u67E5\u8BE2\u540E\uFF0C\u8BFB\u53D6\u540C\u4E00 Checkout \u7684\u6743\u5A01\u72B6\u6001"
    },
    recovery: []
  };
}
function fallbackCardURL2(baseURL, checkoutID, displayToken) {
  const root = baseURL.replace(/\/$/, "");
  return `${root}/v1/checkouts/${encodeURIComponent(checkoutID)}/card?display_token=${encodeURIComponent(displayToken)}`;
}
function fallbackCardPNGURL2(baseURL, checkoutID, displayToken) {
  return `${fallbackCardURL2(baseURL, checkoutID, displayToken)}.png`.replace("/card?", "/card.png?");
}
function checkoutCapabilityID(response, fallback = "") {
  return response.capability_id || fallback;
}
function absolutePublicURL3(baseURL, value) {
  try {
    return new URL(value, baseURL.endsWith("/") ? baseURL : `${baseURL}/`).toString();
  } catch {
    return value;
  }
}
function formatMoney3(amountMinor, currency) {
  return `${(amountMinor / 100).toFixed(2)} ${currency}`;
}
function normalizeServiceActionStatus(status, serviceExecutionID) {
  const normalized = status.trim().toLowerCase();
  if (!serviceActionStatuses.has(normalized)) {
    throw actionInputError(serviceExecutionID, `invalid --status "${status}". Supported: pending, approved, rejected, expired, cancelled`);
  }
  return normalized;
}
function tokenizedCheckoutURL2(checkoutURL, displayToken, qrPayload) {
  if (qrPayload.trim().length > 0) {
    return qrPayload;
  }
  if (checkoutURL.trim().length === 0 || displayToken.trim().length === 0) {
    return checkoutURL;
  }
  try {
    const parsed = new URL(checkoutURL);
    if (!parsed.searchParams.has("display_token")) {
      parsed.searchParams.set("display_token", displayToken);
    }
    return parsed.toString();
  } catch {
    const separator = checkoutURL.includes("?") ? "&" : "?";
    return `${checkoutURL}${separator}display_token=${encodeURIComponent(displayToken)}`;
  }
}

// ../../../../../../tmp/itpay-platform-bundle-7Irajt/node_modules/@itpay/cli/dist/src/main.js
var program2 = new Command();
program2.name("itpay").description("V3 ItPay CLI \u2014 one entry point for buy workflows and future sell workflows").option("--agent-type <type>", "agent runtime type used for device enrollment and client-specific guidance").version(CLI_VERSION);
function withHost(value, agentType, target) {
  if (!value && agentType?.trim().toLowerCase() === "openclaw") {
    throw new CommandContractError("host_required", "OpenClaw requires an explicit --host entry", "\u4ECE\u5F53\u524D\u53EF\u4FE1 OpenClaw \u4F1A\u8BDD\u4E0A\u4E0B\u6587\u4F20\u5165 --host\uFF1BIM \u5165\u53E3\u540C\u65F6\u4F20 --target\u3002\u672C\u6B21\u672A\u521B\u5EFA\u6216\u4FEE\u6539\u8D44\u6E90\u3002", []);
  }
  const host = normalizeHost(value ?? defaultHostForAgentType(agentType));
  if (!host) {
    throw new CommandContractError("invalid_host", `invalid --host "${value ?? ""}". Supported: terminal, codex, claude-code, telegram, discord, whatsapp, feishu, lark, plain-chat`, "\u4F20\u5165\u53D7\u652F\u6301\u7684\u5C55\u793A Host\uFF1B\u672C\u6B21\u672A\u521B\u5EFA\u6216\u4FEE\u6539\u8D44\u6E90\u3002", []);
  }
  const contextError = agentType?.trim().toLowerCase() === "openclaw" ? validateContext(host, target) : void 0;
  if (contextError) {
    throw new CommandContractError(contextError.code, contextError.message, "\u4ECE\u5F53\u524D\u53EF\u4FE1\u4F1A\u8BDD\u4E0A\u4E0B\u6587\u8865\u9F50 --target\uFF1B\u672C\u6B21\u672A\u521B\u5EFA\u6216\u4FEE\u6539\u8D44\u6E90\u3002", []);
  }
  return host;
}
function parseRequiredContactFields(value) {
  if (!value) {
    return void 0;
  }
  const values = value.split(",").map((item) => item.trim().toLowerCase()).filter(Boolean);
  const invalid = values.filter((item) => item !== "email" && item !== "phone");
  if (invalid.length > 0) {
    throw new CommandContractError("contact_field_invalid", `unsupported required contact fields: ${invalid.join(", ")}`, "--require-contact \u53EA\u63A5\u53D7 email\u3001phone \u6216\u4E8C\u8005\u7EC4\u5408\u3002", [{ command: "itpay buy --help", reason: "\u67E5\u770B contact \u53C2\u6570" }]);
  }
  const parsed = values.filter((item) => item === "email" || item === "phone");
  return parsed.length > 0 ? parsed : void 0;
}
function positiveInteger(value, name) {
  const text = String(value ?? "");
  if (!/^[1-9]\d*$/.test(text)) {
    throw new CommandContractError("buy_parameter_invalid", `${name} must be a positive integer`, `${name} \u5FC5\u987B\u662F\u6B63\u6574\u6570\uFF1B\u672C\u6B21\u672A\u521B\u5EFA\u6216\u4FEE\u6539 Cart/Checkout\u3002`, [{ command: "itpay buy --help", reason: "\u67E5\u770B\u53C2\u6570\u683C\u5F0F" }]);
  }
  return Number(text);
}
function resolveCheckoutPresentationArgs(input) {
  if (input.requestedCheckoutID && input.requestedDisplayToken) {
    return { checkoutID: input.requestedCheckoutID, displayToken: input.requestedDisplayToken };
  }
  if (input.requestedCheckoutID && !input.requestedDisplayToken) {
    if (input.savedCheckoutID === input.requestedCheckoutID && input.savedDisplayToken) {
      return { checkoutID: input.requestedCheckoutID, displayToken: input.savedDisplayToken };
    }
    const savedHint = input.savedCheckoutID ? ` Saved checkout is ${input.savedCheckoutID}.` : "";
    throw new Error(`display token is required for checkout ${input.requestedCheckoutID}.${savedHint} Pass --token for that checkout or run \`itpay checkout\` without --id to use the saved checkout.`);
  }
  if (input.requestedDisplayToken) {
    if (input.savedCheckoutID) {
      return { checkoutID: input.savedCheckoutID, displayToken: input.requestedDisplayToken };
    }
    throw new Error("checkout id is required when --token is provided and no saved checkout exists");
  }
  if (input.savedCheckoutID && input.savedDisplayToken) {
    return { checkoutID: input.savedCheckoutID, displayToken: input.savedDisplayToken };
  }
  throw new Error("checkout id and display token are required; pass --id/--token or create a checkout first");
}
function reportCLIError(error, contract) {
  const commandError = error instanceof CommandContractError ? error : void 0;
  const backendOverrideError = error instanceof BackendOverrideError ? error : void 0;
  const deviceError = error instanceof DeviceAuthorizationError ? error : void 0;
  const stateError = error instanceof DeviceStateError ? error : void 0;
  const transportError = error instanceof HttpTransportError ? error : void 0;
  const httpRecovery = errorRecoveryActions(error).map((action) => ({
    command: action.command,
    reason: action.reason ?? action.label
  }));
  const identityRecovery = error instanceof HttpError && (error.code === "agent_identity_required" || error.code === "agent_device_session_required");
  const incompatible = error instanceof HttpError && (error.code === "client_upgrade_required" || error.code === "client_compatibility_headers_required" || error.code === "platform_release_unavailable" || error.status === 404 && error.code === "unknown_error");
  const requiredCLIVersion = incompatible && error instanceof HttpError && /^\d+\.\d+\.\d+$/.test(error.payload?.minimum_cli_version ?? "") ? error.payload.minimum_cli_version : void 0;
  const backendInternal = error instanceof HttpError && error.status === 500 && error.code === "internal_error";
  const providerConnectionUnavailable = error instanceof HttpError && error.code === "provider_connection_unavailable";
  const providerTemporary = error instanceof HttpError && error.code === "provider_temporarily_unavailable";
  const providerRejected = error instanceof HttpError && error.code === "provider_rejected";
  const providerInputRejected = error instanceof HttpError && error.code === "provider_input_rejected";
  const providerContractMismatch = error instanceof HttpError && error.code === "provider_contract_mismatch";
  const capabilityInputInvalid = error instanceof HttpError && error.code === "capability_input_invalid";
  const deviceRecovery = deviceError ? [{
    command: "itpay skill show itpay --json",
    reason: "\u8BFB\u53D6 ItPay \u8EAB\u4EFD\u8FB9\u754C\uFF1B\u8BE5\u9519\u8BEF\u9700\u8981\u7528\u6237\u6216\u8FD0\u8425\u6062\u590D Backend \u767B\u8BB0\uFF0C\u4E0D\u80FD\u901A\u8FC7\u6362\u7C7B\u578B\u6216\u5220\u9664\u672C\u5730\u8EAB\u4EFD\u7ED5\u8FC7"
  }] : [];
  const stateRecovery = stateError ? [{
    command: "itpay skill show itpay --json",
    reason: "\u8BFB\u53D6 Device \u72B6\u6001\u8FB9\u754C\uFF1B\u4FEE\u590D\u5F53\u524D Host \u7684\u6301\u4E45\u5199\u6743\u9650\u540E\u91CD\u8BD5\u539F\u547D\u4EE4"
  }] : [];
  const authorizationInstruction = stateError ? "\u5F53\u524D\u8FD0\u884C\u73AF\u5883\u65E0\u6CD5\u5199\u5165 owner-only Device \u72B6\u6001\uFF1B\u8BF7\u4FDD\u6301\u540C\u4E00 Node\u3001CLI \u548C Agent Type\uFF0C\u5728\u5141\u8BB8\u6301\u4E45\u5199\u5165 ~/.itpay-v3 \u7684\u6267\u884C\u73AF\u5883\u4E2D\u91CD\u8BD5\u3002\u4E0D\u8981\u624B\u5DE5\u521B\u5EFA lock\u3001\u5220\u9664 identity \u6216\u6362\u8FD0\u884C\u65F6\u78B0\u8FD0\u6C14\u3002" : error instanceof HttpError && error.code === "agent_device_session_required" ? "CLI \u5DF2\u81EA\u52A8\u7EED\u671F\u5E76\u91CD\u8BD5\u540C\u4E00\u8BF7\u6C42\u4E00\u6B21\uFF0C\u4ECD\u88AB\u62D2\u7EDD\uFF1B\u505C\u6B62\u91CD\u8BD5\uFF0C\u4E0D\u8981\u5207\u6362 Agent Type \u6216\u65CB\u8F6C\u8EAB\u4EFD\u3002" : deviceError?.code === "agent_device_revoked" ? "Backend \u5DF2\u64A4\u9500\u5F53\u524D Device \u767B\u8BB0\uFF1BCLI \u6CA1\u6709\u81EA\u52A8\u521B\u5EFA\u66FF\u4EE3\u8EAB\u4EFD\u3002\u505C\u6B62\u91CD\u8BD5\u5E76\u8BF7\u7528\u6237\u6216\u8FD0\u8425\u6062\u590D\u767B\u8BB0\u3002" : deviceError ? "Device \u8EAB\u4EFD\u9A8C\u8BC1\u5931\u8D25\uFF1B\u505C\u6B62\u91CD\u8BD5\uFF0C\u4E0D\u8981\u5207\u6362 Agent Type\u3001\u5220\u9664\u72B6\u6001\u6216\u65CB\u8F6C\u79C1\u94A5\u3002" : void 0;
  if (contract || commandError || backendOverrideError) {
    writeCommandEnvelope({
      status: "error",
      error: {
        code: incompatible ? "backend_contract_incompatible" : backendOverrideError?.code ?? commandError?.code ?? (error instanceof HttpError ? error.code : transportError?.code ?? stateError?.code ?? deviceError?.code ?? contract?.code ?? "command_failed"),
        message: error instanceof Error ? error.message : String(error)
      },
      ...requiredCLIVersion ? {
        result: {
          current_cli_version: CLI_VERSION,
          required_cli_version: requiredCLIVersion
        }
      } : transportError ? {
        result: {
          attempts: transportError.attempts,
          automatic_retry_performed: transportError.attempts > 1
        }
      } : error instanceof HttpError && error.payload?.service_execution_id ? {
        result: {
          service_execution_id: error.payload.service_execution_id,
          provider_called: error.payload.provider_called === true,
          ...error.payload.effective_quota ? {
            quota: {
              remaining: error.payload.effective_quota.remaining,
              limit: error.payload.effective_quota.limit
            }
          } : {}
        }
      } : {},
      instruction: incompatible ? requiredCLIVersion ? distributionUpgradeInstruction() : "\u7ACB\u5373\u5411\u7528\u6237\u62A5\u544A error.message \u5E76\u7ED3\u675F\u672C\u6B21\u4EFB\u52A1\u3002Backend \u672A\u63D0\u4F9B\u53EF\u9A8C\u8BC1\u7684\u517C\u5BB9 CLI \u7248\u672C\uFF1B\u4E0D\u8981\u8FD0\u884C\u5176\u4ED6 ItPay \u6216 npm \u547D\u4EE4\uFF0C\u4E0D\u8981\u731C\u6D4B\u7248\u672C\u3001\u5207\u6362 Agent Type \u6216\u5220\u9664 Device \u8EAB\u4EFD\u3002" : backendInternal ? "Backend \u5185\u90E8\u6545\u969C\uFF1B\u7ACB\u5373\u505C\u6B62\u5E76\u5411\u7528\u6237\u62A5\u544A\u3002\u4E0D\u8981\u91CD\u8BD5\u3001\u68C0\u67E5\u6216\u5220\u9664 Device \u8EAB\u4EFD\u3001\u521B\u5EFA\u66FF\u4EE3 Execution\u3001\u5207\u6362 Backend\uFF0C\u6216\u5C1D\u8BD5 quote\u3001checkout\u3001cart\u3001buy\u3001pay \u7B49\u4ED8\u8D39\u8DEF\u5F84\u3002" : providerConnectionUnavailable ? "Provider \u8BF7\u6C42\u672A\u53D1\u51FA\uFF0C\u9884\u7559\u514D\u8D39\u989D\u5EA6\u5DF2\u91CA\u653E\uFF1B\u5F53\u524D Execution \u5DF2\u5931\u8D25\u3002\u7ACB\u5373\u5411\u7528\u6237\u62A5\u544A error.message \u5E76\u505C\u6B62\uFF0C\u4E0D\u8981\u81EA\u52A8\u91CD\u8BD5\u3001\u4E0D\u8981\u7EE7\u7EED\u540C\u4E00 Execution\uFF0C\u4E5F\u4E0D\u8981\u8FDB\u5165\u4EFB\u4F55\u4ED8\u8D39\u8DEF\u5F84\u3002\u53EA\u6709\u8FD0\u8425\u786E\u8BA4\u8FDE\u63A5\u6062\u590D\u4E14\u7528\u6237\u660E\u786E\u8981\u6C42\u91CD\u65B0\u67E5\u8BE2\u540E\uFF0C\u624D\u542F\u52A8\u65B0\u7684 Service Execution\u3002" : providerTemporary ? "\u4E0A\u6E38\u670D\u52A1\u6682\u65F6\u4E0D\u53EF\u7528\uFF1B\u5411\u7528\u6237\u9010\u5B57\u62A5\u544A error.message \u548C result.quota \u5E76\u505C\u6B62\uFF0C\u4E0D\u8981\u81EA\u52A8\u91CD\u8BD5\u3001\u4E0D\u8981\u521B\u5EFA\u65B0 Execution\u3002\u53EA\u6709\u7528\u6237\u4E4B\u540E\u660E\u786E\u63D0\u51FA\u65B0\u8BF7\u6C42\uFF0C\u624D\u53EF\u91CD\u65B0\u5F00\u59CB\u3002" : providerInputRejected ? `Provider \u660E\u786E\u62D2\u7EDD\u4E86\u8BE5\u8F93\u5165\uFF1A${error instanceof Error ? error.message : String(error)}\u3002\u8BF7\u5411\u7528\u6237\u62A5\u544A error.message \u548C result.quota \u5E76\u505C\u6B62\u3002\u4E0D\u8981\u81EA\u884C\u4FEE\u6539\u8F93\u5165\u3001\u4E0D\u8981\u91CD\u8BD5\u3001\u4E0D\u8981\u521B\u5EFA\u65B0 Execution\uFF1B\u53EA\u6709\u7528\u6237\u660E\u786E\u63D0\u4F9B\u65B0\u8F93\u5165\u540E\u624D\u80FD\u91CD\u65B0\u67E5\u8BE2\u3002` : providerContractMismatch ? "Provider \u54CD\u5E94\u4E0E\u5DF2\u53D1\u5E03\u5951\u7EA6\u4E0D\u4E00\u81F4\u3002\u8FD9\u4E0D\u662F\u7528\u6237\u8F93\u5165\u95EE\u9898\u3002\u7ACB\u5373\u505C\u6B62\uFF0C\u4E0D\u8981\u4FEE\u6539\u8F93\u5165\u3001\u4E0D\u8981\u91CD\u8BD5\u3001\u4E0D\u8981\u521B\u5EFA\u65B0 Execution\uFF0C\u4E5F\u4E0D\u8981\u8FDB\u5165\u4ED8\u8D39\u8DEF\u5F84\uFF1B\u5411\u7528\u6237\u62A5\u544A\u5E73\u53F0\u6545\u969C\u548C result.quota\u3002" : providerRejected ? "Provider \u62D2\u7EDD\u4E86\u672C\u6B21\u8BF7\u6C42\uFF0C\u4F46\u672A\u58F0\u660E\u8FD9\u662F\u8F93\u5165\u9519\u8BEF\uFF1B\u5411\u7528\u6237\u9010\u5B57\u62A5\u544A error.message \u548C result.quota \u5E76\u505C\u6B62\u3002\u4E0D\u8981\u4FEE\u6539\u8F93\u5165\u3001\u4E0D\u8981\u91CD\u8BD5\u3001\u4E0D\u8981\u521B\u5EFA\u65B0 Execution\u3002" : capabilityInputInvalid ? "\u8F93\u5165\u672A\u901A\u8FC7\u672C\u5730\u6821\u9A8C\uFF0C\u4E0A\u6E38\u5C1A\u672A\u88AB\u8C03\u7528\u4E14\u7528\u6237\u989D\u5EA6\u672A\u53D8\u5316\u3002\u5411\u7528\u6237\u9010\u5B57\u62A5\u544A error.message \u5E76\u505C\u6B62\uFF0C\u4E0D\u8981\u539F\u6837\u91CD\u8BD5\u6216\u8FD0\u884C\u5176\u4ED6\u6062\u590D\u547D\u4EE4\u3002\u7528\u6237\u63D0\u4F9B\u4FEE\u6B63\u540E\u7684\u8F93\u5165\u540E\uFF0C\u7EE7\u7EED\u4F7F\u7528\u5F53\u524D\u672A\u7ED3\u675F\u7684 Execution\u3002" : transportError ? transportError.attempts > 1 ? "\u4E34\u65F6\u7F51\u7EDC\u6545\u969C\uFF1BCLI \u5DF2\u4EC5\u5BF9\u53EF\u5B89\u5168\u91CD\u653E\u7684\u64CD\u4F5C\u5B8C\u6210\u6709\u9650\u81EA\u52A8\u91CD\u8BD5\uFF0C\u4F46\u4ECD\u672A\u83B7\u5F97\u5B8C\u6574\u54CD\u5E94\u3002\u6309 recovery \u67E5\u8BE2\u540C\u4E00\u8D44\u6E90\u7684\u6743\u5A01\u72B6\u6001\uFF1B\u4E0D\u8981\u521B\u5EFA\u66FF\u4EE3 Checkout\u3001Execution\u3001Payment \u6216 Refund\u3002" : "\u7F51\u7EDC\u5728\u5B8C\u6574\u54CD\u5E94\u524D\u4E2D\u65AD\uFF1B\u5F53\u524D\u5199\u64CD\u4F5C\u6CA1\u6709\u5B89\u5168\u91CD\u653E\u5408\u540C\uFF0C\u56E0\u6B64 CLI \u672A\u81EA\u52A8\u91CD\u8BD5\u3002\u6309 recovery \u67E5\u8BE2\u6743\u5A01\u72B6\u6001\uFF1B\u4E0D\u8981\u539F\u6837\u91CD\u653E\u6216\u521B\u5EFA\u66FF\u4EE3 Checkout\u3001Execution\u3001Payment \u6216 Refund\u3002" : backendOverrideError ? "\u79FB\u9664 ITPAY_BACKEND_URL \u4F7F\u7528\u6B63\u5F0F\u73AF\u5883\uFF0C\u6216\u51C6\u786E\u8BBE\u7F6E\u4E3A https://dev.itpay.ai\u3002" : commandError?.instruction ?? authorizationInstruction ?? contract?.instruction ?? "\u68C0\u67E5\u547D\u4EE4\u53C2\u6570\u540E\u91CD\u8BD5\u3002",
      next: null,
      recovery: incompatible ? requiredCLIVersion ? [distributionUpgradeAction(requiredCLIVersion)] : [] : backendInternal || providerConnectionUnavailable || providerTemporary || providerInputRejected || providerContractMismatch || providerRejected || capabilityInputInvalid ? [] : backendOverrideError ? [] : commandError?.recovery ?? (stateError ? stateRecovery : deviceError ? deviceRecovery : identityRecovery ? httpRecovery : contract?.recovery ?? [])
    }, {
      ...contract?.jsonOutput !== void 0 ? { jsonOutput: contract.jsonOutput } : backendOverrideError ? { jsonOutput: process.argv.includes("--json") } : {},
      output: (text) => {
        process.stderr.write(text);
      }
    });
    process.exitCode = 1;
    return;
  }
  if (error instanceof HttpError) {
    process.stderr.write(`[${error.status}] ${error.code}: ${error.message}
`);
    printErrorRecovery(error, (text) => process.stderr.write(text));
    process.exitCode = 1;
    return;
  }
  if (error instanceof HttpTransportError) {
    process.stderr.write(`[${error.code}] ${error.message}
`);
    process.exitCode = 1;
    return;
  }
  if (error instanceof Error) {
    process.stderr.write(`${error.message}
`);
    process.exitCode = 1;
    return;
  }
  throw error;
}
function docsErrorFallback(jsonOutput) {
  return {
    jsonOutput,
    code: "docs_unavailable",
    instruction: "\u5185\u7F6E\u6587\u6863\u7F3A\u5931\u6216\u635F\u574F\uFF1B\u901A\u8FC7\u5F53\u524D\u5206\u53D1\u65B9\u5F0F\u6062\u590D\u540C\u7248\u672C CLI \u540E\u91CD\u8BD5\u3002",
    recovery: [distributionUpgradeAction(CLI_VERSION)]
  };
}
function distributionUpgradeAction(version) {
  switch (cliDistribution()) {
    case "openclaw-skill-bundle":
      return { command: "openclaw skills update itpay", reason: `\u66F4\u65B0\u5305\u542B ItPay CLI ${version} \u7684 Skill bundle` };
    case "kimi-plugin-bundle":
      return {
        command: "/plugins install https://github.com/itpay-ai/itpay-plugin-kimi-work",
        reason: `\u66F4\u65B0\u5305\u542B ItPay CLI ${version} \u7684 Kimi plugin`
      };
    default:
      return { command: `npm install -g @itpay/cli@${version}`, reason: "\u5B89\u88C5 Backend \u6307\u5B9A\u7684\u517C\u5BB9 CLI \u7248\u672C" };
  }
}
function distributionUpgradeInstruction() {
  if (cliDistribution() === "npm") {
    return "\u5F53\u524D CLI \u4E0E Backend \u5408\u7EA6\u4E0D\u517C\u5BB9\u3002\u505C\u6B62\u6240\u6709 ItPay \u4E1A\u52A1\u547D\u4EE4\uFF1B\u53EA\u6267\u884C recovery.command\uFF0C\u5C06 @itpay/cli \u66F4\u65B0\u5230 Backend \u6307\u5B9A\u7684\u7CBE\u786E\u7248\u672C\u3002\u5B89\u88C5\u5B8C\u6210\u540E\u786E\u8BA4 itpay --version \u4E0E result.required_cli_version \u5B8C\u5168\u4E00\u81F4\uFF0C\u518D\u91CD\u65B0\u8FD0\u884C readyz\u3002\u4E0D\u8981\u5B89\u88C5 latest\u3001\u731C\u6D4B\u7248\u672C\u3001\u5207\u6362 Agent Type \u6216\u5220\u9664 Device \u8EAB\u4EFD\u3002";
  }
  return "\u5F53\u524D\u5E73\u53F0 bundle \u4E0E Backend \u5408\u7EA6\u4E0D\u517C\u5BB9\u3002\u505C\u6B62\u6240\u6709 ItPay \u4E1A\u52A1\u547D\u4EE4\uFF1B\u53EA\u6267\u884C recovery.command\uFF0C\u66F4\u65B0\u5E73\u53F0 Skill/plugin \u540E\u542F\u52A8\u65B0\u4F1A\u8BDD\uFF0C\u786E\u8BA4 itpay --version \u4E0E result.required_cli_version \u5B8C\u5168\u4E00\u81F4\uFF0C\u518D\u91CD\u65B0\u8FD0\u884C readyz\u3002\u4E0D\u8981\u8FD0\u884C npm\u3001\u731C\u6D4B\u7248\u672C\u3001\u5207\u6362 Agent Type \u6216\u5220\u9664 Device \u8EAB\u4EFD\u3002";
}
program2.command("readyz").description("Probe the V3 backend readiness endpoint").option("--json", "output JSON instead of terminal text").action(async (options) => {
  const config = loadConfig();
  const backend = newBackendClient(config);
  try {
    await runReadyz(backend, {
      jsonOutput: Boolean(options.json),
      backendURL: config.baseURL,
      environment: config.environment,
      ...config.agentType ? { agentType: config.agentType } : {}
    });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "backend_unavailable",
      instruction: `\u5F53\u524D\u5B98\u65B9 Backend ${config.baseURL} \u4E0D\u53EF\u7528\uFF1B\u6062\u590D\u524D\u4E0D\u8981\u7EE7\u7EED\u4E0B\u5355\uFF0C\u4E5F\u4E0D\u8981\u5207\u6362\u73AF\u5883\u3002`,
      recovery: [
        { command: "itpay readyz", reason: "\u91CD\u8BD5\u5F53\u524D\u5B98\u65B9 Backend \u7684\u53EF\u7528\u6027\u68C0\u67E5" }
      ]
    });
  }
});
var deviceCmd = program2.command("device").description("Recover the current official Backend registration after an operator-confirmed reset");
deviceCmd.command("recover").description("Forget only the current official Backend registration while preserving the local private key").option("--confirm-backend-reset", "confirm that an operator reset the selected Backend registration database").option("--json", "output JSON instead of terminal text").action(async (options) => {
  const config = loadConfig();
  try {
    if (!config.agentType) {
      throw new CommandContractError("agent_type_required", `agent type is required for ${config.baseURL} Device recovery`, "\u5982\u5B9E\u58F0\u660E\u5F53\u524D Agent Type\uFF1B\u6062\u590D\u540E\u5FC5\u987B\u7528\u540C\u4E00\u7C7B\u578B\u91CD\u65B0\u767B\u8BB0\u3002", [{ command: "itpay install --json", reason: "\u9009\u62E9\u5F53\u524D\u771F\u5B9E Agent Type" }]);
    }
    if (!options.confirmBackendReset) {
      throw new CommandContractError("backend_reset_confirmation_required", "--confirm-backend-reset is required", "\u4EC5\u5728\u8FD0\u8425\u5DF2\u786E\u8BA4\u5F53\u524D Backend \u7684 Device \u767B\u8BB0\u6570\u636E\u5E93\u88AB\u91CD\u5EFA\u6216\u6E05\u7A7A\u540E\u6267\u884C\uFF1B\u666E\u901A session \u5931\u6548\u6216 revoked \u4E0D\u5F97\u4F7F\u7528\u3002", [{ command: "itpay docs show identity-and-sessions --json", reason: "\u68C0\u67E5\u9002\u7528\u8FB9\u754C" }]);
    }
    const recovered = await new DeviceAuthority({
      baseURL: config.baseURL,
      requestedAgentType: config.agentType,
      compatibilityHeaders: {}
    }).recoverBackendReset();
    writeCommandEnvelope({
      status: recovered.removed ? "backend_registration_removed" : "backend_registration_absent",
      result: {
        backend: config.baseURL,
        removed_agent_types: recovered.agentTypes,
        private_key_preserved: true,
        other_backend_registrations_preserved: true
      },
      instruction: "\u53EA\u8BFB\u5217\u51FA Service Executions\uFF0C\u4EE5\u540C\u4E00\u79C1\u94A5\u548C Agent Type \u91CD\u65B0\u767B\u8BB0\u5F53\u524D Backend\uFF1B\u4E0D\u8981\u5220\u9664 ~/.itpay-v3 \u6216\u5207\u6362\u8FD0\u884C\u65F6\u3002",
      next: {
        command: `itpay --agent-type ${config.agentType} services list --limit 1 --json`,
        reason: "\u7528\u65E0\u4E1A\u52A1\u5199\u5165\u7684\u7B7E\u540D\u8BF7\u6C42\u91CD\u65B0\u767B\u8BB0\u5F53\u524D Backend"
      },
      recovery: []
    }, {
      jsonOutput: Boolean(options.json),
      plainResult: [
        `backend: ${config.baseURL}`,
        `registration: ${recovered.removed ? "removed" : "already absent"}`,
        "private_key: preserved",
        "other_backends: preserved"
      ]
    });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "device_recovery_failed",
      instruction: "\u4EC5\u6062\u590D\u8FD0\u8425\u5DF2\u786E\u8BA4\u91CD\u5EFA\u7684\u5F53\u524D Backend\uFF1B\u4E0D\u8981\u5220\u9664\u6574\u4E2A Device identity\u3002",
      recovery: [{ command: "itpay docs show identity-and-sessions --json", reason: "\u68C0\u67E5 Device \u6062\u590D\u8FB9\u754C" }]
    });
  }
});
var skillCmd = program2.command("skill").description("Read complete packaged Agent skills");
skillCmd.command("show").description("Show one complete packaged skill").argument("<name>", "skill name").option("--json", "output JSON instead of terminal text").action((name, options) => {
  const config = loadConfig();
  try {
    runSkillShow(name, { jsonOutput: Boolean(options.json), ...config.agentType ? { agentType: config.agentType } : {} });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "skill_unavailable",
      instruction: "\u5185\u7F6E Skill \u7F3A\u5931\u6216\u635F\u574F\uFF1B\u901A\u8FC7\u5F53\u524D\u5206\u53D1\u65B9\u5F0F\u6062\u590D\u540C\u7248\u672C CLI \u540E\u91CD\u8BD5\u3002",
      recovery: [distributionUpgradeAction(CLI_VERSION)]
    });
  }
});
program2.command("next").description("Show the next recommended agent action from remembered server handles").option("--json", "output JSON instead of terminal text").action(async (options) => {
  const config = loadConfig();
  try {
    await requirePlatformCompatibility(newBackendClient(config));
    const session = CartSession.loadFromFile(cartSessionPath(), config.checkoutCurrency);
    runNext(session, { jsonOutput: Boolean(options.json) });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "next_unavailable",
      instruction: "Backend \u5408\u540C\u53EF\u7528\u540E\u518D\u8BFB\u53D6\u672C\u5730\u6062\u590D\u53E5\u67C4\uFF1B\u4E0D\u8981\u6839\u636E\u65E7\u53E5\u67C4\u7EE7\u7EED\u4EA4\u6613\u3002",
      recovery: []
    });
  }
});
var catalogCmd = program2.command("catalog").description("Browse V3 service catalog");
catalogCmd.command("list").description("List all available services from the published catalog manifest").option("--json", "output JSON instead of terminal text").action(async (options) => {
  const backend = newBackendClient(loadConfig());
  try {
    await requirePlatformCompatibility(backend);
    await runCatalogList(backend, { jsonOutput: Boolean(options.json) });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "catalog_unavailable",
      instruction: "\u786E\u8BA4 ItPay \u53EF\u7528\u540E\u91CD\u8BD5\u76EE\u5F55\u8BFB\u53D6\uFF1B\u4E0D\u8981\u731C\u6D4B service_id\u3002",
      recovery: [
        { command: "itpay readyz", reason: "\u786E\u8BA4 Backend \u53EF\u7528" },
        { command: "itpay catalog list", reason: "\u91CD\u65B0\u8BFB\u53D6\u5DF2\u53D1\u5E03\u76EE\u5F55" }
      ]
    });
  }
});
var installCmd = program2.command("install").description("Show setup instructions for each agent host");
installCmd.argument("[target]", "Agent Type, or list").option("--json", "output JSON instead of terminal text").description("Show agent-specific installation and configuration instructions").action((target, options) => {
  try {
    runInstall(target, { jsonOutput: Boolean(options.json) });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "install_failed",
      instruction: "\u9009\u62E9\u53D7\u652F\u6301\u7684\u771F\u5B9E Agent Type\uFF1B\u672C\u547D\u4EE4\u4E0D\u4F1A\u4FEE\u6539\u5BBF\u4E3B\u914D\u7F6E\u3002",
      recovery: [{ command: "itpay install --json", reason: "\u5217\u51FA\u652F\u6301\u7C7B\u578B" }]
    });
  }
});
var docsCmd = program2.command("docs").description("Browse agent documentation");
docsCmd.command("list").description("List all available agent doc topics").option("--json", "output JSON instead of terminal text").action((options) => {
  try {
    runDocsList({ jsonOutput: Boolean(options.json) });
  } catch (error) {
    reportCLIError(error, docsErrorFallback(Boolean(options.json)));
  }
});
docsCmd.command("show").description("Show a specific doc topic").argument("<topic>", "doc topic name").option("--json", "output JSON instead of terminal text").action((topic, options) => {
  try {
    runDocsShow(topic, { jsonOutput: Boolean(options.json) });
  } catch (error) {
    reportCLIError(error, docsErrorFallback(Boolean(options.json)));
  }
});
docsCmd.command("search").description("Search doc topics by keyword").argument("<query>", "search query").option("--json", "output JSON instead of terminal text").action((query, options) => {
  try {
    runDocsSearch(query, { jsonOutput: Boolean(options.json) });
  } catch (error) {
    reportCLIError(error, docsErrorFallback(Boolean(options.json)));
  }
});
var cart = program2.command("cart").description("V3 canonical server cart");
cart.command("add").description("Add a variant/offer/quantity to the canonical server cart").option("--item <catalog_item_id>").option("--variant <catalog_variant_id>").option("--offer <offer_id>").option("--quote <service_quote_lock_id>", "add a prepared service quote").option("--quantity <n>", "quantity", Number, 1).option("--input <json>").option("--host <host>", "client host (terminal, codex, telegram, feishu, lark, ...)").option("--target <target>", "chat id / channel id / open id for IM hosts").option("--json", "output JSON instead of terminal text").option("--local", "only add to the local draft cache; not valid for service-backed flows").action(async (options) => {
  const config = loadConfig();
  const sessionPath = cartSessionPath();
  const session = CartSession.loadFromFile(sessionPath, config.checkoutCurrency);
  const jsonOutput = Boolean(options.json);
  try {
    const quoteMode = Boolean(options.quote);
    if (quoteMode && (options.item || options.variant || options.offer || options.input || options.local)) {
      throw new CommandContractError("cart_item_scope_invalid", "--quote cannot be combined with catalog fields, input, or --local", "\u670D\u52A1\u62A5\u4EF7\u53EA\u4F7F\u7528 services quote \u8FD4\u56DE\u7684 quote ID\uFF1B\u4E0D\u8981\u6DF7\u5165 Catalog \u6216 input \u53C2\u6570\u3002", [{ command: "itpay cart add --help", reason: "\u67E5\u770B\u4E24\u79CD\u6DFB\u52A0\u65B9\u5F0F" }]);
    }
    if (!quoteMode && (!options.item || !options.variant || !options.offer)) {
      throw new CommandContractError("cart_item_required", "--item, --variant and --offer are required", "\u4F7F\u7528\u540C\u4E00\u6761 Catalog \u8BB0\u5F55\u8FD4\u56DE\u7684 item\u3001variant \u548C offer ID\uFF1B\u4E0D\u8981\u731C\u6D4B\u6216\u6DF7\u7528\u3002", [{ command: "itpay catalog list --json", reason: "\u8BFB\u53D6\u5DF2\u53D1\u5E03\u76EE\u5F55 ID" }]);
    }
    if (!quoteMode && (!Number.isInteger(options.quantity) || options.quantity < 1)) {
      throw new CommandContractError("quantity_invalid", "--quantity must be a positive integer", "\u4F7F\u7528\u5927\u4E8E 0 \u7684\u6574\u6570 quantity\uFF1B\u672C\u6B21\u672A\u4FEE\u6539 Cart\u3002", [{ command: "itpay cart show", reason: "\u786E\u8BA4\u5F53\u524D Cart \u672A\u53D8\u5316" }]);
    }
    let input;
    if (options.input) {
      const parsed = JSON.parse(options.input);
      if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
        throw new CommandContractError("cart_input_invalid", "--input must be a JSON object", "\u6309\u7167\u670D\u52A1\u5408\u540C\u4F20\u5165 JSON object\uFF1B\u672C\u6B21\u672A\u4FEE\u6539 Cart\u3002", [{ command: "itpay catalog list --json", reason: "\u91CD\u65B0\u786E\u8BA4\u670D\u52A1\u5165\u53E3" }]);
      }
      input = parsed;
    }
    const addOptions = {
      catalogItemID: options.item,
      catalogVariantID: options.variant,
      offerID: options.offer,
      quantity: options.quantity,
      ...input ? { input } : {}
    };
    if (options.local) {
      runCartAdd(session, { ...addOptions, jsonOutput });
    } else {
      const host = withHost(options.host, config.agentType, options.target);
      const contextError = validateContext(host, options.target);
      if (contextError) {
        throw new CommandContractError(contextError.code, contextError.message, "\u8865\u9F50\u5F53\u524D\u5BA2\u6237\u7AEF\u6240\u9700\u7684 Host/target\uFF1B\u672C\u6B21\u672A\u521B\u5EFA\u6216\u4FEE\u6539 Cart\u3002", [{ command: "itpay cart add --help", reason: "\u67E5\u770B\u5BA2\u6237\u7AEF\u53C2\u6570" }]);
      }
      const backend = newBackendClient(config);
      if (quoteMode) {
        await runCartAddQuoteServer({
          serviceQuoteLockID: options.quote,
          backend,
          config,
          session,
          host,
          ...options.target ? { target: options.target } : {},
          jsonOutput
        });
      } else {
        await runCartAddServer({
          ...addOptions,
          backend,
          config,
          session,
          host,
          ...options.target ? { target: options.target } : {},
          jsonOutput
        });
      }
    }
  } catch (error) {
    const quoteMode = Boolean(options.quote);
    reportCLIError(error, {
      jsonOutput,
      code: "cart_add_failed",
      instruction: quoteMode ? "Quote \u662F\u5426\u5DF2\u52A0\u5165 Cart \u5C1A\u672A\u786E\u8BA4\uFF1B\u5148\u6062\u590D\u5F53\u524D Cart \u6216\u6765\u6E90 Execution\uFF0C\u4E0D\u8981\u91CD\u590D\u51C6\u5907\u62A5\u4EF7\u6216\u76F4\u63A5\u521B\u5EFA Checkout\u3002" : "\u6838\u5BF9 Catalog ID\u3001\u8F93\u5165\u548C Cart \u72B6\u6001\uFF1B\u4E0D\u8981\u5728\u5931\u8D25\u540E\u76F4\u63A5\u521B\u5EFA Checkout\u3002",
      recovery: quoteMode ? [
        { command: "itpay cart show --json", reason: "\u68C0\u67E5\u5F53\u524D canonical Cart" },
        { command: "itpay services list --json", reason: "\u6062\u590D Quote \u6240\u5C5E\u7684 Service Execution" }
      ] : [
        { command: "itpay catalog list --json", reason: "\u6838\u5BF9\u5DF2\u53D1\u5E03\u9879\u76EE" },
        { command: "itpay cart show", reason: "\u786E\u8BA4 canonical Cart \u5F53\u524D\u72B6\u6001" }
      ]
    });
  } finally {
    session.saveToFile(sessionPath);
  }
});
cart.command("next").description("Show the next recommended agent action for the remembered server cart").option("--json", "output JSON instead of terminal text").action(async (options) => {
  const config = loadConfig();
  const backend = newBackendClient(config);
  const session = CartSession.loadFromFile(cartSessionPath(), config.checkoutCurrency);
  try {
    await runCartNext(backend, session, { jsonOutput: Boolean(options.json) });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "cart_next_failed",
      instruction: "canonical Cart \u65E0\u6CD5\u8BFB\u53D6\uFF1B\u4E0D\u8981\u731C\u6D4B Cart \u5185\u5BB9\u6216\u521B\u5EFA\u91CD\u590D\u8BA2\u5355\u3002",
      recovery: [
        { command: "itpay services list --json", reason: "\u6062\u590D\u5F53\u524D\u8BBE\u5907\u53EF\u89C1\u7684 Service Execution" },
        { command: "itpay catalog list --json", reason: "\u5728\u6CA1\u6709\u53EF\u6062\u590D\u6267\u884C\u65F6\u91CD\u65B0\u9009\u62E9\u670D\u52A1" }
      ]
    });
  }
});
cart.command("remove").description("Remove a line from the canonical server cart").option("--line <cart_item_id>", "server cart item id; defaults to last remembered cart item").option("--variant <catalog_variant_id>", "local draft variant id, only with --local").option("--offer <offer_id>", "local draft offer id, only with --local").option("--local", "only remove from the explicit local draft cache").option("--json", "output JSON instead of terminal text").action(async (options) => {
  const config = loadConfig();
  const sessionPath = cartSessionPath();
  const session = CartSession.loadFromFile(sessionPath, config.checkoutCurrency);
  const jsonOutput = Boolean(options.json);
  try {
    if (options.local) {
      if (!options.variant || !options.offer) {
        throw new CommandContractError("local_cart_item_required", "--local remove requires --variant and --offer", "\u4ECE `cart show --local --json` \u4F7F\u7528\u540C\u4E00\u6761\u8349\u7A3F line \u7684 variant \u548C offer\uFF1B\u4E0D\u8981\u731C\u6D4B\u3002", [{ command: "itpay cart show --local --json", reason: "\u8BFB\u53D6\u672C\u5730\u8349\u7A3F" }]);
      }
      if (options.line) {
        throw new CommandContractError("cart_remove_scope_invalid", "--line cannot be combined with --local", "canonical line \u4F7F\u7528 --line\uFF1B\u672C\u5730\u8349\u7A3F\u4F7F\u7528 --local --variant --offer\uFF0C\u4E0D\u8981\u6DF7\u7528\u3002", [{ command: "itpay cart remove --help", reason: "\u67E5\u770B\u4E24\u79CD\u5220\u9664\u8303\u56F4" }]);
      }
      runCartRemove(session, {
        catalogVariantID: options.variant,
        offerID: options.offer,
        jsonOutput
      });
    } else {
      if (options.variant || options.offer) {
        throw new CommandContractError("cart_remove_scope_invalid", "--variant and --offer require --local", "canonical Cart \u4F7F\u7528 cart_item_id\uFF1B\u5148\u4ECE `cart show --json` \u8BFB\u53D6 line\u3002", [{ command: "itpay cart show --json", reason: "\u8BFB\u53D6 canonical line \u53E5\u67C4" }]);
      }
      if (!session.lastCartID) {
        throw new CommandContractError("cart_handle_missing", "no canonical server cart is remembered", "\u672C\u5730\u6CA1\u6709 canonical Cart \u53E5\u67C4\uFF1B\u4E0D\u8981\u7528 local draft \u4EE3\u66FF\u670D\u52A1\u7AEF\u5220\u9664\u3002", [{ command: "itpay next --json", reason: "\u68C0\u67E5\u5176\u4ED6\u53EF\u6062\u590D\u53E5\u67C4" }]);
      }
      const lineID = options.line ?? session.lastCartItemID;
      if (!lineID) {
        throw new CommandContractError("cart_item_required", "cart item id is required", "\u4ECE `cart show --json` \u9009\u62E9 cart_item_id\uFF1B\u4E0D\u8981\u4F7F\u7528 variant\u3001offer \u6216 quote lock ID\u3002", [{ command: "itpay cart show --json", reason: "\u8BFB\u53D6 canonical line \u53E5\u67C4" }]);
      }
      const backend = newBackendClient(config);
      await runCartRemoveServer(backend, session, lineID, { jsonOutput });
    }
  } catch (error) {
    const locked = error instanceof HttpError && error.code === "cart_item_locked";
    reportCLIError(error, {
      jsonOutput,
      code: "cart_remove_failed",
      instruction: locked ? "\u8BE5 line \u5DF2\u7ED1\u5B9A quote/Checkout\uFF0C\u4E0D\u80FD\u518D\u5220\u9664\uFF1B\u7EE7\u7EED\u540C\u4E00 Cart \u7684\u73B0\u6709\u6D41\u7A0B\uFF0C\u4E0D\u8981\u6E05\u672C\u5730\u72B6\u6001\u4F2A\u88C5\u6210\u529F\u3002" : "\u5220\u9664\u5931\u8D25\uFF1B\u91CD\u65B0\u8BFB\u53D6\u540C\u4E00 Cart\uFF0C\u4E0D\u8981\u5047\u8BBE line \u6216 Service Execution \u5DF2\u53D6\u6D88\u3002",
      recovery: [{ command: "itpay cart next --json", reason: "\u8BFB\u53D6\u540C\u4E00 Cart \u7684\u670D\u52A1\u7AEF\u9996\u9009\u52A8\u4F5C" }]
    });
  } finally {
    session.saveToFile(sessionPath);
  }
});
cart.command("show").description("Print the canonical server cart or local draft fallback").option("--json", "output JSON instead of terminal text").option("--local", "show only the explicit local compatibility draft").action(async (options) => {
  const config = loadConfig();
  const sessionPath = cartSessionPath();
  const session = CartSession.loadFromFile(sessionPath, config.checkoutCurrency);
  try {
    if (options.local) {
      runCartShow(session, { jsonOutput: Boolean(options.json) });
    } else {
      await runCartShowServer(newBackendClient(config), session, { jsonOutput: Boolean(options.json) });
    }
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "cart_show_failed",
      instruction: "canonical Cart \u65E0\u6CD5\u8BFB\u53D6\uFF1B\u4E0D\u8981\u6839\u636E\u672C\u5730\u65E7\u53E5\u67C4\u731C\u6D4B\u670D\u52A1\u7AEF\u72B6\u6001\u3002",
      recovery: [
        { command: "itpay services list --json", reason: "\u6062\u590D\u5F53\u524D\u8BBE\u5907\u53EF\u89C1\u7684 Service Execution" },
        { command: "itpay catalog list --json", reason: "\u5728\u6CA1\u6709\u53EF\u6062\u590D\u8D44\u6E90\u65F6\u91CD\u65B0\u9009\u62E9" }
      ]
    });
  }
});
cart.command("clear").description("Abandon the canonical server cart or explicitly clear local state").option("--local", "only clear local handles and explicit local draft").option("--json", "output JSON instead of terminal text").action(async (options) => {
  const config = loadConfig();
  const sessionPath = cartSessionPath();
  const session = CartSession.loadFromFile(sessionPath, config.checkoutCurrency);
  try {
    if (options.local) {
      runCartClear(session, { jsonOutput: Boolean(options.json) });
    } else {
      const backend = newBackendClient(config);
      await runCartAbandonServer(backend, session, { jsonOutput: Boolean(options.json) });
    }
  } catch (error) {
    const locked = error instanceof HttpError && (error.code === "cart_item_locked" || error.status === 409);
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "cart_clear_failed",
      instruction: locked ? "\u8BE5 Cart \u5DF2\u7ED1\u5B9A quote/Checkout\uFF0C\u4E0D\u80FD\u653E\u5F03\uFF1B\u4FDD\u7559\u672C\u5730\u53E5\u67C4\u5E76\u7EE7\u7EED\u540C\u4E00\u6D41\u7A0B\u3002" : "\u653E\u5F03\u5931\u8D25\uFF1B\u4E0D\u8981\u6E05\u672C\u5730\u53E5\u67C4\u6216\u5047\u8BBE Backend Cart \u5DF2\u6539\u53D8\u3002",
      recovery: [{ command: "itpay cart next --json", reason: "\u6062\u590D\u540C\u4E00 canonical Cart" }]
    });
  } finally {
    session.saveToFile(sessionPath);
  }
});
program2.command("buy").description("Create a V3 cart and checkout, then render the checkout QR for the host").option("--host <host>", "client host (terminal, telegram, feishu, lark, ...)").option("--target <target>", "chat id / channel id / open id for IM hosts").option("--item <catalog_item_id>").option("--variant <catalog_variant_id>").option("--offer <offer_id>").option("--cart <cart_id>", "existing canonical server cart id").option("--quantity <n>", "quantity", "1").option("--ref <client_reference_id>").option("--contact-email <email>").option("--contact-phone <phone>").option("--require-contact <fields>", "comma-separated required contact fields: email,phone").option("--qr-format <format>", "unicode|utf8|ansi|terminal").option("--qr-file <path>", "explicit QR file path").option("--locale <locale>", "payment card language: zh-CN|en", "zh-CN").option("--pay", "also create a payment intent and optionally wait for verification").option("--method <alipay|wechatpay>", "payment method for --pay", "alipay").option("--no-wait", "do not wait for payment verification after --pay").option("--timeout <seconds>", "max seconds to wait for payment", "120").option("--json", "output JSON instead of terminal text").action(async (options) => {
  const config = loadConfig();
  const backend = newBackendClient(config);
  const sessionPath = cartSessionPath();
  const session = CartSession.loadFromFile(sessionPath, config.checkoutCurrency);
  const jsonOutput = Boolean(options.json);
  try {
    const inline = [options.item, options.variant, options.offer].filter(Boolean).length;
    if (inline !== 0 && inline !== 3) {
      throw new CommandContractError("buy_source_invalid", "--item, --variant and --offer must be provided together", "inline \u8D2D\u4E70\u5FC5\u987B\u540C\u65F6\u4F7F\u7528 Catalog \u8FD4\u56DE\u7684 item\u3001variant \u548C offer\uFF1B\u4E0D\u8981\u731C\u6D4B\u6216\u90E8\u5206\u63D0\u4EA4\u3002", [{ command: "itpay catalog list --json", reason: "\u8BFB\u53D6\u5DF2\u53D1\u5E03\u9879\u76EE" }]);
    }
    if (options.cart && inline > 0) {
      throw new CommandContractError("buy_source_invalid", "--cart cannot be combined with --item/--variant/--offer", "\u5DF2\u6709 canonical Cart \u4E0E inline item \u4E8C\u9009\u4E00\uFF1B\u672C\u6B21\u672A\u4FEE\u6539\u4EFB\u4F55\u8D44\u6E90\u3002", [{ command: "itpay cart show --json", reason: "\u68C0\u67E5\u5DF2\u6709 Cart" }]);
    }
    if (options.method !== "alipay" && options.method !== "wechatpay") {
      throw new CommandContractError("payment_method_invalid", `unsupported payment method: ${options.method}`, "--method \u53EA\u63A5\u53D7 alipay \u6216 wechatpay\u3002", [{ command: "itpay buy --help", reason: "\u67E5\u770B\u4ED8\u6B3E\u53C2\u6570" }]);
    }
    if (options.wait === false && !options.pay) {
      throw new CommandContractError("buy_parameter_invalid", "--no-wait requires --pay", "\u666E\u901A buy \u4E0D\u521B\u5EFA Payment Intent\uFF1B\u79FB\u9664 --no-wait\uFF0C\u6216\u4F7F\u7528\u660E\u786E\u7684\u4ED8\u6B3E\u8FD0\u7EF4\u6D41\u7A0B\u3002", [{ command: "itpay buy --help", reason: "\u67E5\u770B\u53C2\u6570\u5173\u7CFB" }]);
    }
    const quantity = positiveInteger(options.quantity, "--quantity");
    const timeout = positiveInteger(options.timeout, "--timeout");
    const host = withHost(options.host, config.agentType, options.target);
    const contact = {};
    if (options.contactEmail)
      contact.email = options.contactEmail;
    if (options.contactPhone)
      contact.phone = options.contactPhone;
    const requiredContactFields = parseRequiredContactFields(options.requireContact);
    const missingContactFields = (requiredContactFields ?? []).filter((field) => {
      const value = contact[field];
      return typeof value !== "string" || value.trim().length === 0;
    });
    if (missingContactFields.length > 0) {
      throw new CommandContractError("missing_contact", `missing required contact fields: ${missingContactFields.join(", ")}`, `\u5411\u7528\u6237\u8BE2\u95EE ${missingContactFields.join(" \u548C ")}\uFF0C\u518D\u8865\u5145\u5BF9\u5E94 contact \u53C2\u6570\u91CD\u8DD1\u540C\u4E00\u547D\u4EE4\uFF1B\u7981\u6B62\u7F16\u9020\u3002`, [{ command: "itpay buy --help", reason: "\u67E5\u770B contact \u53C2\u6570" }]);
    }
    if (inline === 3) {
      runCartAdd(session, {
        catalogItemID: options.item,
        catalogVariantID: options.variant,
        offerID: options.offer,
        quantity,
        output: () => void 0
      });
    }
    const buyOptions = {
      cartSession: session,
      host,
      ...config.agentType ? { agentType: config.agentType } : {},
      ...options.cart ? { cartID: options.cart } : {},
      ...options.target ? { target: options.target } : {},
      ...options.ref ? { clientReferenceID: options.ref } : {},
      ...Object.keys(contact).length > 0 ? { contact } : {},
      ...requiredContactFields ? { requiredContactFields } : {},
      ...options.qrFormat ? { qrFormat: options.qrFormat } : {},
      ...options.qrFile ? { qrFilePath: options.qrFile } : {},
      locale: options.locale,
      ...options.pay ? { pay: true, payMethod: options.method, noWait: options.wait === false, payTimeoutSec: timeout } : {},
      ...jsonOutput ? { jsonOutput: true } : {}
    };
    await runBuy(backend, config, buyOptions);
  } catch (error) {
    reportCLIError(error, {
      jsonOutput,
      code: "buy_failed",
      instruction: "Checkout \u521B\u5EFA\u5931\u8D25\uFF1B\u4FDD\u7559\u5F53\u524D Cart/Checkout \u53E5\u67C4\u5E76\u6309\u6062\u590D\u547D\u4EE4\u7EE7\u7EED\uFF0C\u4E0D\u8981\u91CD\u590D\u521B\u5EFA\u8D44\u6E90\u3002",
      recovery: [
        { command: "itpay next --json", reason: "\u6062\u590D\u6700\u8FD1\u8D44\u6E90" },
        { command: "itpay cart next --json", reason: "\u68C0\u67E5 canonical Cart" }
      ]
    });
  } finally {
    session.saveToFile(sessionPath);
  }
});
program2.command("checkout").description("Read the canonical V3 checkout presentation by checkout_id + display_token").option("--host <host>", "client host").option("--target <target>").option("--id <checkout_id>").option("--token <display_token>").option("--locale <locale>", "payment card language: zh-CN|en", "zh-CN").option("--json", "output compact JSON").action(async (options) => {
  const config = loadConfig();
  const session = CartSession.loadFromFile(cartSessionPath(), config.checkoutCurrency);
  const snap = session.show();
  const backend = newBackendClient(config);
  try {
    const host = withHost(options.host, config.agentType, options.target);
    const { checkoutID, displayToken } = resolveCheckoutPresentationArgs({
      ...options.id ? { requestedCheckoutID: options.id } : {},
      ...options.token ? { requestedDisplayToken: options.token } : {},
      ...snap.lastCheckoutID ? { savedCheckoutID: snap.lastCheckoutID } : {},
      ...snap.lastDisplayToken ? { savedDisplayToken: snap.lastDisplayToken } : {}
    });
    await runCheckoutPresentation(backend, {
      checkoutID,
      displayToken,
      host,
      ...options.target ? { target: options.target } : {},
      ...config.agentType ? { agentType: config.agentType } : {},
      baseURL: config.baseURL,
      locale: options.locale,
      jsonOutput: Boolean(options.json)
    });
  } catch (error) {
    const canResumeSavedService = Boolean(snap.lastServiceExecutionID && (!options.id || options.id === snap.lastCheckoutID));
    const recovery = canResumeSavedService ? [{
      command: `itpay services checkout ${snap.lastServiceExecutionID} --resume --json`,
      reason: "\u4E3A\u540C\u4E00\u4E2A Service Execution \u8F6E\u6362 Checkout handoff"
    }] : [{ command: "itpay services list --json", reason: "\u67E5\u627E\u5F53\u524D\u8BBE\u5907\u53EF\u6062\u590D\u7684 Service Execution" }];
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "checkout_unavailable",
      instruction: error instanceof HttpError && error.status === 404 ? "\u5F53\u524D Checkout \u53E5\u67C4\u5DF2\u5931\u6548\u6216\u4E0D\u5339\u914D\uFF1B\u6062\u590D\u539F Service Execution\uFF0C\u4E0D\u8981\u521B\u5EFA\u65E0\u5173\u8D2D\u7269\u8F66\u3002" : "\u4F7F\u7528\u540C\u4E00\u7B14 Checkout \u7684\u5B8C\u6574 checkout_id \u4E0E display token\uFF1B\u4E0D\u8981\u62FC\u63A5\u4E0D\u540C Checkout \u7684\u53E5\u67C4\u3002",
      recovery
    });
  }
});
program2.command("pay").description("Create a V3 payment intent (CLI escape hatch \u2014 usually done by the checkout page)").requiredOption("--checkout <checkout_id>").requiredOption("--method <alipay|wechatpay>").option("--token <display_token>", "checkout display token; defaults only from the same saved checkout").option("--refresh", "request a fresh provider payment action for the existing intent").option("--host <host>", "client host").option("--target <target>").option("--json", "output compact JSON").action(async (options) => {
  const config = loadConfig();
  const backend = newBackendClient(config);
  const session = CartSession.loadFromFile(cartSessionPath(), config.checkoutCurrency);
  const jsonOutput = Boolean(options.json);
  try {
    if (options.method !== "alipay" && options.method !== "wechatpay") {
      throw new CommandContractError("payment_method_invalid", `unsupported payment method: ${options.method}`, "--method \u53EA\u63A5\u53D7 alipay \u6216 wechatpay\uFF1B\u672C\u6B21\u672A\u521B\u5EFA Payment Intent\u3002", [{ command: "itpay pay --help", reason: "\u67E5\u770B\u53D7\u652F\u6301\u53C2\u6570" }]);
    }
    const displayToken = options.token ?? (session.lastCheckoutID === options.checkout ? session.lastDisplayToken : void 0);
    if (!displayToken) {
      throw new CommandContractError("checkout_token_required", "display token is required for this checkout", "\u63D0\u4F9B\u540C\u4E00 Checkout \u7684 display token\uFF1B\u4E0D\u8981\u62FC\u63A5\u5176\u4ED6 Checkout \u7684 token\u3002", [{ command: "itpay next --json", reason: "\u6062\u590D\u672C\u673A\u4FDD\u5B58\u7684\u540C\u4E00 Checkout" }]);
    }
    const host = withHost(options.host, config.agentType, options.target);
    const contextError = validateContext(host, options.target);
    if (contextError) {
      throw new CommandContractError(contextError.code, contextError.message, "\u4E3A\u5F53\u524D Host \u63D0\u4F9B\u6709\u6548 target\uFF1B\u672C\u6B21\u672A\u521B\u5EFA Payment Intent\u3002", [
        { command: "itpay pay --help", reason: "\u67E5\u770B Host \u53C2\u6570" }
      ]);
    }
    await runPay(backend, {
      checkoutID: options.checkout,
      displayToken,
      method: options.method,
      host,
      ...config.agentType ? { agentType: config.agentType } : {},
      ...options.refresh ? { refreshAction: true } : {},
      ...jsonOutput ? { jsonOutput: true } : {}
    });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput,
      code: "payment_intent_failed",
      instruction: "\u4E0D\u8981\u521B\u5EFA\u66FF\u4EE3 Checkout\uFF1B\u6062\u590D\u540C\u4E00 Checkout \u5E76\u7531\u7528\u6237\u5728 ItPay \u9875\u9762\u7EE7\u7EED\u4ED8\u6B3E\u3002",
      recovery: [{ command: "itpay next --json", reason: "\u6062\u590D\u5F53\u524D Checkout" }]
    });
  }
});
program2.command("order").description("Read a V3 order by id").argument("<order_id>").option("--host <host>", "client host").option("--json", "output JSON instead of terminal text").action(async (orderID, options) => {
  if (options.host)
    withHost(options.host);
  const config = loadConfig();
  const backend = newBackendClient(config);
  try {
    await runOrder(backend, orderID, { ...options.host ? { host: options.host } : {}, jsonOutput: Boolean(options.json) });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "order_read_failed",
      instruction: "\u786E\u8BA4\u8BA2\u5355\u5C5E\u4E8E\u5F53\u524D\u8D26\u53F7\u6216\u5DF2\u7ED1\u5B9A Agent\uFF1B\u4E0D\u8981\u901A\u8FC7\u9519\u8BEF\u5DEE\u5F02\u63A2\u6D4B\u5176\u4ED6\u8D26\u53F7\u7684\u8BA2\u5355\u3002",
      recovery: [{ command: "itpay services list --json", reason: "\u6062\u590D\u5F53\u524D\u8EAB\u4EFD\u53EF\u89C1\u7684 Service Execution" }]
    });
  }
});
program2.command("orders").description("List V3 orders for the account-scoped bearer session").option("--limit <n>", "max orders", (value) => Number.parseInt(value, 10), 20).option("--status <status>").option("--json", "output JSON instead of terminal text").action(async (options) => {
  const config = loadConfig();
  const backend = newBackendClient(config);
  try {
    await runListOrders(backend, config, {
      limit: options.limit,
      status: options.status,
      jsonOutput: Boolean(options.json)
    });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "orders_list_failed",
      instruction: "\u8BA2\u5355\u5386\u53F2\u53EA\u5BF9 account-scoped Buyer session \u5F00\u653E\uFF1B\u4E0D\u8981\u901A\u8FC7\u9519\u8BEF\u5DEE\u5F02\u63A2\u6D4B\u5176\u4ED6\u8D26\u53F7\u3002",
      recovery: [{ command: "itpay services list --json", reason: "\u6062\u590D\u5F53\u524D Agent \u8BBE\u5907\u53EF\u89C1\u7684\u6267\u884C" }]
    });
  }
});
var refund = program2.command("refund").enablePositionalOptions().description("Create a V3 refund request for an order").option("--order <order_id>").option("--reason <reason>").option("--json", "output JSON instead of terminal text").action(async (options) => {
  if (!options.order) {
    process.stdout.write(refund.helpInformation());
    process.stdout.write("\ninstruction: \u4F7F\u7528 `itpay refund create --order <order_id>` \u63D0\u4EA4\u9000\u6B3E\uFF1B\u672C\u6B21\u672A\u53D1\u9001\u8BF7\u6C42\u3002\n");
    return;
  }
  await executeRefundCreate(options.order, options.reason, Boolean(options.json));
});
refund.command("create").option("--order <order_id>").option("--reason <reason>").option("--json", "output JSON instead of terminal text").action(async (options) => {
  const inherited = refund.opts();
  const orderID = options.order ?? inherited.order;
  if (!orderID) {
    reportCLIError(new Error("--order is required"), {
      jsonOutput: Boolean(options.json ?? inherited.json),
      code: "order_required",
      instruction: "\u4F7F\u7528\u7528\u6237\u8BA2\u5355\u7684 order_id\uFF1B\u4E0D\u8981\u731C\u6D4B\u6216\u4EE3\u586B\u3002",
      recovery: [{ command: "itpay services list --json", reason: "\u6062\u590D\u5F53\u524D\u8EAB\u4EFD\u53EF\u89C1\u7684 Service Execution" }]
    });
    return;
  }
  const reason = options.reason ?? inherited.reason;
  await executeRefundCreate(orderID, reason, Boolean(options.json ?? inherited.json));
});
refund.command("list").option("--order <order_id>").option("--json", "output JSON instead of terminal text").action(async (options) => {
  const inherited = refund.opts();
  const orderID = options.order ?? inherited.order;
  const jsonOutput = Boolean(options.json ?? inherited.json);
  if (!orderID) {
    reportCLIError(new Error("--order is required"), {
      jsonOutput,
      code: "order_required",
      instruction: "\u4F7F\u7528\u7528\u6237\u8BA2\u5355\u7684 order_id\uFF1B\u4E0D\u8981\u731C\u6D4B\u6216\u4EE3\u586B\u3002",
      recovery: [{ command: "itpay services list --json", reason: "\u6062\u590D\u5F53\u524D\u8EAB\u4EFD\u53EF\u89C1\u7684 Service Execution" }]
    });
    return;
  }
  const config = loadConfig();
  try {
    await runListRefunds(newBackendClient(config), { orderID, jsonOutput });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput,
      code: "refund_list_failed",
      instruction: "\u786E\u8BA4\u8BA2\u5355\u5C5E\u4E8E\u5F53\u524D\u8D26\u53F7\u6216\u5DF2\u7ED1\u5B9A Agent\uFF1B\u4E0D\u8981\u63A2\u6D4B\u5176\u4ED6\u8D26\u53F7\u7684\u9000\u6B3E\u3002",
      recovery: [{ command: "itpay services list --json", reason: "\u6062\u590D\u5F53\u524D\u8EAB\u4EFD\u53EF\u89C1\u7684 Service Execution" }]
    });
  }
});
refund.command("get").argument("<refund_request_id>").option("--json", "output JSON instead of terminal text").action(async (id, options) => {
  const config = loadConfig();
  try {
    await runGetRefund(newBackendClient(config), id, { jsonOutput: Boolean(options.json ?? refund.opts().json) });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json ?? refund.opts().json),
      code: "refund_read_failed",
      instruction: "\u786E\u8BA4\u9000\u6B3E\u5C5E\u4E8E\u5F53\u524D\u8D26\u53F7\u6216\u5DF2\u7ED1\u5B9A Agent\uFF1B\u4E0D\u8981\u63A2\u6D4B\u5176\u4ED6\u8D26\u53F7\u7684\u9000\u6B3E\u3002",
      recovery: [{ command: "itpay services list --json", reason: "\u6062\u590D\u5F53\u524D\u8EAB\u4EFD\u53EF\u89C1\u7684 Service Execution" }]
    });
  }
});
refund.command("watch").argument("<refund_request_id>").option("--interval <seconds>", "poll interval", Number, 2).option("--timeout <seconds>", "timeout", Number, 120).option("--json", "output JSON instead of terminal text").action(async (id, options) => {
  const config = loadConfig();
  try {
    await runWatchRefund(newBackendClient(config), id, {
      intervalSeconds: options.interval,
      timeoutSeconds: options.timeout,
      jsonOutput: Boolean(options.json ?? refund.opts().json)
    });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json ?? refund.opts().json),
      code: "refund_watch_failed",
      instruction: "\u68C0\u67E5\u9000\u6B3E ID \u548C\u8F6E\u8BE2\u53C2\u6570\u540E\u6062\u590D\u540C\u4E00\u9000\u6B3E\uFF1B\u4E0D\u8981\u91CD\u590D\u7533\u8BF7\u3002",
      recovery: [{ command: `itpay refund get ${id} --json`, reason: "\u8BFB\u53D6\u5F53\u524D\u6743\u5A01\u72B6\u6001" }]
    });
  }
});
refund.command("cancel").argument("<refund_request_id>").option("--reason <reason>").option("--json", "output JSON instead of terminal text").action(async (id, options) => {
  const config = loadConfig();
  try {
    await runCancelRefund(newBackendClient(config), id, options.reason, { jsonOutput: Boolean(options.json ?? refund.opts().json) });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json ?? refund.opts().json),
      code: "refund_cancel_failed",
      instruction: "\u53D6\u6D88\u672A\u751F\u6548\uFF1B\u4EE5 Refund Owner \u5F53\u524D\u72B6\u6001\u4E3A\u51C6\uFF0C\u4E0D\u8981\u91CD\u590D\u9000\u6B3E\u6216\u81EA\u884C\u89E3\u9664\u4EA4\u4ED8\u9501\u3002",
      recovery: [{ command: `itpay refund get ${id} --json`, reason: "\u8BFB\u53D6\u5F53\u524D\u6743\u5A01\u72B6\u6001" }]
    });
  }
});
async function executeRefundCreate(orderID, reason, jsonOutput) {
  const config = loadConfig();
  try {
    await runRefund(newBackendClient(config), config, { orderID, ...reason ? { reason } : {}, jsonOutput });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput,
      code: "refund_create_failed",
      instruction: "\u786E\u8BA4\u8BA2\u5355\u5C5E\u4E8E\u5F53\u524D\u8D26\u53F7\u4E14\u53EF\u9000\u6B3E\uFF1B\u4E0D\u8981\u4FEE\u6539\u91D1\u989D\u3001\u652F\u4ED8\u6216\u6D88\u8D39\u4E8B\u5B9E\u3002",
      recovery: [
        { command: `itpay order ${orderID} --json`, reason: "\u68C0\u67E5\u8BA2\u5355\u548C\u4EA4\u4ED8\u9501" },
        { command: `itpay refund list --order ${orderID} --json`, reason: "\u68C0\u67E5\u5DF2\u6709\u9000\u6B3E" }
      ]
    });
  }
}
var services = program2.command("services").description("Generic V3 Service Execution commands");
services.command("start").description("Start a contract-backed service execution").argument("<service_id>").option("--host <host>", "client host").option("--target <target>").option("--json", "output JSON instead of terminal text").action(async (serviceID, options) => {
  const config = loadConfig();
  const backend = newBackendClient(config);
  try {
    await runServicesStart(backend, serviceID, {
      host: withHost(options.host, config.agentType, options.target),
      ...options.target ? { target: options.target } : {},
      jsonOutput: Boolean(options.json)
    });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "service_start_failed",
      instruction: "\u53EA\u4F7F\u7528\u5DF2\u53D1\u5E03 Catalog \u8FD4\u56DE\u7684 service_id\uFF1B\u8BBE\u5907\u8EAB\u4EFD\u95EE\u9898\u5E94\u7531 CLI \u81EA\u52A8\u6062\u590D\u3002",
      recovery: [
        { command: "itpay catalog list", reason: "\u91CD\u65B0\u53D6\u5F97\u6709\u6548 service_id" },
        { command: "itpay readyz", reason: "\u786E\u8BA4 Backend \u53EF\u7528" }
      ]
    });
  }
});
services.command("invoke").description("Invoke an agent-visible service capability").argument("<service_execution_id>").requiredOption("--capability <capability_id>").option("--input <key=value>", "redacted input summary", collectOption, []).option("--json", "output JSON").action(async (serviceExecutionID, options) => {
  const config = loadConfig();
  const backend = newBackendClient(config);
  try {
    await runServicesInvoke(backend, config, serviceExecutionID, options.capability, parseKeyValueList(options.input), { jsonOutput: Boolean(options.json) });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "service_invoke_failed",
      instruction: "\u8BFB\u53D6\u5F53\u524D Service Execution \u7684\u5408\u6CD5\u4E0B\u4E00\u6B65\u540E\u91CD\u8BD5\uFF1B\u4E0D\u8981\u590D\u7528\u5DF2\u7ED3\u675F\u7684 execution\u3002",
      recovery: [
        { command: `itpay services next ${serviceExecutionID} --json`, reason: "\u8BFB\u53D6\u5F53\u524D\u5408\u6CD5\u52A8\u4F5C" },
        { command: `itpay services get ${serviceExecutionID} --json`, reason: "\u68C0\u67E5\u6267\u884C\u72B6\u6001" }
      ]
    });
  }
});
services.command("action").description("Record a service execution action or human handoff result").argument("<service_execution_id>").requiredOption("--action <action_type>").option("--actor-type <actor_type>").option("--actor-id <actor_id>").option("--status <status>", "pending, approved, rejected, expired, or cancelled").option("--candidate <rank>", "select a displayed candidate by its rank", Number).option("--result-item <service_capability_result_item_id>").option("--required-before <step>").option("--input <key=value>", "action input snapshot", collectOption, []).option("--json", "output JSON instead of terminal text").action(async (serviceExecutionID, options) => {
  const config = loadConfig();
  const backend = newBackendClient(config);
  try {
    await runServicesAction(backend, serviceExecutionID, options.action, parseKeyValueList(options.input), {
      ...options.actorType ? { actorType: options.actorType } : {},
      ...options.actorId ? { actorID: options.actorId } : {},
      ...options.status ? { status: options.status } : {},
      ...options.candidate !== void 0 ? { candidateRank: options.candidate } : {},
      ...options.resultItem ? { resultItemID: options.resultItem } : {},
      ...options.requiredBefore ? { requiredBefore: options.requiredBefore } : {},
      jsonOutput: Boolean(options.json)
    });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "service_action_failed",
      instruction: "\u8BFB\u53D6\u5F53\u524D Service Execution \u7684\u5408\u6CD5 action \u540E\u91CD\u8BD5\uFF1B\u4E0D\u8981\u731C\u6D4B\u72B6\u6001\u6216\u5019\u9009 ID\u3002",
      recovery: [
        { command: `itpay services next ${serviceExecutionID} --json`, reason: "\u8BFB\u53D6\u5F53\u524D\u53EF\u9009\u52A8\u4F5C" },
        { command: `itpay services get ${serviceExecutionID} --json`, reason: "\u68C0\u67E5\u6267\u884C\u72B6\u6001" }
      ]
    });
  }
});
services.command("quote").description("Prepare a paid service quote without creating a Cart or Checkout").argument("<service_execution_id>").requiredOption("--capability <capability_id>").option("--input <key=value>", "input to lock into the paid service quote", collectOption, []).option("--email <delivery_email>").option("--json", "output compact JSON").action(async (serviceExecutionID, options) => {
  const config = loadConfig();
  try {
    await runServicesQuote(newBackendClient(config), serviceExecutionID, options.capability, parseKeyValueList(options.input), { ...options.email ? { email: options.email } : {}, jsonOutput: Boolean(options.json) });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "service_quote_failed",
      instruction: "\u6309\u5F53\u524D Execution \u7684\u5408\u6CD5\u4ED8\u8D39 capability \u548C\u53EF\u4FE1\u8F93\u5165\u91CD\u8BD5\uFF1B\u672C\u6B21\u4E0D\u8981\u81EA\u884C\u521B\u5EFA Cart \u6216 Checkout\u3002",
      recovery: [{ command: `itpay services next ${serviceExecutionID} --json`, reason: "\u8BFB\u53D6\u5F53\u524D\u5408\u6CD5\u52A8\u4F5C" }]
    });
  }
});
services.command("checkout").description("Create checkout from a service execution and render the ItPay checkout handoff").argument("<service_execution_id>").option("--capability <capability_id>").option("--input <key=value>", "input to lock into the paid service quote", collectOption, []).option("--email <delivery_email>").option("--resume", "reissue the existing checkout handoff without creating another checkout").option("--host <host>", "client host (terminal, codex, telegram, feishu, lark, ...)").option("--target <target>", "chat id / channel id / open id for IM hosts").option("--qr-format <format>", "unicode|utf8|ansi|terminal").option("--qr-file <path>", "explicit QR file path").option("--locale <locale>", "payment card language: zh-CN|en", "zh-CN").option("--json", "output JSON instead of terminal text").action(async (serviceExecutionID, options) => {
  const config = loadConfig();
  const backend = newBackendClient(config);
  const sessionPath = cartSessionPath();
  const session = CartSession.loadFromFile(sessionPath, config.checkoutCurrency);
  try {
    await runServicesCheckout(backend, config, serviceExecutionID, options.capability, {
      ...options.email ? { email: options.email } : {},
      lockedInput: parseKeyValueList(options.input),
      resume: Boolean(options.resume),
      host: withHost(options.host, config.agentType, options.target),
      ...config.agentType ? { agentType: config.agentType } : {},
      ...options.target ? { target: options.target } : {},
      ...options.qrFormat ? { qrFormat: options.qrFormat } : {},
      ...options.qrFile ? { qrFilePath: options.qrFile } : {},
      locale: options.locale,
      jsonOutput: Boolean(options.json),
      persistHandoff: (handoff) => {
        session.rememberCheckout({
          checkoutID: handoff.checkoutID,
          displayToken: handoff.displayToken,
          checkoutURL: handoff.checkoutURL,
          serviceExecutionID: handoff.serviceExecutionID
        });
        session.saveToFile(sessionPath);
      }
    });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "service_checkout_failed",
      instruction: "\u8BFB\u53D6\u5F53\u524D Service Execution \u540E\u6309\u670D\u52A1\u7AEF\u5141\u8BB8\u7684 capability\u3001\u8F93\u5165\u548C\u4EA4\u4ED8\u8981\u6C42\u91CD\u8BD5\uFF1B\u4E0D\u8981\u521B\u5EFA\u66FF\u4EE3 Checkout\u3002",
      recovery: [
        { command: `itpay services next ${serviceExecutionID} --json`, reason: "\u8BFB\u53D6\u5F53\u524D\u5408\u6CD5\u4E0B\u4E00\u6B65" },
        { command: `itpay services get ${serviceExecutionID} --json`, reason: "\u68C0\u67E5 Checkout \u4E0E\u6267\u884C\u72B6\u6001" }
      ]
    });
  }
});
services.command("list").description("Recover service executions visible to this enrolled device or account").option("--limit <number>", "maximum executions", "10").option("--json", "output compact JSON").action(async (options) => {
  const config = loadConfig();
  const backend = newBackendClient(config);
  try {
    await runServicesList(backend, { limit: Number.parseInt(options.limit, 10), jsonOutput: Boolean(options.json) });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "services_list_failed",
      instruction: "\u786E\u8BA4\u5F53\u524D\u8BBE\u5907\u8EAB\u4EFD\u548C Backend \u540E\u91CD\u8BD5\uFF1B\u4E0D\u8981\u731C\u6D4B Service Execution ID\u3002",
      recovery: [
        { command: "itpay readyz --json", reason: "\u786E\u8BA4 Backend \u53EF\u7528" },
        { command: "itpay services list --limit 10 --json", reason: "\u91CD\u65B0\u8BFB\u53D6\u6700\u8FD1\u6267\u884C" }
      ]
    });
  }
});
services.command("get").description("Read a service execution timeline").argument("<service_execution_id>").option("--json", "output compact JSON").action(async (serviceExecutionID, options) => {
  const config = loadConfig();
  const backend = newBackendClient(config);
  try {
    await runServicesGet(backend, serviceExecutionID, { jsonOutput: Boolean(options.json) });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "service_get_failed",
      instruction: "\u786E\u8BA4 execution \u5C5E\u4E8E\u5F53\u524D\u8BBE\u5907\u6216\u8D26\u53F7\uFF1B\u4E0D\u8981\u901A\u8FC7\u9519\u8BEF\u5DEE\u5F02\u63A2\u6D4B\u5176\u4ED6\u8D26\u53F7\u3002",
      recovery: [{ command: "itpay services list --json", reason: "\u8BFB\u53D6\u5F53\u524D\u8EAB\u4EFD\u53EF\u89C1\u7684\u6267\u884C" }]
    });
  }
});
services.command("next").description("Show the next recommended agent action for a Service Execution").argument("<service_execution_id>").option("--json", "output JSON instead of terminal text").action(async (serviceExecutionID, options) => {
  const config = loadConfig();
  const backend = newBackendClient(config);
  try {
    await runServicesNext(backend, serviceExecutionID, { jsonOutput: Boolean(options.json) });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "service_next_failed",
      instruction: "\u68C0\u67E5 Service Execution \u662F\u5426\u5C5E\u4E8E\u5F53\u524D\u8BBE\u5907\u6216\u8D26\u53F7\uFF0C\u7136\u540E\u8BFB\u53D6\u5B8C\u6574\u65F6\u95F4\u7EBF\u3002",
      recovery: [{ command: `itpay services get ${serviceExecutionID} --json`, reason: "\u68C0\u67E5\u6267\u884C\u72B6\u6001\u4E0E\u5F52\u5C5E" }]
    });
  }
});
services.command("read-result").description("Read a human-granted service result for this agent").argument("<service_execution_id>").option("--json", "output JSON instead of terminal text").action(async (serviceExecutionID, options) => {
  const config = loadConfig();
  const backend = newBackendClient(config);
  try {
    await runServicesReadResult(backend, serviceExecutionID, { jsonOutput: Boolean(options.json) });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "agent_access_denied",
      instruction: "\u8BF7\u7528\u6237\u5728\u8BA2\u5355\u9875\u9762\u91CD\u65B0\u6388\u6743\uFF1B\u4E0D\u8981\u4F7F\u7528\u5F00\u53D1\u8005\u6743\u9650\u7ED5\u8FC7\u6388\u6743\u6216\u9000\u6B3E\u9501\u3002",
      recovery: [{ command: `itpay services next ${serviceExecutionID} --json`, reason: "\u68C0\u67E5\u4EA4\u4ED8\u6A21\u5F0F\u548C grant \u72B6\u6001" }]
    });
  }
});
services.command("events").description("List redacted service execution events").argument("<service_execution_id>").option("--after-sequence <number>", "return events after this sequence", "0").option("--limit <number>", "maximum events (1-100)", "50").option("--json", "output compact JSON").action(async (serviceExecutionID, options) => {
  const config = loadConfig();
  const backend = newBackendClient(config);
  try {
    await runServicesEvents(backend, serviceExecutionID, {
      afterSequence: Number(options.afterSequence),
      limit: Number(options.limit),
      jsonOutput: Boolean(options.json)
    });
  } catch (error) {
    reportCLIError(error, {
      jsonOutput: Boolean(options.json),
      code: "service_events_failed",
      instruction: "\u786E\u8BA4 execution \u5C5E\u4E8E\u5F53\u524D\u8EAB\u4EFD\uFF1B\u4E8B\u4EF6\u53EA\u7528\u4E8E\u8BCA\u65AD\uFF0C\u4E0D\u8981\u636E\u6B64\u91CD\u653E\u4E1A\u52A1\u6B65\u9AA4\u3002",
      recovery: [
        { command: `itpay services next ${serviceExecutionID} --json`, reason: "\u8BFB\u53D6\u5F53\u524D\u4E1A\u52A1\u52A8\u4F5C" },
        { command: "itpay services list --json", reason: "\u5217\u51FA\u5F53\u524D\u8EAB\u4EFD\u53EF\u89C1\u6267\u884C" }
      ]
    });
  }
});
program2.parseAsync(process.argv).catch((error) => {
  reportCLIError(error);
});
