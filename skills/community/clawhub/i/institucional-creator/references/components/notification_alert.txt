You are given a task to integrate an existing React component in the codebase

The codebase should support:
- shadcn project structure  
- Tailwind CSS
- Typescript

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind or Typescript.

Determine the default path for components and styles. 
If default path for components is not /components/ui, provide instructions on why it's important to create this folder
Copy-paste this component to /components/ui folder:
```tsx
notification-alert-dialog.tsx
"use client"

import { BellRing, X, Clock, Check } from "lucide-react"
import { useState } from "react"

import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface Notification {
    id: string
    sender: {
        name: string
        initials: string
    }
    message: string
    time: string
    read: boolean
}

export function Component() {
    const [notifications, setNotifications] = useState<Notification[]>([
        {
            id: "1",
            sender: {
                name: "John Doe",
                initials: "JD",
            },
            message: "Hey, can we discuss the project timeline?",
            time: "5 minutes ago",
            read: false,
        },
        {
            id: "2",
            sender: {
                name: "Alice Smith",
                initials: "AS",
            },
            message: "I've uploaded the design files you requested",
            time: "10 minutes ago",
            read: false,
        },
        {
            id: "3",
            sender: {
                name: "Robert Johnson",
                initials: "RJ",
            },
            message: "The client meeting has been rescheduled to tomorrow",
            time: "1 hour ago",
            read: false,
        },
        {
            id: "4",
            sender: {
                name: "Emily Davis",
                initials: "ED",
            },
            message: "Please review the latest changes to the documentation",
            time: "2 hours ago",
            read: false,
        },
        {
            id: "5",
            sender: {
                name: "Michael Wilson",
                initials: "MW",
            },
            message: "Don't forget about our team meeting at 3 PM today",
            time: "3 hours ago",
            read: false,
        },
    ])

    const [isDialogOpen, setIsDialogOpen] = useState(false)
    const [showAllNotifications, setShowAllNotifications] = useState(false)

    const markAsRead = (id: string) => {
        setNotifications(
            notifications.map((notification) => (notification.id === id ? { ...notification, read: true } : notification)),
        )
    }

    const markAllAsRead = () => {
        setNotifications(notifications.map((notification) => ({ ...notification, read: true })))
    }

    const unreadCount = notifications.filter((notification) => !notification.read).length

    return (
        <>
            <AlertDialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                <AlertDialogTrigger asChild>
                    <Button className="relative pr-6 bg-indigo-500 hover:bg-indigo-600 dark:bg-indigo-600 dark:hover:bg-indigo-700 text-white">
                        <BellRing className="h-5 w-5 mr-1" />
                        Notifications
                        {unreadCount > 0 && (
                            <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                                {unreadCount}
                            </span>
                        )}
                    </Button>
                </AlertDialogTrigger>
                <AlertDialogContent className="border-indigo-200 dark:border-indigo-900 border-2 max-w-md bg-white dark:bg-gray-900">
                    <AlertDialogHeader>
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <BellRing className="h-5 w-5 text-indigo-500 dark:text-indigo-400" />
                                <AlertDialogTitle className="dark:text-white">Notifications</AlertDialogTitle>
                            </div>
                            {unreadCount > 0 && (
                                <Button
                                    variant="ghost"
                                    size="sm"
                                    onClick={markAllAsRead}
                                    className="text-xs text-indigo-500 hover:text-indigo-600 dark:text-indigo-400 dark:hover:text-indigo-300 dark:hover:bg-black/50"
                                >
                                    Mark all as read
                                </Button>
                            )}
                        </div>
                        <AlertDialogDescription className="dark:text-gray-400">
                            You have {unreadCount} unread {unreadCount === 1 ? "message" : "messages"} from your team members.
                        </AlertDialogDescription>
                    </AlertDialogHeader>
                    <div className="my-3 space-y-2">
                        {notifications.slice(0, showAllNotifications ? notifications.length : 2).map((notification) => (
                            <div
                                key={notification.id}
                                className={cn(
                                    "flex items-center gap-3 p-3 rounded-md transition-all duration-200 cursor-pointer",
                                    notification.read ? "bg-gray-100 dark:bg-gray-800" : "bg-indigo-50 dark:bg-indigo-900/40 shadow-sm",
                                )}
                                onClick={() => markAsRead(notification.id)}
                            >
                                <div
                                    className={cn(
                                        "w-10 h-10 rounded-full flex items-center justify-center font-medium shrink-0",
                                        notification.read
                                            ? "bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300"
                                            : "bg-indigo-200 text-indigo-700 dark:bg-indigo-800 dark:text-indigo-300",
                                    )}
                                >
                                    {notification.sender.initials}
                                </div>
                                <div className="flex-1 min-w-0">
                                    <p
                                        className={cn(
                                            "text-sm font-medium",
                                            notification.read ? "text-gray-700 dark:text-gray-300" : "text-gray-900 dark:text-white",
                                        )}
                                    >
                                        {notification.sender.name}
                                    </p>
                                    <p className="text-xs text-gray-500 dark:text-gray-400 truncate">{notification.message}</p>
                                    <div className="flex items-center text-xs text-gray-400 dark:text-gray-500 mt-1">
                                        <Clock className="h-3 w-3 mr-1" />
                                        {notification.time}
                                    </div>
                                </div>
                                {!notification.read && (
                                    <span className="h-2.5 w-2.5 rounded-full bg-indigo-500 dark:bg-indigo-400 shrink-0"></span>
                                )}
                            </div>
                        ))}
                    </div>
                    <AlertDialogFooter>
                        <AlertDialogCancel
                            onClick={() => {
                                setShowAllNotifications(false)
                            }}
                            className="border-indigo-200 text-indigo-700 hover:bg-indigo-50 dark:border-indigo-800 dark:text-indigo-400 dark:hover:bg-indigo-900/40"
                        >
                            Close
                        </AlertDialogCancel>
                        <AlertDialogAction
                            className="bg-indigo-500 hover:bg-indigo-600 dark:text-white dark:bg-indigo-700 dark:hover:bg-indigo-800"
                            onClick={() => {
                                setShowAllNotifications(true)
                                setIsDialogOpen(false)
                                document.body.classList.add("overflow-hidden")
                            }}
                        >
                            View All
                        </AlertDialogAction>
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialog>
            <div
                className={cn(
                    "fixed inset-0 bg-black/50 dark:bg-black/70 z-50 transition-opacity duration-300",
                    showAllNotifications ? "opacity-100" : "opacity-0 pointer-events-none",
                )}
            >
                <div
                    className={cn(
                        "fixed top-0 right-0 h-full shadow-lg transition-transform duration-300 ease-in-out transform w-full max-w-md",
                        "bg-white dark:bg-gray-900 border-l border-gray-200 dark:border-gray-800",
                        showAllNotifications ? "translate-x-0" : "translate-x-full",
                    )}
                >
                    <div className="flex flex-col h-full">
                        <div className="p-4 border-b border-gray-200 dark:border-gray-800 flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <BellRing className="h-5 w-5 text-indigo-500 dark:text-indigo-400" />
                                <h2 className="text-lg font-semibold dark:text-white">All Notifications</h2>
                            </div>
                            <Button
                                variant="ghost"
                                size="icon"
                                onClick={() => {
                                    setShowAllNotifications(false)
                                    document.body.classList.remove("overflow-hidden")
                                }}
                                className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                            >
                                <X className="h-5 w-5" />
                                <span className="sr-only">Close</span>
                            </Button>
                        </div>
                        <div className="flex-1 overflow-y-auto p-4 space-y-3 scrollbar-thin scrollbar-thumb-indigo-200 dark:scrollbar-thumb-indigo-800">
                            {notifications.length === 0 ? (
                                <div className="flex flex-col items-center justify-center h-full text-gray-500 dark:text-gray-400">
                                    <BellRing className="h-12 w-12 mb-2 text-gray-300 dark:text-gray-700" />
                                    <p>No notifications</p>
                                </div>
                            ) : (
                                notifications.map((notification) => (
                                    <div
                                        key={notification.id}
                                        className={cn(
                                            "flex items-start gap-3 p-4 rounded-lg transition-all duration-200 cursor-pointer",
                                            notification.read
                                                ? "bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700"
                                                : "bg-indigo-50 dark:bg-indigo-900/40 border border-indigo-100 dark:border-indigo-800 shadow-sm",
                                        )}
                                        onClick={() => markAsRead(notification.id)}
                                    >
                                        <div
                                            className={cn(
                                                "w-10 h-10 rounded-full flex items-center justify-center font-medium shrink-0",
                                                notification.read
                                                    ? "bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300"
                                                    : "bg-indigo-200 text-indigo-700 dark:bg-indigo-800 dark:text-indigo-300",
                                            )}
                                        >
                                            {notification.sender.initials}
                                        </div>
                                        <div className="flex-1">
                                            <div className="flex justify-between items-start">
                                                <p
                                                    className={cn(
                                                        "text-sm font-medium",
                                                        notification.read ? "text-gray-700 dark:text-gray-300" : "text-gray-900 dark:text-white",
                                                    )}
                                                >
                                                    {notification.sender.name}
                                                </p>
                                                <div className="flex items-center text-xs text-gray-400 dark:text-gray-500">
                                                    <Clock className="h-3 w-3 mr-1" />
                                                    {notification.time}
                                                </div>
                                            </div>
                                            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{notification.message}</p>

                                            {notification.read && (
                                                <div className="flex items-center mt-2 text-xs text-indigo-500 dark:text-indigo-400">
                                                    <Check className="h-3 w-3 mr-1" />
                                                    Read
                                                </div>
                                            )}
                                        </div>
                                        {!notification.read && (
                                            <span className="h-2.5 w-2.5 rounded-full bg-indigo-500 dark:bg-indigo-400 shrink-0 mt-2"></span>
                                        )}
                                    </div>
                                ))
                            )}
                        </div>
                        <div className="p-4 border-t border-gray-200 dark:border-gray-800">
                            <Button
                                className="w-full bg-indigo-500 hover:bg-indigo-600 dark:bg-indigo-600 dark:hover:bg-indigo-700"
                                onClick={() => {
                                    markAllAsRead()
                                    setShowAllNotifications(false)
                                    document.body.classList.remove("overflow-hidden")
                                }}
                            >
                                Mark All as Read
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

demo.tsx
import { Component } from "@/components/ui/notification-alert-dialog";

export default function AlertDialogDemo() {
  return (
    <div className="flex w-full h-screen justify-center items-center">
      <Component />
    </div>
  );
};
```

Copy-paste these files for dependencies:
```tsx
shadcn/alert-dialog
"use client"

import * as React from "react"
import * as AlertDialogPrimitive from "@radix-ui/react-alert-dialog"

import { cn } from "@/lib/utils"
import { buttonVariants } from "@/components/ui/button"

const AlertDialog = AlertDialogPrimitive.Root

const AlertDialogTrigger = AlertDialogPrimitive.Trigger

const AlertDialogPortal = AlertDialogPrimitive.Portal

const AlertDialogOverlay = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Overlay
    className={cn(
      "fixed inset-0 z-50 bg-black/80  data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className
    )}
    {...props}
    ref={ref}
  />
))
AlertDialogOverlay.displayName = AlertDialogPrimitive.Overlay.displayName

const AlertDialogContent = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Content>
>(({ className, ...props }, ref) => (
  <AlertDialogPortal>
    <AlertDialogOverlay />
    <AlertDialogPrimitive.Content
      ref={ref}
      className={cn(
        "fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg",
        className
      )}
      {...props}
    />
  </AlertDialogPortal>
))
AlertDialogContent.displayName = AlertDialogPrimitive.Content.displayName

const AlertDialogHeader = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      "flex flex-col space-y-2 text-center sm:text-left",
      className
    )}
    {...props}
  />
)
AlertDialogHeader.displayName = "AlertDialogHeader"

const AlertDialogFooter = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      "flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2",
      className
    )}
    {...props}
  />
)
AlertDialogFooter.displayName = "AlertDialogFooter"

const AlertDialogTitle = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Title>
>(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Title
    ref={ref}
    className={cn("text-lg font-semibold", className)}
    {...props}
  />
))
AlertDialogTitle.displayName = AlertDialogPrimitive.Title.displayName

const AlertDialogDescription = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Description>
>(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Description
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
))
AlertDialogDescription.displayName =
  AlertDialogPrimitive.Description.displayName

const AlertDialogAction = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Action>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Action>
>(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Action
    ref={ref}
    className={cn(buttonVariants(), className)}
    {...props}
  />
))
AlertDialogAction.displayName = AlertDialogPrimitive.Action.displayName

const AlertDialogCancel = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Cancel>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Cancel>
>(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Cancel
    ref={ref}
    className={cn(
      buttonVariants({ variant: "outline" }),
      "mt-2 sm:mt-0",
      className
    )}
    {...props}
  />
))
AlertDialogCancel.displayName = AlertDialogPrimitive.Cancel.displayName

export {
  AlertDialog,
  AlertDialogPortal,
  AlertDialogOverlay,
  AlertDialogTrigger,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogFooter,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogAction,
  AlertDialogCancel,
}

```
```tsx
shadcn/button
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive:
          "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline:
          "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary:
          "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  },
)
Button.displayName = "Button"

export { Button, buttonVariants }

```

Install NPM dependencies:
```bash
lucide-react, @radix-ui/react-alert-dialog, @radix-ui/react-slot, class-variance-authority
```

Implementation Guidelines
 1. Analyze the component structure and identify all required dependencies
 2. Review the component's argumens and state
 3. Identify any required context providers or hooks and install them
 4. Questions to Ask
 - What data/props will be passed to this component?
 - Are there any specific state management requirements?
 - Are there any required assets (images, icons, etc.)?
 - What is the expected responsive behavior?
 - What is the best place to use this component in the app?

Steps to integrate
 0. Copy paste all the code above in the correct directories
 1. Install external dependencies
 2. Fill image assets with Unsplash stock images you know exist
 3. Use lucide-react icons for svgs or logos if component requires them
